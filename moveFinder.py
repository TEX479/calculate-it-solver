import itertools
from typing import Iterator
from icecream import ic # type: ignore
from sympy import isprime, prevprime, nextprime # type: ignore


digits: set[str] = {'0','1','2','3','4','5','6','7','8','9'}
operations: set[str] = {'add','sub','mul','div','mod','sq','sqr','switch','primes','X++'}
operations_with_argument : set[str] = {'add', 'sub', 'mul', 'div', 'mod'}
buttons_implemented: set[str] =  digits | operations | {'='}
button_costs_default: dict[str, float] = {'0': 1.0, '1': 1.0, '2': 1.0, '3': 1.0, '4': 1.0, '5': 1.0, '6': 1.0, '7': 1.0, '8': 1.0, '9': 1.0,
                                          'add': 1.0, 'sub': 1.0, 'mul': 1.0, 'div': 1.0,
                                          'mod': 1.0, 'sq': 1.0, 'sqr': 1.0,
                                          'switch': 1.0, 'primes': 1.0, 'X++': 1.0,
                                          '=': 0}

def _find_nearest_prime(number_current: int) -> int:
    if isprime(number_current):
        return number_current
    if number_current <= 2: return 2
    
    lower = prevprime(number_current)
    upper = nextprime(number_current)
    
    if not isinstance(lower, int) or not isinstance(upper, int):
        raise TypeError(f"'prevprime()' or 'nextprime()' did not return an int. this is a reminder that you should not copy code from chargpt.")
    
    # Return the closest prime
    if abs(lower - number_current) <= abs(upper - number_current):
        return lower
    else:
        return upper

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

def check_button_sequence(button_sequence:list[str], buttons_availible:list[str], number_current:int, number_target:int, coins:int=0, cost_maximum:float|None=None) -> None | float:
    '''
    returns `None` if button_sequence is invalid, otherwise it returns a tuple containing the following:
    - the remaining actions/button uses (`list[str]`)
    - the cost of performing that operation (using a custom cost-function) (`float`)

    this function modifies the lists it gets, so give it a copy not the original list
    '''

    global digits
    global operations
    global operations_with_argument
    global buttons_implemented

    last_operation: str = '='
    number_input: str = ''
    cost:float = 0.0
    number_last = number_current

    if len(button_sequence) == 0:
        if number_current == number_target: return cost
        else: return None
    if button_sequence[-1] != '=': button_sequence.append('=')
    if buttons_implemented | set(button_sequence) != buttons_implemented: return # <- invalid, because button_sequence contains invalid buttons

    for action in button_sequence:
        eval_equals: bool = False
        last_operation_buffer: str = ''

        if cost_maximum != None and cost >= cost_maximum: return # costs too much
    
        # \|/ not needed, as the "button_sequence" passed to this funciton is a subset of "buttons_availible" when passed to this function.
        #if (not action in buttons_availible) and (action != '='): return # <- invalid input (can not press buttons if they are not availible)
        if action in digits:
            if not (last_operation in operations_with_argument): return # <- invalid input ("5² 2" or "5 sq 2" does not make sense)
            if number_input == '' and action == '0': return # <- leading zeros are a waste of button inputs; can be generated without the leading zero
            number_input += action
            cost += _calculate_cost(buttons_availible=buttons_availible, action=action)
            #last_button = bi
            buttons_availible.remove(action)
            continue

        if action in operations:
            if last_operation in operations_with_argument and number_input == '': return # <- invalid input ("x + /" does not make sense)
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
            if last_operation in operations_with_argument and number_input == '': return None # <- invalid input ("x + /" does not make sense)
            match last_operation:
                case 'add': number_current += int(number_input)
                case 'sub': number_current -= int(number_input)
                case 'mul': number_current *= int(number_input)
                case 'div':
                    if int(number_input) == 0: return None # <- invalid input (a // 0 is not defined)
                    number_current = number_current // int(number_input)
                case 'mod':
                    if int(number_input) <= 0: return None # <- invalid input (a mod 0 is not defined)
                    number_current = number_current % int(number_input)

                case 'sq' : number_current = number_current * number_current
                case 'sqr':
                    if int(number_current) < 0: return None # <- invalid input (squareroot of negatives is not allowed)
                    number_current = round(number_current ** 0.5)
                case 'switch': number_current, number_target = number_target, number_current
                case 'primes': number_current = _find_nearest_prime(number_current=number_current)
                case 'X++': number_current += 1
                case a    : 
                    warning = f"unknown operation '{a}'. how did that slip through the validation of inputs?"
                    ic(warning)
                    return None # <- input not implemented
            
            if number_current != number_last: number_last = number_current
            else: return None # <- means whatever steps where taken did only increase cost but did not change anything

            number_input = ''
            last_operation = '=' if last_operation_buffer == '' else last_operation_buffer
            continue

        return None # <- invalid input

    if number_current != number_target: return None
    return cost

def all_subsets(lst:list[str], max_turns:int|None=None) -> Iterator[list[str]]:
    seen: set[tuple[str, ...]] = set()

    # Iterate over all subset sizes (from 0 to len(lst))
    for r in range(len(lst) + 1):
        # Get all combinations of size r
        for subset in itertools.combinations(lst, r):
            # Get all permutations of the subset
            for perm in itertools.permutations(subset):
                if max_turns != None and len(perm) > max_turns: return
                perm_tuple = tuple(perm)
                if perm_tuple not in seen:
                    seen.add(perm_tuple)  # Mark this permutation as seen
                    yield list(perm)

def brute_force_solution(buttons:list[str], number_current:int, number_target:int, max_iterations:int=100_000, increase_iterations:int=20_000, max_turns:int|None=None, debug:bool=False) -> list[tuple[float, list[str]]]:
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
    for subset in all_subsets(buttons, max_turns=max_turns):
        if iterations > max_iterations:
            break
        if debug: print(f"\riterations: {iterations:>0{iterations_max_len}} | solutions: {solutions_ammount:>0{solutions_ammount_max_len}}", end="")
        return_value = check_button_sequence(
            button_sequence=subset.copy(), buttons_availible=buttons.copy(), number_current=number_current, number_target=number_target, cost_maximum=cost_maximum
        )
        iterations += 1
        if return_value == None:
            continue
        cost = return_value

        solutions_ammount += 1
        solutions.append((round(cost, 5), subset))
        cost_maximum = min(cost*2, cost_maximum)
        max_iterations = max(max_iterations, iterations + increase_iterations)
    if debug: print()
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
