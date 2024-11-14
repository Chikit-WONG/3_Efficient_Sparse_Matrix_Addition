import sys
from AddSparseMatrix import read_sparse_matrix, write_sparse_matrix, add_matrices

def main(input_file1="input1.txt", input_file2="input2.txt", output_file="output2.txt"):
    rows, cols, matrix1 = read_sparse_matrix(input_file1)
    _, _, matrix2 = read_sparse_matrix(input_file2)

    # 相加矩阵
    result_matrix = add_matrices(matrix1, matrix2)

    # 写入结果矩阵
    write_sparse_matrix(output_file, rows, cols, result_matrix)

# 运行主程序
if __name__ == "__main__":
    # 如果有传入参数，则使用参数中的文件名
    args = sys.argv[1:]
    input_file1 = args[0] if len(args) > 0 else "input1.txt"
    input_file2 = args[1] if len(args) > 1 else "input2.txt"
    output_file = args[2] if len(args) > 2 else "output2.txt"
    main(input_file1, input_file2, output_file)
