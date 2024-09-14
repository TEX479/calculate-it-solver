import itertools
from typing import Iterator
from icecream import ic # type: ignore
from math import factorial


class Calculator():
    def __init__(self, buttons_availible:list[str]|dict[str, int]|None=None, number_current:int|None=None, number_target:int|None=None, currency:int=0) -> None:
        self.digits = {'0','1','2','3','4','5','6','7','8','9'}
        self.operations: set[str] = {'add','sub','mul','div','mod','sq','sqr'}
        self.buttons_implemented: set[str] =  self.digits | self.operations | {'='}

        self.buttons_availible : list[str] = ['0','0','1','1','2','2','3','3','4','4','5','5','6','6','7','7','8','8','9','9',
                                            'add','add','sub','sub','mul','mul','div','div']
        if type(buttons_availible) == list: self.buttons_availible = buttons_availible
        elif type(buttons_availible) == dict: self.buttons_availible = self.__buttondict2list(button_dict=buttons_availible)

        self.operations_with_argument : set[str] = {'add', 'sub', 'mul', 'div', 'mod'}
        self.button_costs_default : dict[str, float] = {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1,
                                                        'add': 1, 'sub': 1, 'mul': 1, 'div': 1,
                                                        'mod': 1.2, 'sq': 1.2, 'sqr': 1.2,
                                                        '=': 0}

        self.number_current = 0 if number_current == None else number_current
        self.number_target = 0 if number_target == None else number_target
        self.currency = currency
    
    def _cost_multiplier_by_ammount(self, ammount:int) -> float:
        if ammount: return 10
        if ammount <= 1: return 1.5
        if ammount <= 3: return 1
        if ammount <= 5: return 0.8

        if ammount > 20: return 0.2
        return 0.5

    def __buttondict2list(self, button_dict:dict[str, int]) -> list[str]:
        l2r : list[str] = [] #list 2 return
        for name in button_dict:
            if (not name in self.buttons_availible) or ((ammount:=button_dict[name]) <= 0):
                continue
            l2r += [name] * ammount
        return l2r
    
    def button_sequence_is_valid(self, button_sequence:list[str]=[]) -> bool:
        button_ammounts: list[str] = self.buttons_availible
        last_action : str = '='
        for button_input in button_sequence:
            if (not button_input in self.buttons_implemented) and (button_input != '='):
                return False
            if not button_input in button_ammounts:
                return False
            if button_input in self.operations_with_argument and last_action in self.operations_with_argument:
                return False
            if last_action == '=' and button_input.isdigit():
                return False
            if last_action == '=' and button_input == '=':
                return False
            
            button_ammounts.remove(button_input)
            last_action = button_input
        
        if last_action in self.operations_with_argument:
            return False

        return True

    def _calc_cost(self, button_ammounts:list[str], action:str) -> float:
        return self._cost_multiplier_by_ammount(button_ammounts.count(action)) * self.button_costs_default[action]

    def try_apply_button_sequence(self, button_sequence:list[str]=[]) -> None | tuple[int, list[str], float]:
        '''
        returns `None` if button_sequence is invalid, otherwise it returns a tuple containing the following:
        - the current number of the calculation (`int`)
        - the remaining actions/button uses (`list[str]`)
        - the cost of performing that operation (using a custom cost-function) (`float`)

        DOES NOT change any variables of the calculator itself
        '''
        button_ammounts: list[str] = self.buttons_availible
        number_current: int = self.number_current
        #last_button: str = '='
        last_operation: str = '='
        number_input: str = ''
        cost:float = 0.0

        for action in button_sequence:
            if not action in self.buttons_implemented: return # <- invalid input
            if not action in button_ammounts: return # <- invalid input
            if (last_operation in self.operations_with_argument):
                if not action in self.digits or len(action) > 1: return # <- invalid input
                number_input += action
                cost += self._calc_cost(button_ammounts=button_ammounts, action=action)
                #last_button = bi
                continue
            if action in self.digits: return # <- invalid input
            if action in self.operations and last_operation != "=": return # <- invalid input
            if action == "=":
                if last_operation == '=': return # <- invalid input
                if last_operation in self.operations_with_argument and number_input == '': return # <- invalid input
                match last_operation:
                    case 'add': number_current += int(number_input)
                    case 'sub': number_current -= int(number_input)
                    case 'mul': number_current *= int(number_input)
                    case 'div': number_current = number_current // int(number_input)
                    case 'mod': number_current = number_current % int(number_input)

                    case 'sq' : number_current = number_current * number_current
                    case 'sqr':
                                if int(number_current) < 0: return # <- invalid input
                                number_current = int(number_current ** 0.5)
                    case _    : return # <- invalid input
                
                number_input = ''
                #last_button = '='
                last_operation = '='
                continue
            if action in self.operations:
                if number_input != '': return # <- invalid input
                cost += self._calc_cost(button_ammounts=button_ammounts, action=action)
                last_operation = action
                continue

            return # <- invalid input

        return number_current, button_ammounts, cost

    def apply_state(self, number_current:int, buttons_availible:list[str]|dict[str,int]) -> None:
        self.number_current = number_current
        if type(buttons_availible) == dict: buttons_availible = self.__buttondict2list(button_dict=buttons_availible)
        elif type(buttons_availible) != list: raise TypeError('Dude I hinted all the types. It should be easy to not fuck this up. This error should not be able to risen whatsoever. It exists because pylance sucks ass. If this gets run, your coding skills are so bad, you should probably think about doing something else than coding with your life.')
        self.buttons_availible = buttons_availible

    def has_buttons_left(self) -> bool:
        return len(self.buttons_availible) != 0


