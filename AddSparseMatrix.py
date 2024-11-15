def read_sparse_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # 第一行是矩阵的尺寸
        rows, cols = map(int, lines[0].strip().split(','))
        matrix = {}
        for line in lines[1:]:
            row_data = line.strip().split()
            if not row_data:  # 跳过空行
                continue
            row_index = int(row_data[0])
            elements = row_data[1:] if len(row_data) > 1 else []
            matrix[row_index] = {}
            for element in elements:
                if ":" in element and element.count(":") == 1:  # 确保格式正确
                    col_index, value = element.split(':')
                    if col_index.strip() and value.strip():  # 确保值不为空
                        matrix[row_index][int(col_index)] = int(value)
        return rows, cols, matrix

def write_sparse_matrix(file_path, rows, cols, matrix):
    with open(file_path, 'w') as file:
        file.write(f"{rows}, {cols}\n")
        for row_index in range(1, rows + 1):  # 确保遍历所有行
            if row_index in matrix and matrix[row_index]:  # 行有数据
                line = f"{row_index} " + " ".join(
                    f"{col}:{val}" for col, val in sorted(matrix[row_index].items())
                ) + " "  # 添加空格以匹配格式
            else:  # 空行
                line = f"{row_index} :"
            file.write(line + "\n")



def add_sparse_matrices(rows, cols, matrix1, matrix2):
    result_matrix = {}
    for row in range(1, rows + 1):
        result_matrix[row] = {}
        row1 = matrix1.get(row, {})
        row2 = matrix2.get(row, {})
        all_columns = set(row1.keys()).union(set(row2.keys()))
        for col in all_columns:
            val1 = row1.get(col, 0)
            val2 = row2.get(col, 0)
            if val1 + val2 != 0:
                result_matrix[row][col] = val1 + val2
    return result_matrix

def main():
    input1 = "input1.txt"
    input2 = "input2.txt"
    output = "output.txt"
    
    # 读取输入矩阵
    rows1, cols1, matrix1 = read_sparse_matrix(input1)
    rows2, cols2, matrix2 = read_sparse_matrix(input2)
    
    if rows1 != rows2 or cols1 != cols2:
        raise ValueError("Matrices dimensions do not match.")
    
    # 计算矩阵相加
    result_matrix = add_sparse_matrices(rows1, cols1, matrix1, matrix2)
    
    # 写入输出矩阵
    write_sparse_matrix(output, rows1, cols1, result_matrix)

if __name__ == "__main__":
    main()
