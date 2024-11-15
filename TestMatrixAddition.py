import random
from MatrixAdditionMonitor import matrix_addition_with_monitor

def generate_sparse_matrix(rows, cols, sparsity):
    """生成稀疏矩阵"""
    matrix = {}
    for i in range(1, rows + 1):
        matrix[i] = {}
        for j in range(1, cols + 1):
            if random.random() > sparsity:  # 保持稀疏性
                matrix[i][j] = random.randint(-100, 100)  # 随机非零整数
    return matrix

def write_matrix_to_file(matrix, file_name):
    """将稀疏矩阵写入文件"""
    rows = len(matrix)
    cols = max(max(row.keys(), default=0) for row in matrix.values())
    with open(file_name, 'w') as file:
        file.write(f"{rows}, {cols}\n")
        for i in sorted(matrix.keys()):
            if matrix[i]:  # 写非空行
                line = f"{i} " + " ".join(f"{col}:{val}" for col, val in sorted(matrix[i].items()))
                file.write(line + "\n")

def test_matrix_addition(test_name, rows, cols, sparsity, input1, input2, output):
    """生成测试矩阵并运行矩阵加法监控"""
    # 生成稀疏矩阵
    matrix1 = generate_sparse_matrix(rows, cols, sparsity)
    matrix2 = generate_sparse_matrix(rows, cols, sparsity)
    
    # 写入测试输入文件
    write_matrix_to_file(matrix1, input1)
    write_matrix_to_file(matrix2, input2)

    print(f"Running {test_name}...")
    try:
        # 调用矩阵加法监控
        matrix_addition_with_monitor(input1, input2, output, rows, cols)
        print(f"{test_name}: Passed!")
        return True
    except Exception as e:
        print(f"{test_name}: Failed - {str(e)}")
        return False

def main():
    # 定义测试
    tests = [
        {"name": "Test A", "rows": 1000, "cols": 1000, "sparsity": 0.95, "score": 30},
        {"name": "Test B", "rows": 2000, "cols": 2000, "sparsity": 0.95, "score": 30},
        {"name": "Test C", "rows": 5000, "cols": 5000, "sparsity": 0.99, "score": 40},
    ]

    # 总分
    total_score = 0

    for test in tests:
        input1 = f"{test['name']}_input1.txt"
        input2 = f"{test['name']}_input2.txt"
        output = f"{test['name']}_output.txt"
        passed = test_matrix_addition(
            test["name"], test["rows"], test["cols"], test["sparsity"], input1, input2, output
        )
        if passed:
            total_score += test["score"]

    print(f"Total Score: {total_score} / 100")

if __name__ == "__main__":
    main()
