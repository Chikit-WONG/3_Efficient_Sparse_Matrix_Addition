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
