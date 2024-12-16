def split_file():
    with open('domains.txt', 'r', encoding='utf-8') as infile:  # 根据实际编码调整encoding参数
        lines = infile.readlines()
        total_lines = len(lines)
        lines_per_file = 10000
        file_count = total_lines // lines_per_file

        for i in range(file_count):
            start_index = i * lines_per_file
            end_index = start_index + lines_per_file
            with open(f"./domains/{i + 1}.txt", 'w', encoding='utf-8') as outfile:
                outfile.writelines(lines[start_index:end_index])


if __name__ == "__main__":
    split_file()

