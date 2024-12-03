from util.file_util import FileUtil

if __name__ == '__main__':
    domains = FileUtil.read_list_from_file('domain')
    new_domains = []
    for line in domains:
        domain = line.strip().split()[0]
        new_domains.append(domain)
    FileUtil.write_list_to_file(new_domains, 'domains.txt')