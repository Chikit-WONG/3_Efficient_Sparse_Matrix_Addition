def read_csr_matrix(file_path):
    """读取稀疏矩阵并转换为 CSR 格式"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].strip().split(','))

        values = []
        columns = []
        row_pointers = [0]  # 起始为0

        for line in lines[1:]:
            row_data = line.strip().split()
            nonzero_count = 0

            if row_data and len(row_data) > 1:  # 确保行有数据
                for element in row_data[1:]:
                    if ":" in element:
                        col_index, value = element.split(':')
                        if col_index.strip() and value.strip():  # 确保不为空
                            values.append(int(value))
                            columns.append(int(col_index))
                            nonzero_count += 1
            row_pointers.append(row_pointers[-1] + nonzero_count)

        return rows, cols, values, columns, row_pointers


def write_csr_matrix(file_path, rows, cols, values, columns, row_pointers):
    """将 CSR 格式矩阵写回文件，并确保列索引按顺序排列"""
    with open(file_path, 'w') as file:
        file.write(f"{rows}, {cols}\n")
        for i in range(rows):
            start = row_pointers[i]
            end = row_pointers[i + 1]

            if start < end:
                row_data = sorted(
                    zip(columns[start:end], values[start:end]),  # 按列索引排序
                    key=lambda x: x[0]  # 按列索引排序
                )
                row_data_str = " ".join(f"{col}:{val}" for col, val in row_data)
                file.write(f"{i + 1} {row_data_str}\n")
            else:
                file.write(f"{i + 1} :\n")


def add_csr_matrices(rows, cols, values1, columns1, row_pointers1, values2, columns2, row_pointers2):
    """将两个 CSR 格式矩阵相加"""
    result_values = []
    result_columns = []
    result_row_pointers = [0]

    for i in range(rows):
        start1, end1 = row_pointers1[i], row_pointers1[i + 1]
        start2, end2 = row_pointers2[i], row_pointers2[i + 1]

        row1 = {columns1[j]: values1[j] for j in range(start1, end1)}
        row2 = {columns2[j]: values2[j] for j in range(start2, end2)}

        merged_row = {}
        for col in set(row1.keys()).union(row2.keys()):
            merged_value = row1.get(col, 0) + row2.get(col, 0)
            if merged_value != 0:
                merged_row[col] = merged_value

        result_values.extend(merged_row.values())
        result_columns.extend(merged_row.keys())
        result_row_pointers.append(len(result_values))

    return result_values, result_columns, result_row_pointers

def main():
    input1 = "input1.txt"
    input2 = "input2.txt"
    output = "output.txt"

    # 读取 CSR 格式的矩阵
    rows1, cols1, values1, columns1, row_pointers1 = read_csr_matrix(input1)
    rows2, cols2, values2, columns2, row_pointers2 = read_csr_matrix(input2)

    if rows1 != rows2 or cols1 != cols2:
        raise ValueError("Matrices dimensions do not match.")

    # 矩阵相加
    result_values, result_columns, result_row_pointers = add_csr_matrices(
        rows1, cols1, values1, columns1, row_pointers1, values2, columns2, row_pointers2
    )

    # 写回 CSR 格式的结果矩阵
    write_csr_matrix(output, rows1, cols1, result_values, result_columns, result_row_pointers)

if __name__ == "__main__":
    main()
