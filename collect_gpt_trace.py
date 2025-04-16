import math
import threading
import time
import os
import pickle
import queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException
# browser = None

script3 = "return document.title"
def collect_data(q,trace_length):
    data = [-1] * (trace_length * 1000)
    trace_time = time.time() * 1000

    while True:
        datum_time = time.time() * 1000
        idx = math.floor(datum_time - trace_time)

        if idx >= len(data):
            break
        num = 0
        while time.time() * 1000 - datum_time < 5:
            num += 1

        data[idx] = num
    q.put(data)

def record_trace(domain,trace_length):
    title_tables = []
    f = open("./title", "r", encoding='utf-8')
    line = f.readline()  # 读取第一行
    while line:
        # txt_data = eval(line) # 可将字符串变为元组
        line = line[:-1]
        title_tables.append(line)  # 列表增加
        line = f.readline()  # 读取下一行
    f.close()
    # if len(title_tables) == 78:
    #     # print("title_tables load successful! length = {}".format(len(title_tables)))
    #     pass
    # else:
    #     print("title_tables load failed ! Back...")
    #     return None

    browser = create_browser()
    q = queue.Queue()
    thread = threading.Thread(target=collect_data, name="record", args=[q,trace_length])
    thread.start()

    start_time = time.time()
    try:
        browser.execute_script("window.open('{}');".format(domain))
    except Exception as e:
        # Called when Selenium stops loading after the length of the trace
        print("domain Access error: {}".format(e))
        browser.quit()
        return None

    sleep_time = trace_length - (time.time() - start_time)
    if sleep_time > 0:
        time.sleep(sleep_time)

    thread.join()
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    flag_newtab = False
    flag_othersite = False
    if title_tables.count(x) != 0:
        if x == 'New Tab' or x == '新标签页':
            flag_newtab = True
        else:
            flag_othersite = True
    browser.switch_to.window(handles[1])
    x = browser.execute_script(script3)
    if title_tables.count(x) != 0:
        if x == 'New Tab' or x == '新标签页':
            flag_newtab = True
        else:
            flag_othersite = True

    if flag_newtab and flag_othersite:
        result = [q.get()]
        browser.quit()
        del browser
        if len(result[0]) == 1 and result[0][0] == -1:
            return None
        return result
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
    out_f = open(out_f_path, "wb")

    i = 0
    while i < num_runs + 1:
        trace = record_trace(domain,trace_length)

        if trace is None:
            out_f.close()
            os.remove(out_f_path)
            return False

        if i > 0:
            data = (trace, domain)

            pickle.dump(data,out_f)

        if i == num_runs:
            print('*',end = '\n')
        elif i != 0:
            print('*', end='')

        i += 1


    out_f.close()
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



# browser =create_browser()


# domain = ["https://www.baidu.com",     "https://www.163.com", "https://www.google.com", "https://www.douban.com"]
domain1 = ["https://yiyan.baidu.com"]
out_path = "D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/data"




for i in range(len(domain1)):
    print("starting collect \"{}\" trace: ".format(domain1[i]))
    success = run(domain1[i], out_path, 100, 15)
    if success:
        print("ending collect  \"{}\" trace: ".format(domain1[i]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------')
    else:

        print("Access {} ERROR break!".format(domain1[i]))
        print('--------------------------------------------------------------------------------------------------------------------------------------------------')
        # break
