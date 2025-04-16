import math
import threading
import time
import os
import pickle
import queue
from selenium import webdriver
from selenium.webdriver.edge.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from browsermobproxy import Server
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
script3 = "return document.title"
# def get_driver():
#     driver_cls = getattr(webdriver, 'Chrome')
#     chrome_opts = Options()
#     chrome_opts.binary_location = os.path.join("D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/chrome_windows/Chrome-bin", "chrome.exe")
#     chrome_opts.add_argument("--disable-dev-shm-usage")
#     chrome_opts.add_argument("--ignore-ssl-errors")  #
#     chrome_opts.add_argument("--ignore-certificate-errors")  #
#     chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_opts.add_argument(r"user-data-dir=D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/data_chrome_default")
#     # chrome_opts.page_load_strategy = "none"
#
#     return driver_cls(options=chrome_opts, executable_path=os.path.join("D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/chrome_windows/Chrome-bin", "chromedriver.exe"))

def get_edge_driver():
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    # 屏蔽inforbar
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])

    driverfile_path = 'D:\\Project_of_postgraduate\\Biger-fish\\bigger-fish-main\\edgedriver\\msedgedriver.exe'
    service = Service(executable_path=driverfile_path)
    #return webdriver.Edge(service=service,options=edge_options)
    return webdriver.Edge(service=service)


# def create_browser():
#     browser = get_driver()
#     browser.set_page_load_timeout(15)
#     return browser

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

'''访问 yiyan.baidu.com'''
def pure_visit1(domain,trace_length):
    #browser = create_browser()
    browser = get_edge_driver()
    start_time = time.time()
    browser.get(domain)
    # try:
    #     browser.get(domain)
    #

    #     '''首次打开登陆注册'''
    #     page_source = browser.page_source
    #     # 点击“立即登录”按钮
    #     login_button = WebDriverWait(browser, 10).until(
    #         EC.element_to_be_clickable((By.CLASS_NAME, "lpzMgwiN.LBFhiHLz"))
    #     )
    #     login_button.click()
    #
    #     # 等待登录框出现
    #     login_frame = WebDriverWait(browser, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="passport-login-pop"]'))
    #     )
    #     # 切换到“账号登录”选项
    #     account_login_tab = WebDriverWait(login_frame, 10).until(
    #         EC.element_to_be_clickable((By.ID, "TANGRAM__PSP_11__changePwdCodeItem"))
    #     )
    #     account_login_tab.click()
    #
    #     # 输入用户名
    #     username_input = WebDriverWait(login_frame, 10).until(
    #         EC.presence_of_element_located((By.ID, "TANGRAM__PSP_11__userName"))
    #     )
    #     username_input.send_keys("18200269880")
    #
    #     # 输入密码
    #     password_input = WebDriverWait(login_frame, 10).until(
    #         EC.presence_of_element_located((By.ID, "TANGRAM__PSP_11__password"))
    #     )
    #     password_input.send_keys("qwer130....")
    #
    #     # 勾选“阅读并接受”复选框
    #     checkbox = WebDriverWait(login_frame, 10).until(
    #         EC.element_to_be_clickable((By.ID, "TANGRAM__PSP_11__isAgree"))
    #     )
    #     if not checkbox.is_selected():
    #         checkbox.click()
    #
    #     # 确保登录按钮启用（如果按钮被禁用，则用JavaScript强制启用）
    #     submit_button = WebDriverWait(login_frame, 10).until(
    #         EC.element_to_be_clickable((By.ID, "TANGRAM__PSP_11__submit"))
    #     )
    #     browser.execute_script("arguments[0].removeAttribute('disabled');", submit_button)
    #
    #     # 点击登录按钮
    #     submit_button.click()
    # except Exception as e:
    #     # Called when Selenium stops loading after the length of the trace
    #     print("domain Access error: {}".format(e))
    #     browser.quit()
    #     return None
    time.sleep(60)
    # sleep_time = trace_length - (time.time() - start_time)
    # if sleep_time > 0:
    #     time.sleep(sleep_time)


    '''第二次访问'''
    browser.get(domain)
    # 等待并找到可编辑的文本框
    text_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.yc-editor[contenteditable='true']"))
    )

    # 点击文本框并输入内容
    text_box.click()  # 激活文本框
    text_box.send_keys("你好")
    time.sleep(1)
    # 等待并找到发送按钮
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "sendBtn"))
    )

    # 点击发送按钮
    send_button.click()
    time.sleep(trace_length)

    '''第三次访问'''
    browser.get(domain)
    # 等待并找到可编辑的文本框
    text_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.yc-editor[contenteditable='true']"))
    )

    # 点击文本框并输入内容
    text_box.click()  # 激活文本框
    text_box.send_keys("你好")
    time.sleep(1)
    # 等待并找到发送按钮
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "sendBtn"))
    )

    # 点击发送按钮
    send_button.click()
    time.sleep(trace_length)

