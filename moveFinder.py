'''
actions:
+,-,*,/,
'''


from typing import Callable
from math import inf


#actions : dict[str, tuple[int, Callable]] = {} # dict['action_name', tuple['arguments_int']]

class Calculator():
    def __init__(self, button_ammounts:dict[str, int]|None=None, number_current:int|None=None, number_target:int|None=None, currency:int=0) -> None:

        self.button_ammounts : dict[str, int] = {'0': 2, '1': 2, '2': 2, '3': 2, '4': 2, '5': 2, '6': 2, '7': 2, '8': 2, '9': 2,
                                                  'add': 2, 'sub': 2, 'mul': 2, 'div': 2,
                                                  'mod': 0, 'sq': 0, 'sqr': 0,
                                                  '=': 999}
        if button_ammounts != None: self.modify_button_ammounts(button_ammounts=button_ammounts)
        self.buttons_operations_with_argument : list[str] = ['add', 'sub', 'mul', 'div', 'mod']
        self.button_costs_default : dict[str, float] = {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1,
                                                        'add': 1, 'sub': 1, 'mul': 1, 'div': 1,
                                                        'mod': 0, 'sq': 0, 'sqr': 0,
                                                        '=': 0}

        self.number_current = 0 if number_current == None else number_current
        self.number_target = 0 if number_target == None else number_target
        self.currency = currency
    
    def modify_button_ammounts(self, button_ammounts:dict[str, int]) -> None:
        self.button_ammounts = {name:self.button_ammounts[name] if not name in button_ammounts else button_ammounts[name] for name in (list(self.button_ammounts) + list(button_ammounts)) if name in self.button_ammounts}
    
    def button_sequence_is_valid(self, button_sequence:list[str]=[]) -> bool:
        button_ammounts = self.button_ammounts
        last_action : str = '='
        for button_input in button_sequence:
            if not button_input in button_ammounts:
                return False
            if button_ammounts[button_input] <= 0:
                return False
            if button_input in self.buttons_operations_with_argument and last_action in self.buttons_operations_with_argument:
                return False
            if last_action == '=' and button_input.isdigit():
                return False
            
            button_ammounts[button_input] -= 1
            last_action = button_input

        return True
    

def action_parser():
    ...

def main():
    buttons = Calculator()#button_ammounts={'3':7})
    print(buttons.button_ammounts)


if __name__ == "__main__":
    main()
