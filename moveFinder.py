from typing import Literal
from icecream import ic # type: ignore
from sympy import isprime, prevprime, nextprime # type: ignore


digits: set[str] = {'0','1','2','3','4','5','6','7','8','9','10'}
operations_simple: set[str] = {'sq','sqr','swap','primes','X++','X--','reverse','near','->25','cut','X+10','X-10'}
operations_with_argument : set[str] = {'+', '-', '*', '/', '%'}
operations_replace: set[str] = {f"{a}->{b}" for a in range(10) for b in range(10) if a != b}
operations_append: set[str] = {f"X{a}" for a in range(10)}
operations_prepend: set[str] = {f"{a}X" for a in range(1, 10)}
buttons_implemented: set[str] =  digits | operations_simple | operations_with_argument | operations_replace | operations_append | operations_prepend | {'='}
button_costs_default: dict[str, float] = {
    '0': 1.0, '1': 1.0, '2': 1.0, '3': 1.0, '4': 1.0, '5': 1.0, '6': 1.0, '7': 1.0, '8': 1.0, '9': 1.0, '10': 1.0,
    '+': 1.1, '-': 1.1, '*': 1.1, '/': 1.1,
    '%': 1.1, 'sq': 1.0, 'sqr': 1.0,
    'swap': 0.8, 'primes': 0.8, 'X++': 1.0, 'X--': 1.0, 'reverse':0.9, 'near': 2.0, '->25': 1.2, 'cut': 1.0,
    'X+10': 1.0, 'X-10': 1.0,
    '=': 0
    }
for name in operations_append | operations_prepend | operations_replace:
    button_costs_default[name] = 0.9

invalid_branches: set[tuple[str, ...]] = set()


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

def check_button_sequence(button_sequence:list[str], buttons_availible:list[str], number_current:int, number_target:int, coins:int=0, cost_maximum:float|None=None) -> tuple[float, Literal["SOLVED"] | Literal["NOT SOLVED"] | Literal["INVALID"]]:
    '''
    this function modifies the lists it gets, so give it a copy not the original list
    '''
    last_operation: str = '='
    number_input: str = ''
    cost:float = 0.0
    number_last = number_current

    if len(button_sequence) == 0:
        if number_current == number_target: return (cost, "SOLVED")
        else: return (cost, "NOT SOLVED")
    if button_sequence[-1] != '=': button_sequence.append('=')
    if buttons_implemented | set(button_sequence) != buttons_implemented:
        return (cost, "INVALID") # <- invalid, because button_sequence contains invalid buttons

    for action in button_sequence:
        eval_equals: bool = False
        last_operation_buffer: str = ''

        if cost_maximum != None and cost >= cost_maximum: return (cost, "NOT SOLVED") # costs too much
    
        if action in digits:
            if not (last_operation in operations_with_argument): return (cost, "INVALID") # <- invalid input ("5 sq 2" does not make sense)
            if number_input == '' and action == '0': return (cost, "INVALID") # <- leading zeros are a waste of button inputs; can be generated without the leading zero
            number_input += action
            cost += _calculate_cost(buttons_availible=buttons_availible, action=action)
            #last_button = bi
            buttons_availible.remove(action)
            continue

        if action in (buttons_implemented ^ digits):
            if last_operation in operations_with_argument and number_input == '':
                return (cost, "INVALID") if action != "=" else (cost, "NOT SOLVED") # <- invalid input ("x + /" does not make sense) (but we do not want to add "+" to the invalid_trees either)
            cost += _calculate_cost(buttons_availible=buttons_availible, action=action)
            if action != "=": buttons_availible.remove(action)
            if last_operation != '=':
                eval_equals = True
                last_operation_buffer = action
            else:
                last_operation = action
                continue
        
        if eval_equals or action == "=":
            if last_operation == '=' and action == '=': continue
            if last_operation in operations_with_argument and number_input == '':
                return (cost, "INVALID") if action != "=" else (cost, "NOT SOLVED") # <- invalid input ("x + /" does not make sense) (but we do not want to add "ad+d" to the invalid_trees either)
            
            if last_operation == '+': number_current += int(number_input)
            elif last_operation == '-': number_current = max(number_current - int(number_input), 0) # the game does not allow you to be under 0, I learned that the hard way
            elif last_operation == '*': number_current *= int(number_input)
            elif last_operation == '/':
                if int(number_input) == 0: return (cost, "INVALID") # <- invalid input (a // 0 is not defined)
                number_current = number_current // int(number_input)
            elif last_operation == '%':
                if int(number_input) <= 0: return (cost, "INVALID") # <- invalid input (a mod 0 is not defined)
                number_current = number_current % int(number_input)

            elif last_operation == 'sq' : number_current = number_current * number_current
            elif last_operation == 'sqr':
                if int(number_current) < 0: return (cost, "INVALID") # <- invalid input (squareroot of negatives is not allowed)
                number_current = round(number_current ** 0.5)
            elif last_operation == 'swap': number_current, number_target = number_target, number_current
            elif last_operation == 'primes': number_current = _find_nearest_prime(number_current=number_current)
            elif last_operation == 'X++': number_current += 1
            elif last_operation == "X--": number_current = max(number_current - 1, 0)
            elif last_operation == 'reverse':
                number_current = int(str(number_current)[::-1])
            elif last_operation == 'near':
                direction = 1 if number_current < number_target else -1
                distance = abs(number_target - number_current) # type: ignore
                distance = min(distance, 10)
                number_current += distance * direction
            elif last_operation == '->25':
                number_current = 25
            elif last_operation == 'cut':
                if len(str(number_target)) < 2: return (cost, "INVALID") # <- the game does not cut the first digit, if it is the only one
                number_target = int(str(number_target)[1:])
            elif last_operation == 'X+10':
                number_current += 10
            elif last_operation == 'X-10':
                number_current -= 10
            elif last_operation in operations_replace:
                if len(last_operation) != 4: raise ValueError(f"'last_operation' can not be parsed since it is not of length 4. How did that even happen?")
                a, b = last_operation[0], last_operation[3]
                number_current = int(str(number_current).replace(a, b))
            elif last_operation in operations_append:
                if len(last_operation) != 2: raise ValueError(f"'last_operation' can not be parsed since it is not of length 4. How did that even happen?")
                a = last_operation[1]
                number_current = int(str(number_current) + a)
                # TODO cap number length (to 999999?) because the game has a cap
            elif last_operation in operations_prepend:
                if len(last_operation) != 2: raise ValueError(f"'last_operation' can not be parsed since it is not of length 4. How did that even happen?")
                a = last_operation[0]
                if a == "0": return (cost, "INVALID")
                number_current = int(a + str(number_current))
                # TODO cap number length (to 999999?) because the game has a cap
            else:
                warning = f"unknown operation '{last_operation}'. how did that slip through the validation of inputs?"
                #ic(warning)
                raise ValueError(warning)
            
            if number_current != number_last: number_last = number_current
            elif action == "=": pass
            else: return (cost, "INVALID") # <- means whatever steps where taken did only increase cost but did not change anything

            number_input = ''
            last_operation = '=' if last_operation_buffer == '' else last_operation_buffer
            continue

        return (cost, "INVALID") # <- invalid input

    if number_current != number_target: return (cost, "NOT SOLVED")
    return (cost, "SOLVED")

