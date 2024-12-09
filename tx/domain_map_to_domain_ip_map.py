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
    outfile = 'new_domain_map_to_domain_ip_map.json'
    FileUtil.write_json_to_file(result, outfile)



