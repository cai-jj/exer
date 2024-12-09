from collections import Counter
from util.file_util import FileUtil

# 获取域名对应的IP地址，一个域名对应多个IP

def remove_common_values(domain_map):
    # 收集所有value中的元素到一个列表中
    all_values = [item for sublist in domain_map.values() for item in sublist]

    # 计算每个元素出现的次数
    value_counts = Counter(all_values)

    # 获取domain_map的长度
    map_length = len(domain_map)

    # 确定哪些值需要被删除（即出现次数等于map长度的）
    to_remove = {value for value, count in value_counts.items() if count == map_length}

    # 从domain_map的每个value列表中移除这些值
    for key in domain_map:
        domain_map[key] = [v for v in domain_map[key] if v not in to_remove]

    return domain_map

def critical_rendering_paths():
    domain_map = FileUtil.read_json_from_file('critical_rendering_path_domain.json')
    # domain_ip_map = FileUtil.read_json_from_file('domain_ip_map.json')
    domain_ip_map = FileUtil.read_json_from_file('new_domain_ip_map.json')
    result = []
    for item in domain_map:
        dp = item["domain"]
        dp_ips = domain_ip_map[dp]
        ds1_list = item["dom_loading_resources_domains"]
        ds1_ips = set()
        for ds1 in ds1_list:
            if ds1:
                ips = domain_ip_map[ds1]
                ds1_ips.update(ips)
        ds2_list = item["dom_content_loaded_resources_domains"]
        ds2_ips = set()
        for ds2 in ds2_list:
            if ds2:
                ips = domain_ip_map[ds2]
                ds2_ips.update(ips)
        ds3_list = item["dom_complete_resources_domains"]
        ds3_ips = set()
        for ds3 in ds3_list:
            if ds3:
                ips = domain_ip_map[ds3]
                ds3_ips.update(ips)
        result.append({
            "dp": dp,
            "dp_ips": dp_ips,
            "ds1": ds1_list,
            "ds1_ips": list(ds1_ips),
            "ds2": ds2_list,
            "ds2_ips": list(ds2_ips),
            "ds3": ds3_list,
            "ds3_ips": list(ds3_ips),
        })
    print(result)
    # FileUtil.write_json_to_file(result, 'critical_rendering_path_domain_map_to_domain_ip_map.json')
    FileUtil.write_json_to_file(result, 'new_critical_rendering_path_domain_map_to_domain_ip_map.json')


if __name__ == '__main__':
    result = []
    outfile = 'domain_to_domain_map.json'
    temp_domain_map = FileUtil.read_json_from_file(outfile)

    domain_map = remove_common_values(temp_domain_map)

    print("origin map length: ", len(temp_domain_map))
    for key, value in temp_domain_map.items():
        print(f"key: {key}, value: {value}")
    print("new map length: ", len(domain_map))
    for key, value in domain_map.items():
        print(f"key: {key}, value: {value}")
    # domain_ip_map = FileUtil.read_json_from_file('domain_ip_map.json')
    domain_ip_map = FileUtil.read_json_from_file('new_domain_ip_map.json')
    for key, values in domain_map.items():
        dp_ips = domain_ip_map[key]
        print(f"The IP addresses for {key} are: {dp_ips}")
        ds_ips = set()
        for v in values:
            iplist = domain_ip_map[v]
            print(f"The IP addresses for {v} are: {iplist}")
            ds_ips.update(iplist)
        result.append({
            "dp": key,
            "dp_ips": dp_ips,
            "ds": values,
            "ds_ips": list(ds_ips)
        })
    # outfile = 'domain_map_to_domain_ip_map.json'
    outfile = 'new_domain_map_to_domain_ip_map.json'
    FileUtil.write_json_to_file(result, outfile)

    critical_rendering_paths()



