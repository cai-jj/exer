import itertools

from util.file_util import FileUtil
data = FileUtil.read_json_from_file('domain_map_to_domain_ip_map.json')

## 优先选择相似度高的进行合并，g1(ip) && g2(ip) / g1(ip) || g2(ip)

def classify_by_dp_ips_and_ds_ips(data):
    """
    按照dp_ips和ds_ips都相同的规则进行分类
    """
    result = []
    combined_dict = {}
    for item in data:
        dp_ips_tuple = tuple(sorted(item["dp_ips"]))
        ds_ips_tuple = tuple(sorted(item["ds_ips"]))
        combined_key = (dp_ips_tuple, ds_ips_tuple)
        if combined_key not in combined_dict:
            combined_dict[combined_key] = []
        combined_dict[combined_key].append(item)
    for combined_key, items in combined_dict.items():
        result.append(items)
    return result
def count_ds_ips_matches(lst1, lst2):
    """
    计算两个ds_ips列表中相似度
    """
    if  len(set(lst1) | set(lst2)) == 0:
        return 0
    return len(set(lst1) & set(lst2))  / len(set(lst1) | set(lst2))

# 计算两个组合并的相似度
def count_groups_matches(groups1, groups2):
    ns = 0
    for group2 in groups2:
        group2_dp_ips = tuple(sorted(group2["dp_ips"]))
        group2_ds_ips = tuple(sorted(group2["ds_ips"]))
        for group1 in groups1:
            group1_dp_ips = tuple(sorted(group1["dp_ips"]))
            group1_ds_ips = tuple(sorted(group1["ds_ips"]))
            ns = (ns +
                  count_ds_ips_matches(group1_ds_ips, group2_ds_ips) +
                  count_ds_ips_matches(group1_dp_ips, group2_dp_ips))
    return ns
def merge_groups(origin_groups, k):
    """
    根据给定的最小个数要求k合并分组
    """
    merged_groups = []
    groups = []
    for group in origin_groups:
        if len(merged_groups) >= k:
            merged_groups.append(group)
        else:
            groups.append(group)

    while groups:
        current_group = groups.pop(0)
        while len(current_group) < k:
            # 先找dp_ips相同的分组作为候选
            dp_ips_same_candidates = []
            if len(groups) == 0:
                break
            max_ns = -1
            best_group = None
            for other_group in groups:
                ns = count_groups_matches(current_group, other_group)
                if ns > max_ns:
                    best_group = other_group
                    max_ns = ns
            current_group.extend(best_group)
            groups.remove(best_group)

            # current_dp_ips = tuple(sorted(current_group[0]["dp_ips"]))  # 提取当前分组的dp_ips并处理
            # current_ds_ips = tuple(sorted(current_group[0]["ds_ips"]))  # 提取当前分组的ds_ips并处理
            #
            # for other_group in groups:
            #     other_dp_ips = tuple(sorted(other_group[0]["dp_ips"]))  # 提取其他分组的dp_ips并处理
            #     if current_dp_ips == other_dp_ips:
            #         dp_ips_same_candidates.append(other_group)
            #
            # if dp_ips_same_candidates:
            #     # 在dp_ips相同的候选分组中，找ds_ips匹配个数最多的
            #     best_candidate = max(dp_ips_same_candidates, key=lambda x: sum(
            #         [count_ds_ips_matches(x[0]["ds_ips"], current_group[0]["ds_ips"]) for _ in x]))
            #     current_group.extend(best_candidate)
            #     groups.remove(best_candidate)  # 使用remove方法移除已合并的分组
            #
            # else:
            #     # 如果没有dp_ips相同的，找ds_ips个数最多的
            #     max_ds_ips_group = \
            #     max([(len(set(itertools.chain.from_iterable([item["ds_ips"] for item in g]))), g) for g in groups if
            #          g != current_group], key=lambda x: x[0], default=(0, None))[1]
            #     if max_ds_ips_group:
            #         current_group.extend(max_ds_ips_group)
            #         groups.remove(max_ds_ips_group)
        merged_groups.append(current_group)

    # 过滤小于k的分组
    for group in merged_groups:
        if len(merged_groups) == 1: break
        if len(group) < k:
            current_group = group
            merged_groups.remove(group)
            max_ns = 0
            best_group = None
            for other_group in merged_groups:
                ns = count_groups_matches(current_group, other_group)
                if ns > max_ns:
                    best_group = other_group
                    max_ns = ns
            best_group.extend(current_group)
    return merged_groups

classified_result = classify_by_dp_ips_and_ds_ips(data)
FileUtil.write_json_to_file(classified_result, 'classify.json')
# 按照格式打印结果
origin_count = 0
new_count = 0
print("分类结果如下：")
for group_index, group in enumerate(classified_result):
    dp_ips_count = len(group)  # 统计当前dp_ips分类下的元素个数
    print(f"分类 {group_index + 1}（个数：{dp_ips_count}）:")
    for element in group:
        origin_count += 1
        print(f"    域名 (dp): {element['dp']}")
        print(f"    域名对应的IP列表 (dp_ips): {element['dp_ips']}")
        print(f"    子域名列表 (ds): {element['ds']}")
        print(f"    子域名对应的IP列表 (ds_ips): {element['ds_ips']}")
        print("    ---")

merged_groups = merge_groups(classified_result, 2)

print("分类结果如下：")
for group_index, group in enumerate(merged_groups):
    dp_ips_count = len(group)  # 统计当前dp_ips分类下的元素个数
    print(f"分类 {group_index + 1}（个数：{dp_ips_count}）:")
    for element in group:
        new_count += 1
        print(f"    域名 (dp): {element['dp']}")
        print(f"    域名对应的IP列表 (dp_ips): {element['dp_ips']}")
        print(f"    子域名列表 (ds): {element['ds']}")
        print(f"    子域名对应的IP列表 (ds_ips): {element['ds_ips']}")
        print("    ---")
FileUtil.write_json_to_file(merged_groups, "merged_groups.json")


print(f"origin_count: {origin_count}, new_count: {new_count}")