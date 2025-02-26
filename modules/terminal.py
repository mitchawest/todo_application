import sys
import time
import os
from modules.prompt import Prompt


class Terminal:
    def print(self, text, delay=None):
        if delay is not None and type(delay) in [float, int]:
            self.__type_out_text(text, delay)
        else:
            print(text)

    def __type_out_text(self, text, delay):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    def clear(self):
        os.system("clear")

    def ask(self, question=None):
        answer = ""
        if isinstance(question, Prompt):
            answer = input(question.build())
            valid_selections = question.get_valid_selections()
            if answer not in valid_selections:
                err_msg = f"{answer} is not a valid selection. Valid selections are {valid_selections}"
                raise ValueError(err_msg)

            self.print("")
            question.execute(answer)
        elif isinstance(question, str):
            self.print(question, 0.01)
            answer = input("\n\n> ")
            self.print("")
        return answer
