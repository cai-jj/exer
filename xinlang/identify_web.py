import re
import random

from util.file_util import FileUtil

def process_url(url):
    # 使用正则表达式匹配并替换掉http(s)://前缀
    return re.sub(r'^https?://', '', url)

if __name__ == '__main__':

    domain_map = FileUtil.read_json_from_file('domain_to_domain_map.json')
    base_result = FileUtil.read_json_from_file('domain_map_to_domain_ip_map.json')
    domain_ip_map = FileUtil.read_json_from_file('domain_ip_map.json')

    capture_result = {}
    for key, value in domain_map.items():
        capture_list = []
        dp_ips = domain_ip_map[key]
        dp_random_element = random.choice(dp_ips)
        capture_list.append(dp_random_element)
        for domain in value:
            ds_ips = domain_ip_map[domain]
            ds_random_element = random.choice(dp_ips)
            capture_list.append(ds_random_element)
        capture_result[key] = capture_list
    print("capture result:")
    for key, value in capture_result.items():
        print(f"key: {key}, value: {value}")
    FileUtil.write_json_to_file(capture_result, 'capture_result.json')
    ip_entropy = FileUtil.read_json_from_file('ip_entropies.json')
    # for entry in base_result:
    #     dp = entry.get('dp', 'N/A')
    #     dp_ips = entry.get('dp_ips', [])
    #     ds = entry.get('ds', [])
    #     ds_ips = entry.get('ds_ips', [])
    #     print(f"Domain: {dp}")
    #     print(f"DP IPs: {dp_ips}")
    #     print(f"Subdomains: {ds}")
    #     print(f"DS IPs: {ds_ips}")
    #     print("-" * 40)  # 分隔线

    counter = 0
    true_domains = []
    false_domains = []
    # 遍历 capture_result 中的每个条目
    for key, ips in capture_result.items():
        # 存储匹配的 entry 和命中数量
        matched_entries = []
        for entry in base_result:
            dp_ips = entry.get('dp_ips', [])
            ds_ips = entry.get('ds_ips', [])
            # 检查 dp_ips 是否包含 capture_result 中的任何 IP 地址
            ip = ips[0]
            if ip in dp_ips:
                # 如果匹配到 dp_ips，将 entry 添加到结果中
                matched_entry = {
                    'entry': entry,
                    'hit_count': 0
                }
                matched_entries.append(matched_entry)
                # 移除已经匹配的 IP 地址
                tmp_ips = list(ips)
                tmp_ips.remove(ip)
                # 检查 ds_ips 是否包含剩余的未匹配 IP 地址
                sum_entropies = ip_entropy[ip]
                matched_entry['hit_ipList'] = []
                for tmp_ip in tmp_ips:
                    if tmp_ip in ds_ips:
                        matched_entry['hit_count'] += 1
                        matched_entry['hit_ipList'].append(tmp_ip)
                        sum_entropies += ip_entropy[tmp_ip]
                matched_entry['sum_entropies'] = sum_entropies
        print(f"初始域名为：{key}")
        print(f"命中主域名的个数：{len(matched_entries)}")
        max_value = 0
        dp = None
        for matched_entry in matched_entries:
            print(f"Entry: {matched_entry['entry']['dp']}")
            print(f"DP IPs: {matched_entry['entry']['dp_ips']}")
            print(f"DS IPs: {matched_entry['entry']['ds_ips']}")
            print(f"Hit Count: {matched_entry['hit_count']}")
            print(f"hit_ipList: {matched_entry['hit_ipList']}")
            print(f"sum_entropies: {matched_entry['sum_entropies']}")
            print("-" * 40)  # 分隔线
            if max_value != None and max_value < matched_entry['sum_entropies']:
                max_value = matched_entry['sum_entropies']
                dp = matched_entry['entry']['dp']
            else:
                max_value = matched_entry['sum_entropies']
                dp = matched_entry['entry']['dp']
        max_count = 0
        for matched_entry in matched_entries:
            if max_value == matched_entry['sum_entropies']: max_count += 1
        url = process_url(key)
        print(f"orgin domain: {url}, predict domain: {dp}, 最大熵值个数: {max_count}")
        if url == dp:
            true_domains.append((key, url))
            counter += 1
        else: false_domains.append((key, url))
    print(f"counter: {counter}, len: {len(capture_result)}, 识别率：{counter/len(capture_result)}")
    print(f"true_domains: {true_domains}")
    print(f"false_domains: {false_domains}")


