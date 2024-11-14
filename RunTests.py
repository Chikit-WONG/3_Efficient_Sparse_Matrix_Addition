import random
import time
import os
from AddSparseMatrixWithLimits import main

# 生成稀疏矩阵的函数
def generate_sparse_matrix(rows, cols, sparsity=0.95, filename="input.txt"):
    """生成一个稀疏矩阵并将其写入指定文件。"""
    with open(filename, 'w') as file:
        file.write(f"{rows}, {cols}\n")
        
        for row in range(1, rows + 1):
            non_zero_elements = []
            for col in range(1, cols + 1):
                if random.random() > sparsity:
                    value = random.randint(-100, 100)
                    non_zero_elements.append(f"{col}:{value}")
            
            if non_zero_elements:
                file.write(f"{row} {' '.join(non_zero_elements)}\n")
            else:
                file.write(f"{row} :\n")

# 测试运行函数
def run_test(matrix_size, test_name):
    """运行测试，生成稀疏矩阵文件，测量时间和内存使用，并检查输出准确性。"""
    rows, cols = matrix_size
    print(f"Running {test_name} with matrix size {rows}x{cols}...")

    # 使用不同的文件名生成测试输入文件
    generate_sparse_matrix(rows, cols, sparsity=0.95, filename="test_input1.txt")
    generate_sparse_matrix(rows, cols, sparsity=0.95, filename="test_input2.txt")

    # 测量时间
    start_time = time.time()
    main("test_input1.txt", "test_input2.txt", "output.txt")
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time:.2f} seconds")

    # 检查输出文件的大小
    output_size = os.path.getsize("output.txt") / 1024  # 转换为KB
    print(f"Output file size: {output_size:.2f} KB")

    # 检查输出文件的准确性
    if compare_files("output.txt", "output_original.txt"):
        print(f"{test_name} passed: Output matches expected results.")
    else:
        print(f"{test_name} failed: Output does not match expected results.")
    
    print(f"{test_name} completed.\n")

def compare_files(file1, file2):
    """逐行比较两个文件内容是否相同"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line1, line2 in zip(f1, f2):
            if line1.strip() != line2.strip():
                return False
    return True

# 定义测试用例
def test_a():
    run_test((100, 50), "Test A")

def test_b():
    run_test((1000, 500), "Test B")

def test_c():
    run_test((10000, 5000), "Test C")

# 运行所有测试用例
if __name__ == "__main__":
    # 生成原始文件以供比较
    generate_sparse_matrix(100, 50, sparsity=0.95, filename="output_original.txt")
    test_a()
    test_b()
    test_c()
