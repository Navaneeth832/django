class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    def __init__(self):
        self.current_items = {}
        self.completed_items = []

    def read_current(self):
        self.current_items = {}
        try:
            with open(self.TASKS_FILE, "r") as file:
                for line in file.readlines():
                    item = line.rstrip("\n").split(" ")
                    self.current_items[int(item[0])] = " ".join(item[1:])
        except Exception:
            pass

    def read_completed(self):
        self.completed_items = []
        try:
            with open(self.COMPLETED_TASKS_FILE, "r") as file:
                self.completed_items = [line.rstrip("\n") for line in file.readlines()]
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w") as f:
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w") as f:
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
            self.current_items[priority] = text
            self.write_current()
            print(f"Added task: \"{text}\" with priority {priority}")
        except ValueError:
            print("Error: Invalid priority number. Please provide a valid integer for priority.")

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
            # Only task description is stored in completed.txt, matching test expectations
            self.completed_items.append(task)
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
                print(f"Error: item with priority {priority} does not exist. Nothing deleted.")
                return
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted item with priority {priority}")
        except ValueError:
            print("Error: Invalid priority number. Please provide a valid integer for priority.")

    def ls(self):
        if not self.current_items:
            print("No tasks found.")
            return
        count = 0
        for priority in sorted(self.current_items.keys()):
            count += 1
            print(f"{count}. {self.current_items[priority]} [{priority}]")

    def report(self):
        pending_count = len(self.current_items)
        completed_count = len(self.completed_items)
        print(f"Pending : {pending_count}")
        count = 0
        for priority in sorted(self.current_items.keys()):
            count += 1
            print(f"{count}. {self.current_items[priority]} [{priority}]")
        print()
        print(f"Completed : {completed_count}")
        count = 0
        for task in self.completed_items:
            count += 1
            print(f"{count}. {task}")