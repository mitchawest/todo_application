from modules.todo import Todo


class TodoFileManager:
    def __init__(self, path="saved_todos.txt"):
        self.__file_path = path

    def get_todos_from_file(self):
        try:
            contents = open(self.__file_path, "r").readlines()
            todos = []
            for row in contents:
                row = row.replace("\n", "").split("\t")
                todos.append(Todo(row[0], row[1]))
            return todos
        except FileNotFoundError:
            try:
                print(f"{self.__file_path} not found. Creating...")
                open(self.__file_path, "w").write("")
                self.get_todos_from_file()
            except Exception as e:
                print(str(e))
                exit()

    def save_todos_to_file(self, todos=[]):
        writer = open(self.__file_path, "w")
        file_text = ""
        for todo in todos:
            if not isinstance(todo, Todo):
                raise ValueError("Todos cannot be saved. Item in list is not a valid Todo")
            file_text += f"{todo.get_priority()}\t{todo.get_name()}\n"
        writer.write(file_text)
