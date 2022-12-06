from pathlib import Path

lines = (Path(__file__).parent / "input.txt").read_text().split("\n")

# Task 1
start_offset = 4
for line in lines:
    for reader_idx in range(start_offset, len(line)):
        sub_string = line[reader_idx-4:reader_idx]
        if len(set(sub_string)) == 4:
            break
    print(reader_idx)

print("---")

# Task 1
offset = 14
for line in lines:
    for reader_idx in range(offset, len(line)):
        sub_string = line[reader_idx-offset:reader_idx]
        if len(set(sub_string)) == offset:
            break
    print(reader_idx)

