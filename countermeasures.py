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

script3 = "return document.title"
invalid_request_script = """
    for (let i = 0; i < 10; i++) {
        fetch('https://kimi.moonshot.cn', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',  // 使用错误的 Content-Type
                'X-Custom-Header': 'InvalidValuexxxx'  // 添加无效的自定义头部
            },
            body: 'invalidParam=invalidValue'  // 发送不符合预期格式的请求体
        })
        .then(response => console.log('Request sent:', response))
        .catch(error => console.error('Error:', error));
    }
"""

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


def record_trace(browser, domain, trace_length, proxy, trace_index):
    start_time = time.time()
    try:
        # 启动 HAR 记录
        proxy.new_har(f"trace_{trace_index}")

        browser.get(domain)
        # 注入 JavaScript 代码
        browser.execute_script(invalid_request_script)
        # 等待文本框出现并输入内容
        input_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.editorContentEditable___FZJd9"))
        )
        input_box.click()
        input_box.send_keys("给我一篇1500字关于勤奋主题的议论文，1500字！")

        input_box.click()
        time.sleep(0.1)
        # 等待发送按钮并点击
        send_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.sendButton___gubKW"))
        )
        send_button.click()
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
    if "Kimi" in x:
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
                'Request Headers': request.get('headers'),  # 提取请求头
                'Request Size': request.get('bodySize'),
                'Response Size': response.get('bodySize')
            }
            filtered_har_data.append(filtered_entry)

        return filtered_har_data
    else:
        print("Title ERROR")
        return None



def run(domain):
    # 启动 BrowserMob Proxy 服务器
    server_path = "D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/Second/browsermob_proxy/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
    server = Server(server_path)
    server.start()
    # proxy = server.create_proxy({"trustAllServers": True})
    proxy = server.create_proxy({'disableCache': True})

    browser = get_edge_driver(proxy)

    '''登录过程'''
    browser.get(domain)

    time.sleep(15)

    trace = record_trace(browser, domain, 25, proxy, 1)

    print(trace)            //79


domain = "https://kimi.moonshot.cn"

run(domain)