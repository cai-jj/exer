from collections import defaultdict

from util.file_util import FileUtil
if __name__ == '__main__':
    # data = FileUtil.read_json_from_file('domain_ip_map.json')
    data = FileUtil.read_json_from_file('new_domain_ip_map.json')
    reversed_data = defaultdict(list)

    for domain, ips in data.items():
        for ip in ips:
            reversed_data[ip].append(domain)


    domain_entropies = FileUtil.read_json_from_file('domain_entropies.json')

    ip_entropies = {}
    for key, value in reversed_data.items():
        sum = 0
        for domain in value:
            sum += domain_entropies[domain]
        count = len(value)
        average = sum / count
        ip_entropies[key] = average
    # output_file = 'ip_entropies.json'
    output_file = 'new_ip_entropies.json'
    FileUtil.write_json_to_file(ip_entropies, output_file)
