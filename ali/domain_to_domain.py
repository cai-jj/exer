import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
from util.file_util import FileUtil
from urllib.parse import urlparse
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
def process_url(url):
    return re.sub(r'^https?://', '', url)

def get_critical_rendering_path_resources(url, headers=None):
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    """
    获取指定网页在关键渲染路径不同阶段的资源列表对应的域名

    参数:
    url (str): 要爬取的网页的URL地址

    返回:
    tuple: 包含三个列表的元组，分别对应domLoading、domContentLoaded、domComplete阶段的资源域名列表，若请求出现异常则对应列表为空
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 若请求状态码不是200等正常状态，抛出异常
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        dom_loading_resources_domains = []
        dom_content_loaded_resources_domains = []
        dom_complete_resources_domains = []

        # domLoading阶段资源域名获取
        for link in soup.find_all('link'):
            if 'href' in link.attrs:
                parsed_url = urlparse(link['href'])
                domain = parsed_url.netloc
                dom_loading_resources_domains.append(domain)
        for script in soup.find_all('script'):
            if'src' in script.attrs:
                parsed_url = urlparse(script['src'])
                domain = parsed_url.netloc
                dom_loading_resources_domains.append(domain)

        # domContentLoaded阶段资源域名获取
        for img in soup.find_all('img'):
            if'src' in img.attrs:
                parsed_url = urlparse(img['src'])
                domain = parsed_url.netloc
                dom_content_loaded_resources_domains.append(domain)

        # domComplete阶段资源域名获取
        scripts = soup.find_all('script', attrs={'src': True})
        for script in scripts:
            parsed_url = urlparse(script['src'])
            domain = parsed_url.netloc
            dom_complete_resources_domains.append(domain)

        return set(dom_loading_resources_domains), set(dom_content_loaded_resources_domains), set(dom_complete_resources_domains)
    except requests.RequestException as e:
        print(f"请求出现异常: {e}")
        return [], [], []

if __name__ == '__main__':
    outfile = 'domain.txt'
    domains = FileUtil.read_list_from_file(outfile)
    domain_map = {}
    for domain in domains:
        domains = get_domains_from_url(domain)
        url = process_url(domain)
        if url in domains:
            domains.remove(url)
        domain_list = list(domains)
        domain_map[url] = domain_list
    outfile = 'domain_to_domain_map.json'
    FileUtil.write_json_to_file(domain_map, outfile)
    outfile = 'domain.txt'
    critical_domains = FileUtil.read_list_from_file(outfile)
    result = []
    for domain in critical_domains:
        url = process_url(domain)
        dom_loading_resources_domains, dom_content_loaded_resources_domains, dom_complete_resources_domains \
            = get_critical_rendering_path_resources(domain)
        result.append({"domain": url, "dom_loading_resources_domains": list(dom_loading_resources_domains),
                       "dom_content_loaded_resources_domains": list(dom_content_loaded_resources_domains),
                       "dom_complete_resources_domains": list(dom_complete_resources_domains)})
    FileUtil.write_json_to_file(result, 'critical_rendering_path_domain.json')
    print(result)