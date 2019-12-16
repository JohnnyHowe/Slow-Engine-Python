import glob

total = 0
filenames = glob.glob("*.py")

for filename in filenames:
    if filename == "line_counter.py":
        continue
    lines = open(filename, "r").readlines()
    for line in lines:
        line.replace(" ", "")
        if line != "\n":
            total += 1

print(total)
        
