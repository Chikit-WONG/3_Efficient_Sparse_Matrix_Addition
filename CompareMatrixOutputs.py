def normalize_line_endings(lines):
    """将行末统一为 LF 格式以避免换行符差异导致的误判"""
    return [line.rstrip('\r\n') for line in lines]

def compare_files(file1, file2):
    """比较两个文件的内容并显示不同之处"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = normalize_line_endings(f1.readlines())
        lines2 = normalize_line_endings(f2.readlines())
    
    differences = []
    max_lines = max(len(lines1), len(lines2))
    
    for i in range(max_lines):
        line1 = lines1[i] if i < len(lines1) else "<MISSING>"
        line2 = lines2[i] if i < len(lines2) else "<MISSING>"
        if line1 != line2:
            differences.append((i + 1, line1, line2))  # 行号从1开始
    
    return differences

def display_differences(differences):
    """格式化并显示差异"""
    if not differences:
        print("两个文件完全一致！")
    else:
        print(f"发现 {len(differences)} 处不同：")
        for line_num, line1, line2 in differences:
            print(f"第 {line_num} 行不同：")
            print(f"  output.txt:      {line1}")
            print(f"  output_original.txt: {line2}")
            print("-" * 40)

def main():
    file1 = "output.txt"
    file2 = "output_original.txt"
    
    differences = compare_files(file1, file2)
    display_differences(differences)

if __name__ == "__main__":
    main()
