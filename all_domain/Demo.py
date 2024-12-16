import re
import urllib

import requests
from bs4 import BeautifulSoup

from util.file_util import FileUtil
import whois
import socket
def get_domains_from_url(url, error_domains, headers=None):

    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    try:
        # 步骤 1: 获取网页内容
        response = requests.get(url, headers=headers,timeout=5)
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
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        error_domains.append(url)
        return set()
def process_url(url):
    return re.sub(r'^https?://', '', url)


def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"Error resolving IP for {domain}: {e}")
        return None

def get_network_provider(ip):
        try:
            w = whois.whois(ip)
            if 'asn' in w and 'asn_description' in w:
                return w.asn_description
            else:
                return None
        except Exception as e:
            print(f"Error querying Whois for {ip}: {e}")
            return None

def classify_domains_by_provider(domains):
    provider_dict = {}
    for domain in domains:
        ip = get_ip_address(domain)
        if ip:
            provider = get_network_provider(ip)
            if provider:
                if provider in provider_dict:
                    provider_dict[provider].append(domain)
                else:
                    provider_dict[provider] = [domain]
    return provider_dict
if __name__ == '__main__':
    domains = FileUtil.read_list_from_file("domains.txt")
    print(classify_domains_by_provider(domains))



