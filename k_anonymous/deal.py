from util.file_util import FileUtil



if __name__ == '__main__':
    domains = set()
    domain_map = FileUtil.read_json_from_file('../domain_to_domain_map.json')
    for key, value in domain_map.items():
        domains.add(key)
        domains.update(value)
    domains_list = list(domains)
    temp_map = {}
    count = 0
    for item in domains_list:
        temp_map[item] = str(count)
        count += 1
    print(temp_map)
    FileUtil.write_json_to_file(temp_map, '../domain_to_number_map.json')
    number_domain_map = {}
    for key, value in domain_map.items():
        newKey = temp_map[key]
        value_list = []
        for item in value:
            value_list.append(temp_map[item])
        number_domain_map[newKey] = value_list

    print(number_domain_map)
    FileUtil.write_json_to_file(number_domain_map, '../domain_map_to_number_map.json')