'''访问https://www.doubao.com'''
def pure_visit2(domain,trace_length):
    browser = get_edge_driver()
    start_time = time.time()
    browser.get(domain)
    ''' 登录 '''
    # 点击登录按钮
    login_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="to_login_button"]'))
    )
    login_button.click()

    # 输入手机号
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="login_phone_number_input"]'))
    )
    phone_input.send_keys("18200269880")

    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    if "豆包" in x:
        print("HAVE")

    time.sleep(40)


    ''' 文本框发送数据 '''
    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.semi-input-textarea"))
    )
    # 确保文本框获得焦点，然后输入 "你好"
    input_box.click()  # 点击文本框以确保其获得焦点
    input_box.send_keys("你好")
    # 等待发送按钮可点击
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "flow-end-msg-send"))
    )
    # 点击发送按钮
    send_button.click()
    end_time = time.time()
    time.sleep(20-(end_time-start_time))

    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)

    ''' 文本框发送数据 '''
    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.semi-input-textarea"))
    )
    # 确保文本框获得焦点，然后输入 "你好"
    input_box.click()  # 点击文本框以确保其获得焦点
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")
    # 等待发送按钮可点击
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "flow-end-msg-send"))
    )
    # 点击发送按钮
    send_button.click()

    end_time = time.time()
    time.sleep(20 - (end_time - start_time))

    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
def pure_visit3(domain,trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(30)


    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.scroll-display-none"))
    )
    # 点击文本框以确保其获得焦点
    input_box.click()
    # 输入 "为我生成一张高清晰度的包含各种动物的森林图片"
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")

    # 等待发送按钮可点击
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.enter > img.enter_icon"))
    )
    # 点击发送按钮
    send_button.click()

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)

    start_time = time.time()
    browser.get(domain)

    # 等待文本框出现
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.scroll-display-none"))
    )
    # 点击文本框以确保其获得焦点
    input_box.click()
    # 输入 "为我生成一张高清晰度的包含各种动物的森林图片"
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")

    # 等待发送按钮可点击
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.enter > img.enter_icon"))
    )
    # 点击发送按钮
    send_button.click()

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)            #智谱清言

def pure_visit4(domain,trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(60)

    start_time = time.time()
    browser.get("https://taichu-web.ia.ac.cn/#/chat")  # 替换为实际网址

    # 等待文本框出现并输入文本
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.metahuman-input"))
    )
    input_box.click()
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")

    # 确保发送按钮变为可点击状态
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., '发送')]"))
    )
    send_button.click()

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit5(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(60)

def pure_visit6(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(60)


    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ant-input.textarea--g7EUvnQR"))
    )
    input_box.click()
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")
    # 确保按钮变为可点击状态，然后点击按钮
    send_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.anticon"))
    )
    send_button.click()

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit7(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(60)

    start_time = time.time()
    browser.get(domain)

    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
    )
    input_box.click()
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")

    # 模拟按下回车键发送
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit8(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(40)

    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ant-input.QuestionInput_v2_textArea__0l2ER"))
    )
    input_box.click()
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")

    # 模拟点击回车键
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit9(domain, trace_length):
    browser = create_browser()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(1000)

    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ant-input.QuestionInput_v2_textArea__0l2ER"))
    )
    input_box.click()
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")

    # 模拟点击回车键
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit10(domain, trace_length):
    # 启动 BrowserMob Proxy 服务器
    server_path = "D:/Project_of_postgraduate/Biger-fish/bigger-fish-main/Second/browsermob_proxy/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
    server = Server(server_path)
    server.start()
    # proxy = server.create_proxy({"trustAllServers": True})
    proxy = server.create_proxy({'disableCache': True})

    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(15)

    start_time = time.time()
    # 启动 HAR 记录
    proxy.new_har(f"trace_{1}")
    browser.get(domain)
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

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

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
                'Request Size': request.get('bodySize'),
                'Response Size': response.get('bodySize')
            }
            filtered_har_data.append(filtered_entry)

        return filtered_har_data
    else:
        print("Title ERROR")
        return None

