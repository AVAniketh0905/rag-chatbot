import os

# Specify the directory containing the .txt files
directory = "output"
total_lines = 0
# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        size = os.path.getsize(file_path)
        sizeMb = size / 1024 / 1024

        # Open the file and count the lines
        with open(file_path, "r", encoding="UTF-8") as file:
            line_count = sum(1 for line in file)

        # Print the file name and the number of lines
        print(f"{filename}: {line_count} lines, {sizeMb:.2f} MB")
        total_lines += line_count
print(f"Total lines: {total_lines}")
