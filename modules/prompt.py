import types


class Prompt:
    # Expects prompts to be a dictionary map of { "prompt string": function }
    def __init__(self, submitted_prompts):
        # maps to a dictionary of
        # { "selection number":
        # {"text": "prompt text here", "function" : function here }}
        self.__prompt_map = {}
        current_number = "1"
        for prompt_string in submitted_prompts:
            self.__prompt_map[current_number] = {
                "text": prompt_string,
                "function": submitted_prompts[prompt_string],
            }
            current_number = str(int(current_number) + 1)

    def get_valid_selections(self):
        return list(self.__prompt_map.keys())

    def build(self):
        prompt_string = ""
        for prompt_number in self.__prompt_map:
            prompt_string += f"{prompt_number}. {self.__prompt_map[prompt_number]['text']}\n"
        prompt_string += "\n> "

        return prompt_string

    def execute(self, selection):
        func = self.__prompt_map[selection]["function"]
        if isinstance(func, types.FunctionType):
            return func()