def get_local_buttons_availible(buttons_availible:list[str], buttons_used:list[str]) -> list[str]:
    batr: list[str] = buttons_availible.copy() # buttons-availible-to-return
    for button in buttons_used:
        if button in batr:
            batr.remove(button)
    return batr

def brute_force_solution(buttons:list[str], number_current:int, number_target:int, coins:int=0, max_iterations:int=100_000, increase_iterations:int=20_000, debug:bool=False) -> list[tuple[float, list[str]]]:
    branches: list[tuple[float, list[str]]] = [(0.0, [])]
    solutions: list[tuple[float, list[str]]] = []

    iterations_max_len = len(str(max_iterations))
    solutions_ammount_max_len = 2
    
    iterations = 0
    solutions_ammount = 0

    while (iterations < max_iterations) and branches != []:
        iterations += 1

        if debug: print(f"\riterations: {iterations:>0{iterations_max_len}} | solutions: {solutions_ammount:>0{solutions_ammount_max_len}} | len(branches): {len(branches):>06}", end="")

        if (iterations % 5000) == 0:
            branches = sorted(branches, key=lambda x: x[0])
        _cost_current, button_sequence = branches[0]
        branches.pop(0)

        #local_buttons_availible = get_local_buttons_availible(buttons_availible=buttons, buttons_used=button_sequence)
        cost, solved = check_button_sequence(
            button_sequence=button_sequence.copy(), buttons_availible=buttons.copy(), number_current=number_current, number_target=number_target,
            coins=coins
        )

        if solved == "INVALID":
            continue
        elif solved == "SOLVED":
            solutions_ammount += 1
            solutions.append((round(cost, 2), button_sequence))
            continue
        else:
            if solved != "NOT SOLVED":
                raise ValueError(f"How does the button sequence not resolve to either 'SOLVED', 'NOT SOLVED' or 'INVALID' but instead '{solved}'")
        
        branches_new: list[tuple[float, list[str]]] = []
        local_buttons_availible = get_local_buttons_availible(buttons_availible=buttons, buttons_used=button_sequence)
        for button in set(local_buttons_availible):
            cost_new = cost + _calculate_cost(buttons_availible=local_buttons_availible, action=button)
            branches_new.append((cost_new, button_sequence + [button]))
        
        branches += branches_new
    
    if debug: print()
    
    return solutions


def main():
    buttons: list[str] = [str(i) for i in range(10)] * 2 + ['+', '-', '*', '/'] * 2 #+ ['+', '-', '/']
    number_current: int = 7
    number_target: int = 49

    solutions: list[tuple[float, list[str]]] = brute_force_solution(
        buttons=buttons, number_current=number_current, number_target=number_target, max_iterations=10_000, increase_iterations=1_000, debug=True
        )
    ic(solutions)

if __name__ == "__main__":
    main()
