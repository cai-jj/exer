from util.file_util import FileUtil

if __name__ == '__main__':
    domain_ip_map = FileUtil.read_json_from_file('all_domain_ip_map.json')
    print(len(domain_ip_map))
    domain_map = FileUtil.read_json_from_file('new_all_domain_to_domain_map.json' )
    domains = []
    for key, values in domain_map.items():
        if key not in domains:
            domains.append(key)
        for domain in values:
            if domain not in domains:
                domains.append(domain)
    new_domain_ip_map = {}
    for domain in domains:
        new_domain_ip_map[domain] = domain_ip_map[domain]

    print(len(new_domain_ip_map))
    print(new_domain_ip_map)
    FileUtil.write_json_to_file(new_domain_ip_map, 'new_all_domain_ip_map.json')