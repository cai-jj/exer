import time

import pyshark
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess
import json
from util.file_util import FileUtil

TSHARK_PATH = r'C:\Program Files\Wireshark\tshark.exe'
def start_tshark(output_file):
    """
    在Windows终端启动tshark进行数据包捕获，并将数据输出到指定文件。
    """
    try:
        # 构建tshark命令
        command = ["tshark", "-w", output_file, "-i", "WLAN"]
        # 使用subprocess.Popen启动tshark进程
        tshark_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return tshark_process
    except FileNotFoundError as e:
        print(f"执行tshark命令失败，可能是tshark未安装或者不在系统环境变量中，错误信息: {e}")
        return None
    except subprocess.SubprocessError as e:
        print(f"启动tshark进程出现其他错误，错误信息: {e}")
        return None

def stop_tshark(tshark_process):
    tshark_process.terminate()
    tshark_process.communicate()
    print(f'Tshark stopped and data saved to {output_file}')

def extract_ips_from_pcap(pcap_file):
    ip_set = set()  # 使用集合来存储IP地址，自动去重且查找效率高
    try:
        capture = pyshark.FileCapture(pcap_file)
        for packet in capture:
            if 'IP' in packet:
                src_ip = packet['IP'].src
                dst_ip = packet['IP'].dst
                ip_set.add(src_ip)  # 直接添加到集合中，自动去重
                ip_set.add(dst_ip)
        capture.close()
    except FileNotFoundError:
        print(f"指定的PCAP文件 {pcap_file} 不存在，请检查文件路径。")
    except Exception as e:
        print(f"解析PCAP文件时出现错误: {e}")
    return list(ip_set)  # 将集合转换为列表返回

def clear_browser_cache(driver, url):
    print("clear browser cache")
    # 清除浏览器缓存
    driver.execute_cdp_cmd("Network.clearBrowserCache", {})
    driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
    # 清除当前访问网站相关的浏览数据
    driver.execute_cdp_cmd("Storage.clearDataForOrigin", {"origin": url, "storageTypes": "all"})

def visit_website(url, output_file):
    # 设置 Chrome 选项
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式，不打开浏览器窗口
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('-incognito')  # 添加这行开启无痕模式

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
        # 清除浏览器缓存
        clear_browser_cache(driver, url)
        # 关闭浏览器
        driver.quit()



if __name__ == '__main__':
    # 访问网站，打开Wireshark抓取对应的IP地址
    urls = FileUtil.read_list_from_file('../domain.txt')
    capture_ip_map = {}
    for i, url in enumerate(urls):
        output_file = f'output_{i}.pcap'
        visit_website(url, output_file)
        ips = extract_ips_from_pcap(output_file)
        capture_ip_map[url] = ips
    output_file = '../capture_ips.json'
    FileUtil.write_json_to_file(capture_ip_map, output_file)
    read_kv_pairs = FileUtil.read_json_from_file(output_file)
    print(read_kv_pairs)

    # capture_ip_map = {}
    # output_file = 'output_1.pcap'
    # # visit_website("https://www.baidu.com", output_file)
    # ips = extract_ips_from_pcap(output_file)
    # capture_ip_map['baidu.com'] = ips
    # print(capture_ip_map)


