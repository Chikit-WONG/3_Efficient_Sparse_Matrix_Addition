def read_sparse_matrix(filename):
    with open(filename, 'r') as file:
        # 读取矩阵大小
        rows, cols = map(int, file.readline().strip().split(','))
        matrix = {}

        # 读取非零元素
        for line in file:
            parts = line.split()
            if not parts:  # 如果行为空，跳过
                continue
            row = int(parts[0])  # 行号
            matrix[row] = {}
            for entry in parts[1:]:
                if ':' in entry:
                    col, value = entry.split(':')
                    if col and value:  # 确保 col 和 value 都存在
                        matrix[row][int(col)] = int(value)

    return rows, cols, matrix


def write_sparse_matrix(filename, rows, cols, matrix):
    with open(filename, 'w') as file:
        file.write(f"{rows}, {cols}\n")
        for row in range(1, rows + 1):
            if row in matrix and matrix[row]:
                # 对列索引排序
                sorted_entries = sorted(matrix[row].items())
                row_entries = " ".join(f"{col}:{val}" for col, val in sorted_entries)
                file.write(f"{row} {row_entries}\n")
            else:
                file.write(f"{row} :\n")


def add_matrices(matrix1, matrix2):
    result = {}
    rows = max(matrix1.keys()) if matrix1 else 0

    for row in range(1, rows + 1):
        result[row] = {}
        cols1 = matrix1.get(row, {})
        cols2 = matrix2.get(row, {})
        
        all_cols = set(cols1.keys()).union(set(cols2.keys()))
        for col in all_cols:
            result[row][col] = cols1.get(col, 0) + cols2.get(col, 0)
            if result[row][col] == 0:
                del result[row][col]

    return result

# 读取两个矩阵
rows, cols, matrix1 = read_sparse_matrix("input1.txt")
_, _, matrix2 = read_sparse_matrix("input2.txt")

# 相加矩阵
result_matrix = add_matrices(matrix1, matrix2)

# 写入结果矩阵
write_sparse_matrix("output.txt", rows, cols, result_matrix)