def pure_visit11(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(30)

    start_time = time.time()
    browser.get(domain)

    # 检查“停止”按钮是否存在并可点击
    try:
        stop_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button']._89d4d19._4d9058c"))
        )
        stop_button.click()  # 点击停止按钮
        print("已点击停止按钮")
    except Exception as e:
        print("停止按钮不可点击或不存在:", e)

    # 等待并点击控件（使用 SVG 元素的 viewBox 属性）
    control = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[viewBox='0 0 17.7415 17.7415']"))
    )
    control.click()  # 点击控件

    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#chat-input"))
    )
    input_box.click()  # 点击文本框以聚焦
    input_box.send_keys("给我一篇1500字关于勤奋主题的议论文，1500字！")

    # 模拟按下回车键
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit12(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(20)

    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.agent-dialogue__content--common__input-box .ql-editor"))
    )
    input_box.click()  # 点击文本框以聚焦
    input_box.send_keys("给我一篇1500字关于勤奋主题的议论文，1500字！")  # 输入问题

    # 模拟按下回车键
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

def pure_visit13(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(20)

    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#chat-input"))
    )
    input_box.click()  # 点击文本框以聚焦
    input_box.send_keys("给我一篇1500字关于勤奋主题的议论文，1500字！")  # 输入问题

    # 模拟按下回车键
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))


def pure_visit14(domain, trace_length):
    browser = get_edge_driver()
    browser.get(domain)
    ''' 登录 '''
    handles = browser.window_handles
    browser.switch_to.window(handles[0])
    x = browser.execute_script(script3)
    print(x)
    time.sleep(20)

    start_time = time.time()
    browser.get(domain)
    # 等待文本框出现并输入内容
    input_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "prompt-text-editor"))
    )
    input_box.click()  # 点击文本框以聚焦
    input_box.send_keys("为我生成一张高清晰度的包含各种动物的森林图片")  # 输入问题

    # 模拟按下回车键
    input_box.send_keys(Keys.RETURN)

    end_time = time.time()
    time.sleep(trace_length - (end_time - start_time))

domain2 = ["https://www.doubao.com"]
domain1 = ["https://yiyan.baidu.com"]
domain3 = ["https://chatglm.cn"]
domain4 = ["https://taichu-web.ia.ac.cn/#/login"]
domain5 = ["https://yiyan.baidu.com"]
domain6 = ["https://tongyi.aliyun.com/qianwen"]
domain7 = ["https://chat.360.com/chat"]
domain8 = ["https://chat.sensetime.com"]
domain9 = ["https://gemini.google.com/app"]         #谷歌登录不允许自动工具
domain10 = ["https://kimi.moonshot.cn/"]            #扫码 word
domain11 = ["https://chat.deepseek.com/"]           #输密码 word   可能存在上一个未完成，所以拉长时间到50
domain12 = ["https://yuanbao.tencent.com/"]         #扫码 word img
domain13 = ["https://hailuoai.com/"]                # word 可能存在上一个未完成，所以拉长时间到35
domain14 = ["https://jimeng.jianying.com/ai-tool/image/generate"]   #纯图片生成， 有生成次数限制，考虑充值？ 抖音扫码



filter_data = []
"https://taichu-web.ia.ac.cn/#/chat"
for i in range(len(domain10)):
    filter_data = pure_visit10(domain10[i],25)
print(filter_data)

# brower = get_edge_driver()
# brower.get("https://chat.360.com/chat")
# time.sleep(60)

# driver = webdriver.Chrome()
# driver.get("https://yiyan.baidu.com")