digits: set[str] = {'0','1','2','3','4','5','6','7','8','9'}
operations: set[str] = {'add','sub','mul','div','mod','sq','sqr'}
operations_with_argument : set[str] = {'add', 'sub', 'mul', 'div', 'mod'}
buttons_implemented: set[str] =  digits | operations | {'='}
button_costs_default: dict[str, float] = {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1,
                                          'add': 1, 'sub': 1, 'mul': 1, 'div': 1,
                                          'mod': 1.2, 'sq': 1.2, 'sqr': 1.2,
                                          '=': 0}

def _cost_multiplier_by_ammount(ammount:int) -> float:
    if ammount <= 1: return 4.0
    if ammount <= 2: return 1.2
    if ammount <= 3: return 1.0
    if ammount <= 5: return 0.8
    if ammount > 20: return 0.2
    return 0.5

def _calculate_cost(buttons_availible:list[str], action:str) -> float:
    global button_costs_default
    return _cost_multiplier_by_ammount(buttons_availible.count(action)) * button_costs_default[action]

def simulate_button_sequence(button_sequence:list[str], buttons_availible:list[str], number_current:int, cost_lowest:float|None=None) -> None | tuple[int, list[str], float]:
    '''
    returns `None` if button_sequence is invalid, otherwise it returns a tuple containing the following:
    - the current number of the calculation (`int`)
    - the remaining actions/button uses (`list[str]`)
    - the cost of performing that operation (using a custom cost-function) (`float`)

    this function modifies the lists it gets, so give it a copy not the original list
    '''

    if len(button_sequence) == 0:
        return (number_current, buttons_availible, 0.0)
    if button_sequence[-1] != '=': button_sequence.append('=')
    if buttons_implemented | set(button_sequence) == buttons_implemented: return

    global digits
    global operations
    global operations_with_argument
    global buttons_implemented

    last_operation: str = '='
    number_input: str = ''
    cost:float = 0.0

    for action in button_sequence:
        eval_equals: bool = False
        last_operation_buffer: str = ''
        if cost_lowest != None and cost >= cost_lowest: return # costs too much
        if (not action in buttons_availible) and (action != '='): return # <- invalid input
        if action in digits:
            if not (last_operation in operations_with_argument): return # <- invalid input
            number_input += action
            cost += _calculate_cost(buttons_availible=buttons_availible, action=action)
            #last_button = bi
            buttons_availible.remove(action)
            continue

        if action in operations:
            if last_operation in operations_with_argument and number_input == '': return # <- invalid input
            cost += _calculate_cost(buttons_availible=buttons_availible, action=action)
            buttons_availible.remove(action)
            if last_operation != '=':
                eval_equals = True
                last_operation_buffer = action
            else:
                last_operation = action
                continue
        
        if eval_equals or action == "=":
            if last_operation == '=' and action == '=': continue
            if last_operation in operations_with_argument and number_input == '': return # <- invalid input
            match last_operation:
                case 'add': number_current += int(number_input)
                case 'sub': number_current -= int(number_input)
                case 'mul': number_current *= int(number_input)
                case 'div':
                            if int(number_input) == 0: return # <- invalid input
                            number_current = number_current // int(number_input)
                case 'mod':
                            if int(number_input) <= 0: return # <- invalid input
                            number_current = number_current % int(number_input)

                case 'sq' : number_current = number_current * number_current
                case 'sqr':
                            if int(number_input) < 0: return # <- invalid input
                            number_current = int(number_current ** 0.5)
                case _    : return # <- invalid input
            
            number_input = ''
            #last_button = '='
            last_operation = '=' if last_operation_buffer == '' else last_operation_buffer
            #buttons_availible.remove(action)
            continue

        return # <- invalid input

    if last_operation != '=':
        return # <- invalid input

    return number_current, buttons_availible, cost

