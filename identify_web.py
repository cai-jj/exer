import re
import random

from util.file_util import FileUtil

def process_url(url):
    # 使用正则表达式匹配并替换掉http(s)://前缀
    return re.sub(r'^https?://', '', url)

if __name__ == '__main__':

    domain_map = FileUtil.read_json_from_file('new_all_domain_to_domain_map.json')
    base_file = 'all_domain_map_to_domain_ip_map.json'
    base_result = FileUtil.read_json_from_file(base_file)
    domain_ip_map = FileUtil.read_json_from_file('new_all_domain_ip_map.json')
    # capture_file = 'capture_ips.json'
    # capture_result = FileUtil.read_json_from_file(capture_file)
    capture_result = {}
    for key, value in domain_map.items():
        capture_list = []
        dp_ips = domain_ip_map[key]
        if len(dp_ips) == 0: continue
        dp_random_element = random.choice(dp_ips)
        capture_list.append(dp_random_element)
        for domain in value:
            ds_ips = domain_ip_map[domain]
            ds_random_element = random.choice(dp_ips)
            if ds_random_element not in capture_list:
                capture_list.append(ds_random_element)
        capture_result[key] = capture_list
    print("capture result:")
    for key, value in capture_result.items():
        print(f"key: {key}, value: {value}")
    ip_entropy = FileUtil.read_json_from_file('all_ip_entropies.json')
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
    # 遍历 capture_result 中的每个条目
    for key, ips in capture_result.items():
        # 存储匹配的 entry 和命中数量
        matched_entries = []

        for entry in base_result:
            dp_ips = set(entry.get('dp_ips', []))
            ds_ips = set(entry.get('ds_ips', []))
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
                tmp_ips = set(ips)
                tmp_ips.remove(ip)
                # 检查 ds_ips 是否包含剩余的未匹配 IP 地址
                matched_ds_ips = tmp_ips & ds_ips
                total = ip_entropy[ip]
                for dp_ip in matched_ds_ips:
                    total += ip_entropy[dp_ip]
                matched_entry['hit_count'] = len(matched_ds_ips)
                matched_entry['total'] = total
        print("-------------" + "域名" + key)
        print(f"长度：{len(matched_entries)}")
        max = 0
        dp = None
        for matched_entry in matched_entries:
            print(f"Entry: {matched_entry['entry']['dp']}")
            print(f"DP IPs: {matched_entry['entry']['dp_ips']}")
            print(f"DS IPs: {matched_entry['entry']['ds_ips']}")
            print(f"Hit Count: {matched_entry['hit_count']}")
            print(f"total: {matched_entry['total']}")
            print("-" * 40)  # 分隔线
            if max != None and max < matched_entry['total']:
                max = matched_entry['total']
                dp = matched_entry['entry']['dp']
            else:
                max = matched_entry['total']
                dp = matched_entry['entry']['dp']
        print("-------------" + "域名" + process_url(key))
        print(f"predict 域名: {dp}")
        if process_url(key) == dp: counter += 1
    print(f"counter: {counter}, len: {len(capture_result)}, 识别率：{counter/len(capture_result)}")


