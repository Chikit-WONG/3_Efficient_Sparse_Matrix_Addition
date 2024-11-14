import random
import time
from AddSparseMatrixWithLimits import main_without_limits

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

def run_time_test(matrix_size, test_name):
    """运行时间测试，生成两个稀疏矩阵文件并测量相加的执行时间。"""
    rows, cols = matrix_size
    print(f"Running {test_name} with matrix size {rows}x{cols}...")

    # 生成两个输入矩阵
    generate_sparse_matrix(rows, cols, sparsity=0.95, filename="input3.txt")
    generate_sparse_matrix(rows, cols, sparsity=0.95, filename="input4.txt")

    # 测量执行时间
    start_time = time.time()
    main_without_limits("input3.txt", "input4.txt", "output2.txt")
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Execution time for {test_name}: {elapsed_time:.2f} seconds\n")

# 定义测试
def test_a():
    run_time_test((100, 50), "Test A")

def test_b():
    run_time_test((1000, 500), "Test B")

def test_c():
    run_time_test((10000, 5000), "Test C")

# 运行测试
if __name__ == "__main__":
    test_a()
    test_b()
    test_c()
