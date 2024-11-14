import random
import time
import resource
import psutil
import os
from AddSparseMatrixWithLimits import main

# 设置最大内存和时间限制
MAX_MEMORY_MB = 128
MAX_TIME_SEC = 30

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

def memory_limit_check():
    """设置内存限制。"""
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY_MB * 1024 * 1024, hard))

def run_test(matrix_size, test_name):
    """运行测试，捕获时间和内存信息，并在超出限制时输出资源使用情况。"""
    rows, cols = matrix_size
    print(f"Running {test_name} with matrix size {rows}x{cols}...")

    # 生成输入矩阵
    generate_sparse_matrix(rows, cols, sparsity=0.95, filename="input3.txt")
    generate_sparse_matrix(rows, cols, sparsity=0.95, filename="input4.txt")

    # 设置内存限制
    memory_limit_check()

    # 初始化psutil监控内存和时间
    process = psutil.Process(os.getpid())
    peak_memory_used = 0
    start_time = time.time()

    try:
        main("input3.txt", "input4.txt", "output2.txt")
    except MemoryError:
        print("Memory limit exceeded!")
    except resource.error:
        print("Resource limit error encountered!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 获取内存使用的峰值
        peak_memory_used = process.memory_info().rss / (1024 * 1024)

        # 输出实际的执行时间和内存峰值
        print(f"Execution time: {elapsed_time:.2f} seconds")
        print(f"Peak memory used: {peak_memory_used:.2f} MB\n")

# 定义测试
def test_a():
    run_test((100, 50), "Test A")

def test_b():
    run_test((1000, 500), "Test B")

def test_c():
    run_test((10000, 5000), "Test C")

# 运行测试
if __name__ == "__main__":
    test_a()
    test_b()
    test_c()
