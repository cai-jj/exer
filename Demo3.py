import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess
import json
from util.file_util import FileUtil

TSHARK_PATH = r'C:\Program Files\Wireshark\tshark.exe'
def start_tshark(output_file):

    # 构建捕获过滤器
    capture_filter = 'port 80 or port 443'
    # 启动 tshark，指定输出文件和捕获过滤器
    # en0网卡配置一下

    tshark_process = subprocess.Popen(
        [TSHARK_PATH, '-i', 'WLAN', '-f', capture_filter, '-w', output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return tshark_process

def stop_tshark(tshark_process):
    tshark_process.terminate()
    tshark_process.communicate()
    print(f'Tshark stopped and data saved to {output_file}')

def clear_browser_cache(driver):
    # 清除浏览器缓存
    driver.execute_cdp_cmd("Network.clearBrowserCache", {})
    driver.execute_cdp_cmd("Network.clearBrowserCookies", {})

    # 清除浏览数据
    driver.execute_cdp_cmd("Storage.clearDataForOrigin", {"origin": "*", "storageTypes": "all"})

def extract_ips_from_pcap(pcap_file):

    result = subprocess.run([TSHARK_PATH, '-r', pcap_file, '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst'],
                            capture_output=True, text=True)
    # 将每行的IP地址对转换为元组，并去除空值
    ip_pairs = [tuple(line.split()) for line in result.stdout.splitlines() if line.strip()]

    # 将所有IP地址放入一个集合中，自动去重
    all_ips = set()
    for src_ip, dst_ip in ip_pairs:
        all_ips.add(src_ip)
        all_ips.add(dst_ip)

    # 将集合转换为列表
    unique_ips = list(all_ips)

    return unique_ips

def visit_website(url, output_file):
    # 设置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不打开浏览器窗口
    chrome_options.add_argument('--disable-gpu')

    # 指定 ChromeDriver 的路径
    service = Service('C:\\Users\\old driver\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe')  # 替换为你的 chromedriver 路径

    # 创建 WebDriver 对象
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 启动 tshark
        tshark_process = start_tshark(output_file)
        # 打开网页
        driver.get(url)
        print(f'Visited {url}')

        # 停留 5 秒
        time.sleep(5)

        # 停止 tshark
        stop_tshark(tshark_process)
    except Exception as e:
        print(f'Error visiting {url}: {e}')
    finally:
        clear_browser_cache(driver)
        # 关闭浏览器
        driver.quit()



if __name__ == '__main__':
    # 访问网站，打开Wireshark抓取对应的IP地址
    urls = FileUtil.read_list_from_file('web.txt')
    capture_ip_map = {}
    for i, url in enumerate(urls):
        output_file = f'output_{i}.pcap'
        visit_website("https://www."+ url, output_file)
        ips = extract_ips_from_pcap(output_file)
        capture_ip_map[url] = ips
        file_path = f'output_{i}.pcap'
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print(f"Warning: File {file_path} does not exist and cannot be removed.")
        except Exception as e:
            print(f'{e}')
    output_file = 'capture_ips.json'
    FileUtil.write_json_to_file(capture_ip_map, output_file)
    read_kv_pairs = FileUtil.read_json_from_file(output_file)
    print(read_kv_pairs)


