class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        if args is None or len(args) < 2:
            print("Error: Missing arguments")
            return
        try:
            priority = int(args[0])
            text = " ".join(args[1:])
            if priority in self.current_items:
                print(f"Error: Task with priority {priority} already exists")
                return
            self.current_items[priority] = text
            self.write_current()
            print(f"Added task: \"{text}\" with priority {priority}")
        except ValueError:
            print("Error: Invalid priority number. Please provide a valid integer for priority.")
        pass

    def done(self, args):
        if not args or len(args) != 1:
            print("Error: Missing priority number")
            return
        try:
            priority = int(args[0])
            if priority not in self.current_items:
                print(f"Error: no incomplete item with priority {priority} exists.")
                return
            task = self.current_items.pop(priority)
            self.completed_items.append(f"{priority} {task}")
            self.write_current()
            self.write_completed()
            print(f"Marked item as done.")
        except ValueError:
            print("Error: Invalid priority number. Please provide a valid integer for priority.")

    def delete(self, args):
        if not args or len(args) != 1:
            print("Error: Missing priority number")
            return
        try:
            priority = int(args[0])
            if priority not in self.current_items:
                print(f"Error: No task found with priority {priority}")
                return
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted task with priority {priority}")
        except ValueError:
            print("Error: Invalid priority number. Please provide a valid integer for priority.")

    def ls(self):
        if not self.current_items:
            print("No tasks found.")
            return
        for priority in sorted(self.current_items.keys()):
            print(f"{priority} {self.current_items[priority]}")

    def report(self):
        total_tasks = len(self.current_items) + len(self.completed_items)
        completed_count = len(self.completed_items)
        print(f"Total tasks: {total_tasks}, Completed tasks: {completed_count}")
