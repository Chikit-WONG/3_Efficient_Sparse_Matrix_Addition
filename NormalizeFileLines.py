def clean_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines([line.strip() + '\n' for line in lines])

clean_file('output.txt')
clean_file('output_original.txt')
