import subprocess

from util.file_util import FileUtil

TSHARK_PATH = r'C:\Program Files\Wireshark\tshark.exe'
def extract_ips_from_pcap(pcap_file):

    result = subprocess.run([TSHARK_PATH, '-r', pcap_file, '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst'],
                            capture_output=True, text=True)
    # 将每行的IP地址对转换为元组，并去除空值
    ip_pairs = [tuple(line.split()) for line in result.stdout.splitlines() if line.strip()]

    # 将所有IP地址放入一个集合中，自动去重
    all_ips = set()
    for src_ip, dst_ip in ip_pairs:
        all_ips.add(src_ip)
        all_ips.add(dst_ip)

    # 将集合转换为列表
    unique_ips = list(all_ips)

    return unique_ips

if __name__ == '__main__':
    capture_ip_map = {}
    urls = FileUtil.read_list_from_file('../domain.txt')
    for i, url in enumerate(urls):
        output_file = f'{i}.pcap'
        ips = extract_ips_from_pcap(output_file)
        capture_ip_map[url] = ips
    output_file = '../capture_ips.json'
    FileUtil.write_json_to_file(capture_ip_map, output_file)
    read_kv_pairs = FileUtil.read_json_from_file(output_file)
    print(read_kv_pairs)