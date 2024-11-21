import time
import psutil
from AddSparseMatrix import add_sparse_matrices_with_two_pointers


def monitor_memory_and_time(func, *args, **kwargs):
    """监控函数的内存和运行时间"""
    start_time = time.perf_counter()  # 使用更精确的时间测量方法
    process = psutil.Process()

    # 调用实际的矩阵加法函数
    result = func(*args, **kwargs)

    end_time = time.perf_counter()  # 使用更精确的时间测量方法
    elapsed_time = end_time - start_time
    peak_memory = process.memory_info().rss / (1024 * 1024)  # 转换为 MB

    return result, elapsed_time, peak_memory


def matrix_addition_with_monitor(input1, input2, output):
    """调用矩阵加法并监控完整过程性能，包括读取和写入矩阵的时间"""
    process = psutil.Process()
    start_time = time.perf_counter()  # 使用更精确的时间测量方法

    # 使用双指针方法进行矩阵加法
    add_sparse_matrices_with_two_pointers(input1, input2, output)

    end_time = time.perf_counter()  # 使用更精确的时间测量方法
    elapsed_time = end_time - start_time
    peak_memory = process.memory_info().rss / (1024 * 1024)  # 转换为 MB

    # 显示性能信息
    print(f"Matrix addition completed in {elapsed_time:.2f} seconds (including I/O).")
    print(f"Peak memory usage: {peak_memory:.2f} MB.")

    # 检测超时或超内存
    if elapsed_time > 30:
        print("Warning: Elapsed time exceeded 30 seconds!")
    if peak_memory > 128:
        print("Warning: Peak memory usage exceeded 128 MB!")
