import time
import resource
import sys
from AddSparseMatrix import read_sparse_matrix, write_sparse_matrix, to_csr, add_csr_matrices

# 设置最大内存限制（128MB）
MAX_MEMORY_MB = 128
MAX_TIME_SEC = 30

def memory_limit_check():
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY_MB * 1024 * 1024, hard))

def time_memory_checker(func):
    def wrapper(*args, **kwargs):
        memory_limit_check()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
        except MemoryError:
            print("Memory limit exceeded!")
            sys.exit(1)
        except resource.error:
            print("Resource limit error encountered!")
            sys.exit(1)
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time > MAX_TIME_SEC:
            print("Time limit exceeded!")
            sys.exit(1)
        
        usage = resource.getrusage(resource.RUSAGE_SELF)
        memory_used_mb = usage.ru_maxrss / 1024

        print(f"Execution time: {elapsed_time:.2f} seconds")
        print(f"Memory used: {memory_used_mb:.2f} MB")
        
        return result
    
    return wrapper

@time_memory_checker
def main(input_file1="input1.txt", input_file2="input2.txt", output_file="output2.txt"):
    rows1, cols1, matrix1 = read_sparse_matrix(input_file1)
    rows2, cols2, matrix2 = read_sparse_matrix(input_file2)

    if rows1 != rows2 or cols1 != cols2:
        raise ValueError("Matrices dimensions do not match.")

    values1, col_indices1, row_ptr1 = to_csr(matrix1)
    values2, col_indices2, row_ptr2 = to_csr(matrix2)

    result_values, result_col_indices, result_row_ptr = add_csr_matrices(
        values1, col_indices1, row_ptr1, values2, col_indices2, row_ptr2
    )

    # 将结果转换回字典格式，方便写入文件
    result_matrix = {}
    for row in range(len(result_row_ptr) - 1):
        result_matrix[row + 1] = {}
        for idx in range(result_row_ptr[row], result_row_ptr[row + 1]):
            col = result_col_indices[idx]
            value = result_values[idx]
            result_matrix[row + 1][col] = value

    write_sparse_matrix(output_file, rows1, cols1, result_matrix)

if __name__ == "__main__":
    main()
