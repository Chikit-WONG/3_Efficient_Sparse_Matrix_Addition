def read_sparse_matrix(filepath):
    """Read a sparse matrix from file in CSR-like format"""
    with open(filepath, 'r') as f:
        # Read dimensions
        first_line = f.readline().strip()
        rows, cols = map(int, first_line.split(','))
        
        # Initialize data structures
        matrix = {}
        
        # Read matrix data
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
                
            row = int(parts[0])
            if len(parts) > 1 and parts[1] != ':':
                for elem in parts[1:]:
                    if ':' in elem:
                        col, val = map(int, elem.split(':'))
                        matrix[(row-1, col-1)] = val  # Convert to 0-based indexing
                        
    return rows, cols, matrix

def write_sparse_matrix(filepath, rows, cols, matrix):
    """Write sparse matrix to file in required format"""
    with open(filepath, 'w') as f:
        # Write dimensions
        f.write(f"{rows}, {cols}\n")
        
        # Write matrix data
        for i in range(rows):
            row_data = []
            # Collect all elements in current row
            for j in range(cols):
                if (i, j) in matrix:
                    row_data.append((j+1, matrix[(i, j)]))  # Convert back to 1-based indexing
            
            # Format row
            if row_data:
                row_str = f"{i+1} " + " ".join(f"{col}:{val}" for col, val in sorted(row_data))
                f.write(row_str + "\n")
            else:
                f.write(f"{i+1} :\n")

def add_sparse_matrices(matrix1, matrix2, rows, cols):
    """Add two sparse matrices represented as dictionaries"""
    result = {}

    # Add the upper half of the matrices first
    half = rows // 2
    for i in range(half):
        for j in range(cols):
            val1 = matrix1.get((i, j), 0)
            val2 = matrix2.get((i, j), 0)
            if val1 + val2 != 0:
                result[(i, j)] = val1 + val2
        write_sparse_matrix("output.txt", half, cols, result)  # Write upper part of matrix

    # Add the lower half of the matrices
    for i in range(half, rows):
        for j in range(cols):
            val1 = matrix1.get((i, j), 0)
            val2 = matrix2.get((i, j), 0)
            if val1 + val2 != 0:
                result[(i, j)] = val1 + val2
        write_sparse_matrix("output.txt", i + 1, cols, result)  # Write lower part of matrix

    return result

def main():
    # Read input matrices
    rows1, cols1, matrix1 = read_sparse_matrix("input1.txt")
    rows2, cols2, matrix2 = read_sparse_matrix("input2.txt")
    
    # Verify dimensions match
    if (rows1, cols1) != (rows2, cols2):
        raise ValueError("Matrix dimensions do not match")
    
    # Add matrices
    result = add_sparse_matrices(matrix1, matrix2, rows1, cols1)
    
    # Write result
    write_sparse_matrix("output.txt", rows1, cols1, result)

if __name__ == "__main__":
    main()
