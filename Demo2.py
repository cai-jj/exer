from util.file_util import FileUtil
if __name__ == '__main__':
    # ['182', '534', '601']
    domain_map = FileUtil.read_json_from_file('domain_map_to_number_map.json')
    # ['485', '559', '690']  ['26', '675', '465']
    for key, value in domain_map.items():
        if key == '182' or key == '534' or key == '601':
            print()