def add_sparse_matrices_with_two_pointers(input1, input2, output):
    with open(input1, "r") as f1, open(input2, "r") as f2, open(output, "w") as out:
        # 读取矩阵大小
        rows1, cols1 = map(int, f1.readline().strip().split(","))
        rows2, cols2 = map(int, f2.readline().strip().split(","))

        # 写入结果矩阵大小
        out.write(f"{rows1}, {cols1}\n")

        # 确保矩阵大小一致
        assert rows1 == rows2 and cols1 == cols2, "Matrices dimensions do not match!"

        # 按行处理矩阵
        line1 = f1.readline()
        line2 = f2.readline()

        while line1 or line2:
            # 如果某个文件的行为空，视为全零行
            if not line1:
                parts1 = [" "]
                row1 = float("inf")  # 标记为最大行号，表示文件结束
            else:
                parts1 = line1.strip().split(maxsplit=1)
                row1 = int(parts1[0])

            if not line2:
                parts2 = [" "]
                row2 = float("inf")
            else:
                parts2 = line2.strip().split(maxsplit=1)
                row2 = int(parts2[0])

            # 当前处理行的行号
            if row1 == row2:
                row_result = process_row(
                    parts1[1] if len(parts1) > 1 else "",
                    parts2[1] if len(parts2) > 1 else "",
                )
                out.write(f"{row1} {row_result}\n" if row_result else f"{row1} :\n")
                line1 = f1.readline()
                line2 = f2.readline()
            elif row1 < row2:
                # 第一矩阵当前行非零元素
                row_result = process_row(parts1[1] if len(parts1) > 1 else "", "")
                out.write(f"{row1} {row_result}\n" if row_result else f"{row1} :\n")
                line1 = f1.readline()
            else:
                # 第二矩阵当前行非零元素
                row_result = process_row("", parts2[1] if len(parts2) > 1 else "")
                out.write(f"{row2} {row_result}\n" if row_result else f"{row2} :\n")
                line2 = f2.readline()


def process_row(row1, row2):
    """处理一行，使用双指针方式相加"""
    elements1 = row1.split() if row1 else []
    elements2 = row2.split() if row2 else []

    i, j = 0, 0
    result = []

    while i < len(elements1) or j < len(elements2):
        # 跳过空元素或格式不正确的元素
        if i < len(elements1) and not is_valid_element(elements1[i]):
            i += 1
            continue
        if j < len(elements2) and not is_valid_element(elements2[j]):
            j += 1
            continue

        if i < len(elements1) and (
            j >= len(elements2) or get_col(elements1[i]) < get_col(elements2[j])
        ):
            # 只处理第一矩阵的元素
            result.append(elements1[i])
            i += 1
        elif j < len(elements2) and (
            i >= len(elements1) or get_col(elements1[i]) > get_col(elements2[j])
        ):
            # 只处理第二矩阵的元素
            result.append(elements2[j])
            j += 1
        else:
            # 相加相同列号的元素
            col = get_col(elements1[i])
            value = int(elements1[i].split(":")[1]) + int(elements2[j].split(":")[1])
            if value != 0:
                result.append(f"{col}:{value}")
            i += 1
            j += 1

    return " ".join(result)


def get_col(element):
    """提取列号"""
    return int(element.split(":")[0])


def is_valid_element(element):
    """检查元素是否是合法的 '列号:值' 格式"""
    if ":" not in element:
        return False
    parts = element.split(":")
    return len(parts) == 2 and parts[0].isdigit() and parts[1].lstrip("-").isdigit()


# 示例调用
if __name__ == "__main__":
    input1 = "input1.txt"
    input2 = "input2.txt"
    output = "output.txt"
    add_sparse_matrices_with_two_pointers(input1, input2, output)
