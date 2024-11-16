import time
import psutil
from AddSparseMatrix import read_sparse_matrix, add_sparse_matrices, write_sparse_matrix

def monitor_memory_and_time(func, *args, **kwargs):
    """监控函数的内存和运行时间"""
    start_time = time.time()
    process = psutil.Process()

    # 调用实际的矩阵加法函数
    result = func(*args, **kwargs)

    end_time = time.time()
    elapsed_time = end_time - start_time
    peak_memory = process.memory_info().rss / (1024 * 1024)  # 转换为 MB

    return result, elapsed_time, peak_memory

def matrix_addition_with_monitor(input1, input2, output2, rows, cols):
    """调用矩阵加法并监控运行性能"""
    rows1, cols1, matrix1 = read_sparse_matrix(input1)
    rows2, cols2, matrix2 = read_sparse_matrix(input2)

    if rows1 != rows2 or cols1 != cols2:
        raise ValueError("Matrices dimensions do not match.")

    # 监控矩阵加法性能
    result, elapsed_time, peak_memory = monitor_memory_and_time(
        add_sparse_matrices, matrix1, matrix2, rows1, cols1  # 确保传入matrix1, matrix2, rows, cols
    )

    # 写入 output2.txt
    write_sparse_matrix(output2, rows1, cols1, result)

    # 显示性能信息
    print(f"Matrix addition completed in {elapsed_time:.2f} seconds.")
    print(f"Peak memory usage: {peak_memory:.2f} MB.")

    # 检测超时或超内存
    if elapsed_time > 30:
        print("Warning: Elapsed time exceeded 30 seconds!")
    if peak_memory > 128:
        print("Warning: Peak memory usage exceeded 128 MB!")

def main():
    input1 = "input1.txt"
    input2 = "input2.txt"
    output2 = "output2.txt"

    rows, cols = 100, 50  # 预定义的矩阵大小
    matrix_addition_with_monitor(input1, input2, output2, rows, cols)

if __name__ == "__main__":
    main()
