from collections import defaultdict
from util.file_util import FileUtil

if __name__ == '__main__':
    domain_ip_map = FileUtil.read_json_from_file('../domain_ip_map.json')
    ip_domain_map = defaultdict(list)

    for domain, ips in domain_ip_map.items():
        for ip in ips:
            ip_domain_map[ip].append(domain)
    FileUtil.write_json_to_file(ip_domain_map, 'ip_domain_map.json')