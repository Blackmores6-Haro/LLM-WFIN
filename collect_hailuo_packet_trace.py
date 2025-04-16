import math
import threading
import time
import os
import pickle
import queue
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from browsermobproxy import Server
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException
# browser = None

'''all_max': 64461, 'all_min': 17912'''         # ask img


script3 = "return document.title"



def record_trace(browser, domain, trace_length, proxy, trace_index):
    start_time = time.time()
    try:
        # 启动 HAR 记录
        proxy.new_har(f"trace_{trace_index}")

        browser.get(domain)

        # 等待文本框出现并输入内容
        input_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#chat-input"))
        )
        input_box.click()  # 点击文本框以聚焦
        input_box.send_keys("给我一篇1500字关于勤奋主题的议论文，1500字！")  # 输入问题

        # 模拟按下回车键
        input_box.send_keys(Keys.RETURN)
    except Exception as e:
        print("domain Access error: {}".format(e))
        return None

    sleep_time = trace_length - (time.time() - start_time)
    if sleep_time > 0:
        time.sleep(sleep_time)
        #browser.refresh()
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    if "海螺AI" in x:
        har_data = proxy.har
        # 提取关键信息
        filtered_har_data = []
        for entry in har_data['log']['entries']:
            request = entry['request']
            response = entry['response']

            # 提取需要的字段并构建字典
            filtered_entry = {
                'Request URL': request.get('url'),
                'Response Status': response.get('status'),
                'Request Time': entry.get('startedDateTime'),
                'Request Method': request.get('method'),
                'Request Size': request.get('bodySize'),
                'Response Size': response.get('bodySize')
            }
            filtered_har_data.append(filtered_entry)

        return filtered_har_data
    else:
        print("Title ERROR")
        return None


def run(domain, out_path, num_runs, trace_length):
    domain_path = ""
    domain_path = domain_path + f"{domain.replace('https://', '').replace('http://', '').replace('www.', '')}"

    domain_path = domain_path + '_' + str(num_runs) + '_' + str(trace_length) + 's' + '.pkl'
    out_f_path = os.path.join(out_path, domain_path)
    if os.path.exists(out_f_path):
        print("File has already exisit !!!")
        return False

    # 启动 BrowserMob Proxy 服务器
    server_path = "D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/Second/browsermob_proxy/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
    server = Server(server_path)
    server.start()
    #proxy = server.create_proxy({"trustAllServers": True})
    proxy = server.create_proxy({'disableCache': True})

    browser = get_edge_driver(proxy)

    '''登录过程'''
    browser.get(domain)

    time.sleep(20)

    '''开始收集'''
    all_har_data = []
    i = 0
    while i < num_runs + 1:
        trace = record_trace(browser, domain, trace_length, proxy, i)
        if trace is None:
            server.stop()
            browser.quit()
            return False

        if i > 0:
            data = (trace, domain)
            all_har_data.append(data)

        if i == num_runs:
            print('*',end = '\n')
        elif i != 0:
            print('*{}'.format(i), end='')

        i += 1

    # 将所有 HAR 数据保存到一个文件中
    with open(out_f_path, "wb") as f:
        pickle.dump(all_har_data, f)

    print()
    server.stop()
    browser.quit()
    return True



def get_driver():
    driver_cls = getattr(webdriver, 'Chrome')
    chrome_opts = Options()
    chrome_opts.binary_location = os.path.join("D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/chrome_windows/Chrome-bin", "chrome.exe")
    chrome_opts.add_argument("--disable-dev-shm-usage")
    chrome_opts.add_argument("--ignore-ssl-errors")  # 关于忽略不安全页面提示
    chrome_opts.add_argument("--ignore-certificate-errors")  # 关于忽略不安全页面提示
    chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_opts.add_argument(r"user-data-dir=D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/data_chrome_default")
    # chrome_opts.page_load_strategy = "none"

    return driver_cls(options=chrome_opts, executable_path=os.path.join("D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/chrome_windows/Chrome-bin", "chromedriver.exe"))


def create_browser():
    browser = get_driver()
    browser.set_page_load_timeout(15)
    return browser

def get_edge_driver(proxy):
    driverfile_path = 'D:\\Project_of_postgraduate\\Biger-fish\\bigger-fish-main\\edgedriver\\msedgedriver.exe'
    # 创建Edge浏览器选项
    edge_opts = Options()
    #edge_opts.use_chromium = True  # 使用 Chromium 模式
    edge_opts.add_argument(f'--proxy-server={proxy.proxy}')
    #edge_opts.set_capability('acceptInsecureCerts', True)
    # 可以添加更多Edge的配置选项
    # edge_opts.add_argument("--disable-dev-shm-usage")
    # edge_opts.add_argument("--ignore-ssl-errors")
    #edge_opts.add_argument("--ignore-certificate-errors")

    service = Service(executable_path=driverfile_path)
    return webdriver.Edge(service=service, options=edge_opts)

# browser =create_browser()


# domain = ["https://www.baidu.com",     "https://www.163.com", "https://www.google.com", "https://www.douban.com"]
domain1 = ["https://hailuoai.com"]
out_path = "D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/Second/Packet_Trace"





for i in range(len(domain1)):
    print("starting collect \"{}\" trace: ".format(domain1[i]))
    success = run(domain1[i], out_path, 100, 35)
    if success:
        print("ending collect  \"{}\" trace: ".format(domain1[i]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------')
    else:
        print("Access {} ERROR break!".format(domain1[i]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------')
        # break
