def read_sparse_matrix(filename):
    """读取稀疏矩阵文件并将其存储为字典格式。"""
    matrix = {}
    with open(filename, 'r') as file:
        rows, cols = map(int, file.readline().strip().split(','))
        for line in file:
            parts = line.split()
            if not parts or parts[0] == ':':
                continue
            row = int(parts[0])
            matrix[row] = {}
            for entry in parts[1:]:
                if ':' in entry and entry.split(':')[1] != '':  # 仅处理包含有效值的项
                    col, value = map(int, entry.split(':'))
                    matrix[row][col] = value
    return rows, cols, matrix


def write_sparse_matrix(filename, rows, cols, matrix):
    """将稀疏矩阵的字典格式写入文件。"""
    with open(filename, 'w') as file:
        file.write(f"{rows}, {cols}\n")
        for row in range(1, rows + 1):
            if row in matrix and matrix[row]:
                sorted_entries = sorted(matrix[row].items())
                row_entries = " ".join(f"{col}:{val}" for col, val in sorted_entries)
                file.write(f"{row} {row_entries}\n")
            else:
                file.write(f"{row} :\n")

def to_csr(matrix):
    """将稀疏矩阵字典转换为 CSR 格式。"""
    values = []
    col_indices = []
    row_ptr = [0]

    for row in sorted(matrix.keys()):
        for col, value in sorted(matrix[row].items()):
            values.append(value)
            col_indices.append(col)
        row_ptr.append(len(values))

    return values, col_indices, row_ptr

def add_csr_matrices(values1, col_indices1, row_ptr1, values2, col_indices2, row_ptr2):
    """计算两个 CSR 格式的矩阵的和。"""
    result_values = []
    result_col_indices = []
    result_row_ptr = [0]
    
    for row in range(len(row_ptr1) - 1):
        row_values = {}
        
        # 遍历第一个矩阵的当前行
        for idx in range(row_ptr1[row], row_ptr1[row + 1]):
            col = col_indices1[idx]
            value = values1[idx]
            row_values[col] = row_values.get(col, 0) + value
        
        # 遍历第二个矩阵的当前行
        for idx in range(row_ptr2[row], row_ptr2[row + 1]):
            col = col_indices2[idx]
            value = values2[idx]
            row_values[col] = row_values.get(col, 0) + value

        # 将非零元素添加到结果矩阵的 CSR 表示
        for col in sorted(row_values.keys()):
            if row_values[col] != 0:  # 只添加非零元素
                result_values.append(row_values[col])
                result_col_indices.append(col)
        
        result_row_ptr.append(len(result_values))

    return result_values, result_col_indices, result_row_ptr
