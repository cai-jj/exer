import re
import random

from util.file_util import FileUtil

def process_url(url):
    # 使用正则表达式匹配并替换掉http(s)://前缀
    return re.sub(r'^https?://', '', url)

def generate_ip_list(file):

    result = []
    domain_map = FileUtil.read_json_from_file('critical_rendering_path_domain.json')
    domain_ip_map = FileUtil.read_json_from_file('domain_ip_map.json')
    for item in domain_map:
        dp = item["domain"]
        dp_ips = domain_ip_map[dp]
        dp_ip = random.choice(dp_ips)
        ds1_list = item["dom_loading_resources_domains"]
        ds1_ips = []
        for ds1 in ds1_list:
            if ds1:
                ds1_ips = domain_ip_map[ds1]
                ds1_ip = random.choice(ds1_ips)
                if ds1_ip not in ds1_ips:
                    ds1_ips.append(ds1_ip)
        ds2_list = item["dom_content_loaded_resources_domains"]
        ds2_ips = []
        for ds2 in ds2_list:
            if ds2:
                ds2_ips = domain_ip_map[ds2]
                ds2_ip = random.choice(ds2_ips)
                if ds2_ip not in ds2_ips:
                    ds2_ips.append(ds2_ip)
        ds3_list = item["dom_complete_resources_domains"]
        ds3_ips = []
        for ds3 in ds3_list:
            if ds3:
                ds3_ips = domain_ip_map[ds3]
                ds3_ip = random.choice(ds3_ips)
                if ds3_ip not in ds3_ips:
                    ds3_ips.append(ds3_ip)
        result.append({"domain": dp, "dp_ip": dp_ip, "ds1_ips": ds1_ips, "ds2_ips": ds2_ips, "ds3_ips": ds3_ips})
    return result
if __name__ == '__main__':
    capture_result = generate_ip_list('critical_rendering_path_domain.json')
    print(capture_result)

    base_result = FileUtil.read_json_from_file('critical_rendering_path_domain_map_to_domain_ip_map.json')
    # domain_map = FileUtil.read_json_from_file('critical_rendering_path_domain.json')
    # base_result = FileUtil.read_json_from_file('domain_map_to_domain_ip_map.json')
    # domain_ip_map = FileUtil.read_json_from_file('domain_ip_map.json')
    #
    # capture_result = {}
    # for key, value in domain_map.items():
    #     capture_list = []
    #     dp_ips = domain_ip_map[key]
    #     dp_random_element = random.choice(dp_ips)
    #     capture_list.append(dp_random_element)
    #     for domain in value:
    #         ds_ips = domain_ip_map[domain]
    #         ds_random_element = random.choice(dp_ips)
    #         capture_list.append(ds_random_element)
    #     capture_result[key] = capture_list
    # print("capture result:")
    # for key, value in capture_result.items():
    #     print(f"key: {key}, value: {value}")
    # FileUtil.write_json_to_file(capture_result, 'capture_result.json')
    ip_entropy = FileUtil.read_json_from_file('ip_entropies.json')
    # # for entry in base_result:
    # #     dp = entry.get('dp', 'N/A')
    # #     dp_ips = entry.get('dp_ips', [])
    # #     ds = entry.get('ds', [])
    # #     ds_ips = entry.get('ds_ips', [])
    # #     print(f"Domain: {dp}")
    # #     print(f"DP IPs: {dp_ips}")
    # #     print(f"Subdomains: {ds}")
    # #     print(f"DS IPs: {ds_ips}")
    # #     print("-" * 40)  # 分隔线
    #
    counter = 0
    true_domains = []
    false_domains = []
    # 遍历 capture_result 中的每个条目
    for capture_entry in capture_result:
        # 存储匹配的 entry 和命中数量
        capture_dp = capture_entry["domain"]
        capture_dp_ip = capture_entry["dp_ip"]
        capture_ds1_ips = capture_entry["ds1_ips"]
        capture_ds2_ips = capture_entry["ds2_ips"]
        capture_ds3_ips = capture_entry["ds3_ips"]
        matched_entries = []
        for entry in base_result:
            dp_ips = entry['dp_ips']
            ds1_ips = entry['ds1_ips']
            ds2_ips = entry['ds2_ips']
            ds3_ips = entry['ds3_ips']
            # 检查 dp_ips 是否包含 capture_result 中的任何 IP 地址
            if capture_dp_ip in dp_ips:
                # 如果匹配到 dp_ips，将 entry 添加到结果中
                matched_entry = {
                    'entry': entry
                }
                matched_entries.append(matched_entry)
            sum_entropies = 0
            for ds1_ip in capture_ds1_ips:
                if ds1_ip in ds1_ips:
                    sum_entropies += ip_entropy[ds1_ip]
            for ds2_ip in capture_ds2_ips:
                if ds2_ip in ds2_ips:
                    sum_entropies += ip_entropy[ds2_ip]
            for ds3_ip in capture_ds3_ips:
                if ds3_ip in ds3_ips:
                    sum_entropies += ip_entropy[ds3_ip]
            matched_entry['sum_entropies'] = sum_entropies
        print(f"初始域名为：{capture_dp}")
        print(f"命中主域名的个数：{len(matched_entries)}")
        max_value = 0
        dp = None
        for matched_entry in matched_entries:
            print(f"Entry: {matched_entry['entry']['dp']}")
            print(f"DP IPs: {matched_entry['entry']['dp_ips']}")
            print(f"DS1: {matched_entry['entry']['ds1']}")
            print(f"DS1 IPs: {matched_entry['entry']['ds1_ips']}")
            print(f"DS2: {matched_entry['entry']['ds2']}")
            print(f"DS2 IPs: {matched_entry['entry']['ds2_ips']}")
            print(f"DS3: {matched_entry['entry']['ds3']}")
            print(f"DS3 IPs: {matched_entry['entry']['ds3_ips']}")
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

        print(f"orgin domain: {capture_dp}, predict domain: {dp}, 最大熵值个数: {max_count}")
        if capture_dp == dp:
            true_domains.append((capture_dp, dp))
            counter += 1
        else: false_domains.append((capture_dp, dp))
    print(f"counter: {counter}, len: {len(capture_result)}, 识别率：{counter/len(capture_result)}")
    print(f"true_domains: {true_domains}")
    print(f"false_domains: {false_domains}")