def all_subsets(lst:list[str]) -> Iterator[list[str]]:
    seen: set[tuple[str, ...]] = set()

    # Iterate over all subset sizes (from 0 to len(lst))
    for r in range(len(lst) + 1):
        # Get all combinations of size r
        for subset in itertools.combinations(lst, r):
            # Get all permutations of the subset
            for perm in itertools.permutations(subset):
                perm_tuple = tuple(perm)
                if perm_tuple not in seen:
                    seen.add(perm_tuple)  # Mark this permutation as seen
                    yield list(perm)

def brute_force_solution(buttons:list[str], number_current:int, number_target:int, max_iterations:int=1000000):
    solutions: list[tuple[float, list[str]]] = []
    iterations = 0
    iterations_max_len = len(str(factorial(len(buttons))))
    solutions_ammount = 0
    solutions_ammount_max_len = 2
    cost_lowest = float(1 << 16)
    for subset in all_subsets(buttons):
        if iterations > max_iterations:
            break
        print(f"\riterations: {iterations:>0{iterations_max_len}} | solutions: {solutions_ammount:>0{solutions_ammount_max_len}}", end="")
        return_value = simulate_button_sequence(button_sequence=subset, buttons_availible=buttons.copy(), number_current=number_current, cost_lowest=cost_lowest)
        iterations += 1
        if return_value == None:
            continue
        #ic(subset, return_value)
        #ic(return_value)
        numer_evaluated, _buttons_remaining, cost = return_value
        if numer_evaluated != number_target:
            continue
        solutions_ammount += 1
        solutions.append((cost, subset))
        cost_lowest = cost #min(cost*1.1, cost_lowest)
    
    return solutions

def main():
    buttons: list[str] = [str(i) for i in range(10)] * 2 + ['add', 'sub', 'mul', 'div'] + ['add', 'sub', 'div']
    number_current: int = 7
    number_target: int = 49

    #c = Calculator()#button_ammounts={'3':7})
    #print(buttons.button_ammounts)

    solutions = brute_force_solution(buttons=buttons, number_current=number_current, number_target=number_target)
    ic(solutions)
    #solution = simulate_button_sequence(['add', '2', 'add', '3'], ['add', 'add', '2', '3', 'mod'], 0)
    #ic(solution)


if __name__ == "__main__":
    main()
