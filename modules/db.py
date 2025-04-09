import sqlite3
from modules.todo import Todo

class Database:
    def __init__(self, args = {}):
        self.__db_name = args["db_name"] or "todo.db"
        
    def get_connection(self):
        conn = sqlite3.connect(self.__db_name)
        return conn.cursor()
    
    def seed(self):
        cursor = self.get_connection()
        cursor.execute("CREATE TABLE IF NOT EXISTS todos (priority INTEGER PRIMARY KEY, name TEXT, is_done BOOLEAN)")
        cursor.execute("INSERT INTO todos (priority, name, is_done) VALUES (1, 'Buy groceries', false) ON CONFLICT(priority) DO NOTHING")
        cursor.execute("INSERT INTO todos (priority, name, is_done) VALUES (2, 'Do laundry', false) ON CONFLICT(priority) DO NOTHING")
        cursor.execute("INSERT INTO todos (priority, name, is_done) VALUES (3, 'Cook dinner', false) ON CONFLICT(priority) DO NOTHING")
        cursor.connection.commit()
        cursor.connection.close()
        
    def get_todos(self, priorities = None, name = None, is_done = False):
        cursor = self.get_connection()
        if priorities is not None and name is not None:
            todos = cursor.execute(f"SELECT * FROM todos WHERE priority IN ({', '.join(['?']*len(priorities))}) AND lower(name) = ? AND is_done = ?", (*priorities, name, is_done)).fetchall()
        elif name is not None:
            todos = cursor.execute("SELECT * FROM todos WHERE lower(name) = ? AND is_done = ?", (name, is_done)).fetchall()
        elif priorities is not None:
            todos = cursor.execute(f"SELECT * FROM todos WHERE priority IN ({', '.join(['?']*len(priorities))}) AND is_done = ?", (*priorities, is_done)).fetchall()
        else:
            todos = cursor.execute("SELECT * FROM todos WHERE is_done = ?", (is_done,)).fetchall()
        cursor.connection.close()
        return list(map(lambda todo: Todo(todo[0], todo[1], True if todo[2] else False), todos))

    def add_todo(self, todo):
        cursor = self.get_connection()
        cursor.execute("INSERT INTO todos (priority, name, is_done) VALUES (?, ?, ?)", (todo.get_priority(), todo.get_name(), todo.get_is_done()))
        cursor.connection.commit()
        cursor.connection.close()
        
    def mark_todo_as_done(self, priorities = []):
        cursor = self.get_connection()
        for priority in priorities:
            cursor.execute("UPDATE todos SET is_done = true WHERE priority = ?", (priority,))
        cursor.connection.commit()
        cursor.connection.close()
    