class TodoList:
    def __init__(self):
        self.__items = []
        self.__done_items = []

    # I don't like function, we should re-write it
    def add_item(self, item):
        existing_item = self.__find_item_by_priority(item.get_priority())

        if existing_item is not None:
            err_msg = f"List item with priority {item.get_priority()} already exists: {existing_item.get_name()}"
            raise ValueError(err_msg)

        self.__items.append(item)
        self.__sort_and_normalize_list()

    def get_item_by_priority(self, priority):
        selected_item = None
        for x in self.__items:
            if x.get_priority() == priority:
                selected_item = x
        return selected_item

    def get_items(self):
        return self.__items

    def get_todos_string(self):
        todos = self.__items
        todo_string = "Todo List:\n"
        for todo in todos:
            todo_string += f"{todo.get_priority()}. {todo.get_name()}\n"
        return todo_string

    def get_done_todos_string(self):
        todos = self.__done_items
        todo_string = "Done Todo List:\n"
        for todo in todos:
            todo_string += f"{todo.get_priority()}. {todo.get_name()}\n"
        return todo_string

    def __find_item_by_priority(self, priority):
        for x in self.__items:
            if x.get_priority() == priority:
                return x

    def __find_done_item_by_priority(self, priority):
        for x in self.__done_items:
            if x.get_priority() == priority:
                return x

    def __sort_and_normalize_list(self):
        self.__items.sort(key=lambda list_item: list_item.get_raw_priority())

        i = 1
        for x in self.__items:
            x.set_priority(i)
            i += 1

    def __sort_and_normalize_done_list(self):
        i = 1
        for x in self.__done_items:
            x.set_priority(i)
            i += 1

    def change_list_item_priority(self, old_priority, new_priority):
        found_item = self.__find_item_by_priority(old_priority)

        if found_item is not None:
            # trickery here, add .1 to all current priorities to force sort order when setting same priority as existing list item
            for x in self.__items:
                x.set_priority(x.get_priority() + 0.1)

            found_item.set_priority(new_priority)
        else:
            err_msg = f"No item found with priority {old_priority}"
            raise ValueError(err_msg)

        self.__sort_and_normalize_list()

    def __swap_items_and_done_items(self):
        done_items_in_not_done_items = [x for x in self.__items if x.get_is_done()]
        not_done_items_with_dones_removed = [x for x in self.__items if not x.get_is_done()]
        not_done_items_in_done_items = [x for x in self.__done_items if not x.get_is_done()]
        done_items_with_not_dones_removed = [x for x in self.__done_items if x.get_is_done()]

        self.__items = not_done_items_with_dones_removed + not_done_items_in_done_items
        self.__done_items = done_items_with_not_dones_removed + done_items_in_not_done_items

        self.__sort_and_normalize_done_list()
        self.__sort_and_normalize_list()

    def mark_todo_as_done(self, done_priority):
        found_item = self.__find_item_by_priority(done_priority)
        if found_item is not None:
            found_item.set_is_done(True)
        else:
            err_msg = f"No item found with priority {done_priority}"
            raise ValueError(err_msg)

        self.__swap_items_and_done_items()

    def restore_done_todo(self, done_priority):
        print(done_priority)
        print(self.__done_items)
        found_item = self.__find_done_item_by_priority(done_priority)
        if found_item is not None:
            found_item.set_is_done(False)
            found_item.set_priority(len(self.__items) + 1)
            self.__swap_items_and_done_items()
        else:
            err_msg = f"No done item found with priority { done_priority}"
            raise ValueError(err_msg)
