import math
from collections import defaultdict
from util.file_util import FileUtil
if __name__ == '__main__':
    data = FileUtil.read_json_from_file('new_all_domain_to_domain_map.json')
    # 统计每个主域名和子域名的出现次数
    main_domain_counts = defaultdict(int)
    subdomain_counts = defaultdict(int)
    total_main_domains = 0
    total_subdomains = 0

    for main_domain, subdomains in data.items():
        main_domain_counts[main_domain] += 1
        total_main_domains += 1
        for subdomain in subdomains:
            subdomain_counts[subdomain] += 1
            total_subdomains += 1

    # 计算每个主域名和子域名的概率
    main_domain_probabilities = {main_domain: count / total_main_domains for main_domain, count in
                                 main_domain_counts.items()}
    subdomain_probabilities = {subdomain: count / total_main_domains for subdomain, count in subdomain_counts.items()}


    # 计算信息熵
    def calculate_entropy(probability):
        if probability == 0:
            return 0
        return -math.log2(probability)


    # 计算主域名的信息熵
    main_domain_entropies = {main_domain: calculate_entropy(prob) for main_domain, prob in
                             main_domain_probabilities.items()}

    # 计算子域名的信息熵
    subdomain_entropies = {subdomain: calculate_entropy(prob) for subdomain, prob in subdomain_probabilities.items()}

    # 打印结果
    print("Main Domain Entropies:")
    for main_domain, entropy in sorted(main_domain_entropies.items(), key=lambda x: x[1], reverse=True):
        print(f"Main Domain: {main_domain}, Entropy: {entropy:.4f}")

    print("\nSubdomain Entropies:")
    for subdomain, entropy in sorted(subdomain_entropies.items(), key=lambda x: x[1], reverse=True):
        print(f"Subdomain: {subdomain}, Entropy: {entropy:.4f}")
    # 合并主域名和子域名的信息熵
    all_entropies = {**main_domain_entropies, **subdomain_entropies}

    # 将结果写入文件
    output_file = 'all_domain_entropies.json'
    FileUtil.write_json_to_file(all_entropies, output_file)