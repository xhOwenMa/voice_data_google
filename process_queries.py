# Open the file and read the contents
with open('queries.txt', 'r') as f:
    lines = f.readlines()

# Process each line to remove quotation marks
processed_lines = [line.replace('"', '') for line in lines]

# Write the processed contents back to the file
with open('queries.txt', 'w') as f:
    f.writelines(processed_lines)
