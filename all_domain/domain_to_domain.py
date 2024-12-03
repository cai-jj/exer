import json
import re
import time
import requests
from bs4 import BeautifulSoup
import socket
import urllib.parse
from util.file_util import FileUtil
# 获取网页托管的域名
def get_domains_from_url(url, headers=None):

    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    try:
        # 步骤 1: 获取网页内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        html_content = response.text

        # 步骤 2: 解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 步骤 3: 提取所有带有 src 或 href 属性的标签
        resources = []
        for tag in soup.find_all(True):
            if tag.name == 'link' and 'href' in tag.attrs:
                resources.append(tag['href'])
            elif tag.name in ['img', 'script', 'iframe', 'video', 'audio', 'source', 'track', 'object',
                              'embed'] and 'src' in tag.attrs:
                resources.append(tag['src'])

        # 步骤 4: 提取域名
        domains = set()
        for resource in resources:
            try:
                parsed_url = urllib.parse.urlparse(resource)
                domain = parsed_url.netloc
                if domain:
                    domains.add(domain)
            except Exception as e:
                print(f"Error parsing URL {resource}: {e}")

        return domains
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return set()


if __name__ == '__main__':
    outfile = 'domains.txt'
    domains = FileUtil.read_list_from_file(outfile)
    domain_map = {}
    for domain in domains:
        domains = get_domains_from_url("https://" + domain)
        url = domain
        if url in domains:
            domains.remove(url)
        domain_list = list(domains)
        domain_map[url] = domain_list
    outfile = 'domain_to_domain_map.json'
    FileUtil.write_json_to_file(domain_map,outfile)
