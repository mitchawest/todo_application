import time
from modules.terminal import Terminal
from modules.prompt import Prompt
from modules.todo_list import TodoList
from modules.todo import Todo
from modules.todo_file_manager import TodoFileManager
from colorama import init, Fore, Style

init()

term = Terminal()
todo_list = TodoList()
file_manager = TodoFileManager()
todos_from_file = file_manager.get_todos_from_file()
for todo in todos_from_file:
    todo_list.add_item(todo)


def safe_convert_int(string_int):
    converted = None
    try:
        converted = int(string_int)
    except Exception:
        pass
    return converted


def exit_program():
    file_manager.save_todos_to_file(todo_list.get_items())
    term.clear()
    term.print("See ya! 👋\n\n", 0.01)
    time.sleep(2)
    term.clear()
    exit()


def list_todos():
    term.clear()
    term.print(todo_list.get_todos_string())
    term.print("What would you like to do?\n", 0.01)
    term.ask(
        Prompt(
            {
                "Go back": None,
                "Add a todo": add_todo,
                "Change todo priority": update_todo_priority,
                "Mark a todo as done": mark_todo_as_done,
                "Show done todos": list_done_todos,
                "Exit": exit_program,
            }
        )
    )


def add_todo():
    term.clear()
    task_name = term.ask("What is the task?")
    priority = term.ask("What is the priority?")

    priority = safe_convert_int(priority)

    todo_list.add_item(Todo(priority, task_name))


def update_todo_priority():
    term.clear()
    term.print(todo_list.get_todos_string())
    requested_priority = term.ask("Which task do you want to change?")

    requested_priority = safe_convert_int(requested_priority)

    new_priority = term.ask("What is the new priority?")

    new_priority = safe_convert_int(new_priority)

    todo_list.change_list_item_priority(requested_priority, new_priority)


def mark_todo_as_done():
    term.clear()
    term.print(todo_list.get_todos_string())
    done_todo = term.ask("Which todo did you finish?")

    done_todo = safe_convert_int(done_todo)

    todo_list.mark_todo_as_done(done_todo)


def mark_todo_as_not_done():
    term.clear()
    not_done_todo = term.ask("Which todo do you want to restore?")

    not_done_todo = safe_convert_int(not_done_todo)

    todo_list.restore_done_todo(not_done_todo)


def list_done_todos():
    term.clear()
    term.print(todo_list.get_done_todos_string())
    term.print("What would you like to do?\n", 0.01)
    term.ask(
        Prompt(
            {
                "Go back": None,
                "Restore todo": mark_todo_as_not_done,
                "Exit": exit_program,
            }
        )
    )

# At some point I'm going to add color with colorama
try:
    term.clear()
    term.print("Welcome to the todo list application!\n\n", 0.01)
    time.sleep(1)
    term.print("Time to get shit done! 🚀🚀🚀\n\n", 0.01)
    time.sleep(1)

    while 1 == 1:
        try:
            term.clear()
            term.print("What would you like to do?\n\n", 0.01)
            term.ask(
                Prompt(
                    {
                        "Add a todo": add_todo,
                        "See my todos": list_todos,
                        "Change todo priority": update_todo_priority,
                        "Mark a todo as done": mark_todo_as_done,
                        "Show done todos": list_done_todos,
                        "Exit": exit_program,
                    }
                )
            )
            term.clear()

        except ValueError as e:
            term.clear()
            term.print(Fore.RED + f"{str(e)}\n\n", 0.005)
            print(Style.RESET_ALL)
            time.sleep(2)

except KeyboardInterrupt:
    file_manager.save_todos_to_file(todo_list.get_items())
    exit_program()
