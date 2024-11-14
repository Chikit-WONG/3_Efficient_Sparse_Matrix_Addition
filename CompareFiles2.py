def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = [line.strip() for line in f1]  # 去除换行符
        content2 = [line.strip() for line in f2]  # 去除换行符
    
    if content1 == content2:
        print("The files match exactly!")
    else:
        differences = []
        for i, (line1, line2) in enumerate(zip(content1, content2), start=1):
            if line1 != line2:
                differences.append((i, line1, line2))
        
        print("The files have differences at the following lines:")
        for line_num, line1, line2 in differences:
            print(f"Line {line_num}:")
            print(f"output.txt        : {line1}")
            print(f"output_original.txt: {line2}")

# 比较 output.txt 和 output_original.txt
compare_files("output2.txt", "output_original.txt")
