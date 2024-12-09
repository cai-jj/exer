import random

from util.file_util import FileUtil

if __name__ == '__main__':
    merged_groups = FileUtil.read_json_from_file('merged_groups.json')
    origin_groups = FileUtil.read_json_from_file('classify.json')
    add_domain_ip_map = {}
    for group in merged_groups:
        all_dp_ips = set()
        all_ds_ips = set()
        for item in group:
            all_dp_ips.update(item["dp_ips"])
            all_ds_ips.update(item["ds_ips"])
        for item in group:
            # 计算dp_ips的差集
            dp = item["dp"]
            ds = item["ds"]
            print(f"dp: {dp}")
            print(f"ds: {ds}")
            dp_ips_diff = list(all_dp_ips - set(item["dp_ips"]))
            for dp_ip in dp_ips_diff:
                if len(dp) < 1: break
                if dp in add_domain_ip_map.keys():
                    add_domain_ip_map[dp].append(dp_ip)
                else:
                    add_domain_ip_map[dp] = [dp_ip]
            # 计算ds_ips的差集
            ds_ips_diff = list(all_ds_ips - set(item["ds_ips"]))
            for ds_ip in ds_ips_diff:
                if len(ds) < 1: break
                d1 = random.choice(ds)
                if d1 in add_domain_ip_map.keys():
                    add_domain_ip_map[d1].append(ds_ip)
                else:
                    add_domain_ip_map[d1] = [ds_ip]
            item["dp_ips"] = list(all_dp_ips)
            item["ds_ips"] = list(all_ds_ips)
    print(add_domain_ip_map)

    domain_ip_map = FileUtil.read_json_from_file('domain_ip_map.json')
    FileUtil.write_json_to_file(add_domain_ip_map, 'add_domain_ip_map.json')

    new_domain_ip_map = {}
    for key, value in domain_ip_map.items():
        new_domain_ip_map[key] = value.copy()

    for key, value in add_domain_ip_map.items():
        if key in new_domain_ip_map:
            new_domain_ip_map[key].extend(value)
        else:
            new_domain_ip_map[key] = value.copy()
    print(new_domain_ip_map)
    FileUtil.write_json_to_file(new_domain_ip_map, 'new_domain_ip_map.json')