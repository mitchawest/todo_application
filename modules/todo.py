class Todo:
    def __init__(self, priority, name, is_done=False):
        self.__priority = self.__normalize_priority(priority)
        self.__name = self.__normalize_name(name)
        self.__is_done = is_done

    def __normalize_priority(self, priority):
        try:
            priority = float(priority)
        except Exception:
            pass

        if not isinstance(priority, float) or priority < 1:
            err_msg = f"Submitted priority {priority} is not a positive, non-zero number"
            raise ValueError(err_msg)

        return priority

    def __normalize_name(self, name):
        if not isinstance(name, str):
            err_msg = f"Submitted name {name} is not a string"
            raise ValueError(err_msg)

        return name

    def set_is_done(self, is_done=True):
        self.__is_done = is_done

    def get_is_done(self):
        return self.__is_done

    def set_priority(self, priority):
        self.__priority = self.__normalize_priority(priority)

    def get_priority(self):
        return round(self.__priority)

    def get_raw_priority(self):
        return self.__priority

    def get_name(self):
        return self.__name
