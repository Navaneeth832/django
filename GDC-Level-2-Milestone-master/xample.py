TASKS_FILE = "tasks.txt"
current_items={}
file = open(TASKS_FILE, "r")
for line in file.readlines():
    item = line[:-1].split(" ")
    current_items[int(item[0])] = " ".join(item[1:])
print(current_items)
file.close()