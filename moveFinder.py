import itertools
from typing import Iterator
from icecream import ic # type: ignore


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

def simulate_button_sequence(button_sequence:list[str], buttons_availible:list[str], number_current:int, cost_maximum:float|None=None) -> None | tuple[int, float]:
    '''
    returns `None` if button_sequence is invalid, otherwise it returns a tuple containing the following:
    - the current number of the calculation (`int`)
    - the remaining actions/button uses (`list[str]`)
    - the cost of performing that operation (using a custom cost-function) (`float`)

    this function modifies the lists it gets, so give it a copy not the original list
    '''

    global digits
    global operations
    global operations_with_argument
    global buttons_implemented

    if len(button_sequence) == 0:
        return (number_current, 0.0)
    if button_sequence[-1] != '=': button_sequence.append('=')
    if buttons_implemented | set(button_sequence) != buttons_implemented: return

    last_operation: str = '='
    number_input: str = ''
    cost:float = 0.0

    for action in button_sequence:
        eval_equals: bool = False
        last_operation_buffer: str = ''
        if cost_maximum != None and cost >= cost_maximum: return # costs too much
        if (not action in buttons_availible) and (action != '='): return # <- invalid input (can not press buttons if they are not availible)
        if action in digits:
            if not (last_operation in operations_with_argument): return # <- invalid input ("5² 2" or "5 sq 2" does not make sense)
            if number_input == '' and action == '0': return # <- leading zeros are a waste of button inputs; can be generated without the leading zero
            number_input += action
            cost += _calculate_cost(buttons_availible=buttons_availible, action=action)
            #last_button = bi
            buttons_availible.remove(action)
            continue

        if action in operations:
            if last_operation in operations_with_argument and number_input == '': return # <- invalid input ("a + /" does not make sense)
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
            if last_operation in operations_with_argument and number_input == '': return # <- invalid input ("a + /" does not make sense)
            match last_operation:
                case 'add': number_current += int(number_input)
                case 'sub': number_current -= int(number_input)
                case 'mul': number_current *= int(number_input)
                case 'div':
                            if int(number_input) == 0: return # <- invalid input (a // 0 is not defined)
                            number_current = number_current // int(number_input)
                case 'mod':
                            if int(number_input) <= 0: return # <- invalid input (a mod 0 is not defined)
                            number_current = number_current % int(number_input)

                case 'sq' : number_current = number_current * number_current
                case 'sqr':
                            if int(number_input) < 0: return # <- invalid input (squareroot of negatives is not allowed)
                            number_current = int(number_current ** 0.5)
                case a    : 
                            warning = f"unknown operation '{a}'. how did that slip through the validation of inputs?"
                            ic(warning)
                            return # <- invalid input
            
            number_input = ''
            #last_button = '='
            last_operation = '=' if last_operation_buffer == '' else last_operation_buffer
            #buttons_availible.remove(action)
            continue

        return # <- invalid input

    return number_current, cost

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

def brute_force_solution(buttons:list[str], number_current:int, number_target:int, max_iterations:int=100_000, increase_iterations:int=20_000, debug:bool=False) -> list[tuple[float, list[str]]]:
    '''
    brute-forces solutions for the current problem.
    returns every solution found.
    if a solution is found, every subsequent search has to have the same or lower cost compared to the previous solutions.
    this means that multiple solutions can be found, but suboptimal ones will be discarded.
    # TODO refine the output to only return a certain range of costs compared to the best.
    '''
    solutions: list[tuple[float, list[str]]] = []
    iterations = 0
    iterations_max_len = len(str(max_iterations))
    solutions_ammount = 0
    solutions_ammount_max_len = 2
    cost_maximum = float(1 << 16)
    for subset in all_subsets(buttons):
        if iterations > max_iterations:
            break
        print(f"\riterations: {iterations:>0{iterations_max_len}} | solutions: {solutions_ammount:>0{solutions_ammount_max_len}}", end="")
        return_value = simulate_button_sequence(button_sequence=subset, buttons_availible=buttons.copy(), number_current=number_current, cost_maximum=cost_maximum)
        iterations += 1
        if return_value == None:
            continue
        numer_evaluated, cost = return_value
        if numer_evaluated != number_target:
            continue
        solutions_ammount += 1
        solutions.append((round(cost, 5), subset))
        cost_maximum = min(cost*2, cost_maximum)
        max_iterations = max(max_iterations, iterations + increase_iterations)
    print()
    return solutions

def main():
    buttons: list[str] = [str(i) for i in range(10)] * 2 + ['add', 'sub', 'mul', 'div'] * 2 #+ ['add', 'sub', 'div']
    number_current: int = 7
    number_target: int = 49

    solutions: list[tuple[float, list[str]]] = brute_force_solution(
        buttons=buttons, number_current=number_current, number_target=number_target, max_iterations=100_000, increase_iterations=20_000, debug=True
        )
    ic(solutions)

if __name__ == "__main__":
    main()
