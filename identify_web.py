
from util.file_util import FileUtil
if __name__ == '__main__':
    base_file = 'domain_map_to_domain_ip_map.json'
    capture_file = 'capture_ips.json'
    base_result = FileUtil.read_json_from_file(base_file)
    capture_result = FileUtil.read_json_from_file(capture_file)

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


    # 遍历 capture_result 中的每个条目
    for key, ips in capture_result.items():
        # 存储匹配的 entry 和命中数量
        matched_entries = []

        for entry in base_result:
            dp_ips = set(entry.get('dp_ips', []))
            ds_ips = set(entry.get('ds_ips', []))
            # 检查 dp_ips 是否包含 capture_result 中的任何 IP 地址
            matched_dp_ips = set(ips) & dp_ips
            if matched_dp_ips:
                # 如果匹配到 dp_ips，将 entry 添加到结果中
                matched_entry = {
                    'entry': entry,
                    'hit_count': 0
                }
                matched_entries.append(matched_entry)

                # 移除已经匹配的 IP 地址
                # unmatched_ips -= matched_dp_ips


                # 检查 ds_ips 是否包含剩余的未匹配 IP 地址
                matched_ds_ips = set(ips) & ds_ips
                matched_entry['hit_count'] = len(matched_ds_ips)
        print("-------------" + "域名" + key)
        print(f"长度：{len(matched_entries)}")
        for matched_entry in matched_entries:
            print(f"Entry: {matched_entry['entry']['dp']}")
            print(f"DP IPs: {matched_entry['entry']['dp_ips']}")
            print(f"DS IPs: {matched_entry['entry']['ds_ips']}")
            print(f"Hit Count: {matched_entry['hit_count']}")
            print("-" * 40)  # 分隔线

