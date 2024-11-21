def add_sparse_matrices_with_two_pointers(input1, input2, output):
    with open(input1, "r") as f1, open(input2, "r") as f2, open(output, "w") as out:
        # Read matrix dimensions
        rows1, cols1 = map(int, f1.readline().strip().split(","))
        rows2, cols2 = map(int, f2.readline().strip().split(","))

        # Write the output matrix dimensions
        out.write(f"{rows1}, {cols1}\n")

        # Ensure the matrices have matching dimensions
        assert rows1 == rows2 and cols1 == cols2, "Matrices dimensions do not match!"

        # Process the matrices row by row
        line1 = f1.readline()
        line2 = f2.readline()

        while line1 or line2:
            # If one file has no more rows, treat it as all-zero rows
            if not line1:
                parts1 = [" "]
                row1 = float("inf")  # Mark as max row number to indicate end of file
            else:
                parts1 = line1.strip().split(maxsplit=1)
                row1 = int(parts1[0])

            if not line2:
                parts2 = [" "]
                row2 = float("inf")
            else:
                parts2 = line2.strip().split(maxsplit=1)
                row2 = int(parts2[0])

            # Process rows with the same or different row numbers
            if row1 == row2:
                row_result = process_row(
                    parts1[1] if len(parts1) > 1 else "",
                    parts2[1] if len(parts2) > 1 else "",
                )
                out.write(f"{row1} {row_result}\n" if row_result else f"{row1} :\n")
                line1 = f1.readline()
                line2 = f2.readline()
            elif row1 < row2:
                # Process non-zero elements in the current row of the first matrix
                row_result = process_row(parts1[1] if len(parts1) > 1 else "", "")
                out.write(f"{row1} {row_result}\n" if row_result else f"{row1} :\n")
                line1 = f1.readline()
            else:
                # Process non-zero elements in the current row of the second matrix
                row_result = process_row("", parts2[1] if len(parts2) > 1 else "")
                out.write(f"{row2} {row_result}\n" if row_result else f"{row2} :\n")
                line2 = f2.readline()


def process_row(row1, row2):
    """Process a single row by summing elements using two pointers."""
    elements1 = row1.split() if row1 else []
    elements2 = row2.split() if row2 else []

    i, j = 0, 0
    result = []

    while i < len(elements1) or j < len(elements2):
        # Skip invalid or empty elements
        if i < len(elements1) and not is_valid_element(elements1[i]):
            i += 1
            continue
        if j < len(elements2) and not is_valid_element(elements2[j]):
            j += 1
            continue

        if i < len(elements1) and (
            j >= len(elements2) or get_col(elements1[i]) < get_col(elements2[j])
        ):
            # Only process elements from the first matrix
            result.append(elements1[i])
            i += 1
        elif j < len(elements2) and (
            i >= len(elements1) or get_col(elements1[i]) > get_col(elements2[j])
        ):
            # Only process elements from the second matrix
            result.append(elements2[j])
            j += 1
        else:
            # Sum elements with the same column index
            col = get_col(elements1[i])
            value = int(elements1[i].split(":")[1]) + int(elements2[j].split(":")[1])
            if value != 0:
                result.append(f"{col}:{value}")
            i += 1
            j += 1

    return " ".join(result)


def get_col(element):
    """Extract the column index from an element."""
    return int(element.split(":")[0])


def is_valid_element(element):
    """Check if the element is a valid 'col:value' pair."""
    if ":" not in element:
        return False
    parts = element.split(":")
    return len(parts) == 2 and parts[0].isdigit() and parts[1].lstrip("-").isdigit()


# Example usage
if __name__ == "__main__":
    input1 = "input1.txt"
    input2 = "input2.txt"
    output = "output.txt"
    add_sparse_matrices_with_two_pointers(input1, input2, output)
