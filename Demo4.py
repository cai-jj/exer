import requests
from bs4 import BeautifulSoup
import dns.resolver
from urllib.parse import urlparse, urljoin


def resolve_to_ip(host):
    """解析主机名到IP地址"""
    try:
        # 使用dnspython进行DNS查询
        answers = dns.resolver.resolve(host, 'A')
        return [answer.address for answer in answers]
    except Exception as e:
        print(f"Failed to resolve {host}: {e}")
        return []


def get_resources(url):
    """获取页面中的资源链接，并按阶段分类"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    resources = {
        'domLoading': [],
        'domContentLoaded': [],
        'domComplete': []
    }

    # domLoading: 阻塞DOM构建的CSS和JavaScript
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href and (href.startswith('http') or href.startswith('//')):
            resources['domLoading'].append(urljoin(base_url, href))

    for script in soup.find_all('script'):
        src = script.get('src')
        if src and (src.startswith('http') or src.startswith('//')):
            if not script.has_attr('async') and not script.has_attr('defer'):
                resources['domLoading'].append(urljoin(base_url, src))
            else:
                resources['domContentLoaded'].append(urljoin(base_url, src))

    # domContentLoaded: 非阻塞的CSS和JavaScript
    # 这里我们假设所有非阻塞的脚本都带有async或defer属性
    # 如果没有特别指定，通常认为是阻塞的

    # domComplete: 图像和其他子资源
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and (src.startswith('http') or src.startswith('//')):
            resources['domComplete'].append(urljoin(base_url, src))

    for iframe in soup.find_all('iframe'):
        src = iframe.get('src')
        if src and (src.startswith('http') or src.startswith('//')):
            resources['domComplete'].append(urljoin(base_url, src))

    return resources


def main(url):
    resources = get_resources(url)

    for event, urls in resources.items():
        print(f"\n{event} Resources:")
        for url in urls:
            parsed_url = urlparse(url)
            host = parsed_url.netloc
            ips = resolve_to_ip(host)
            if ips:
                print(f"  - URL: {url} -> IPs: {', '.join(ips)}")
            else:
                print(f"  - URL: {url} -> No IP found")


if __name__ == "__main__":
    target_url = 'https://www.163.com'  # 替换为你要分析的实际URL
    main(target_url)