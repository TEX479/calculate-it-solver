import moveFinder
import tkinter
from tkinter import scrolledtext
from typing import Literal
#import threading

class GUI():
    def __init__(self) -> None:
        self._ctrl_direction: Literal["ADD"] | Literal["SUB"] = "ADD"

    def create_gui(self) -> None:
        fg = "#ffffff"
        bg = "#000000"

        self.mw = tkinter.Tk()
        self.mw.title(f"Calculate It move calculator")
        #self.mw.geometry("1000x800")
        self.mw.columnconfigure(index=1, minsize=0, weight=1)
        self.mw.rowconfigure(index=1, minsize=0, weight=1)
        self.mw.configure(background=bg)


        self.frame_control = tkinter.Frame(master=self.mw, background=bg)
        self.frame_control.grid(row=0, column=0, padx=5, pady=5)

        self.frame_buttons = tkinter.Frame(self.mw, background=bg)
        self.frame_buttons.grid(row=1, column=0, padx=5, pady=5)

        self.frame_basic_buttons = tkinter.Frame(master=self.frame_buttons, background=bg)
        self.frame_basic_buttons.grid(row=0, column=0, padx=5, pady=5)
        
        self.frame_replacement_buttons = tkinter.Frame(master=self.frame_buttons, background=bg)
        self.frame_replacement_buttons.grid(row=0, column=1, padx=5, pady=5)

        self.frame_XXpend_buttons = tkinter.Frame(master=self.frame_buttons, background=bg)
        self.frame_XXpend_buttons.grid(row=0, column=2, padx=5, pady=5)

        self.frame_prepend_buttons = tkinter.Frame(master=self.frame_XXpend_buttons, background=bg)
        self.frame_prepend_buttons.grid(row=0, column=0, pady=5)
        
        self.frame_append_buttons = tkinter.Frame(master=self.frame_XXpend_buttons, background=bg)
        self.frame_append_buttons.grid(row=1, column=0, pady=5)

        self.frame_solution = tkinter.Frame(master=self.mw, background=bg)
        self.frame_solution.grid(row=2, column=0, padx=5, pady=5)

        """
        number-displays for showing the current and target number
        """
        self.lbl_num_curr = tkinter.Label(master=self.frame_control, foreground=fg, background=bg, text="current:")
        self.lbl_num_curr.grid(row=0, column=0, padx=5)
        self.num_curr_tvar = tkinter.Variable(master=self.mw, value="0")
        self.entry_num_curr = tkinter.Entry(master=self.frame_control, foreground=fg, background=bg, textvariable=self.num_curr_tvar)
        self.entry_num_curr.grid(row=0, column=1)

        self.lbl_num_tar = tkinter.Label(master=self.frame_control, foreground=fg, background=bg, text="target:")
        self.lbl_num_tar.grid(row=0, column=2, padx=5)
        self.num_tar_tvar = tkinter.Variable(master=self.mw, value="0")
        self.entry_num_tar = tkinter.Entry(master=self.frame_control, foreground=fg, background=bg, textvariable=self.num_tar_tvar)
        self.entry_num_tar.grid(row=0, column=3)

        self.lbl_coins = tkinter.Label(master=self.frame_control, foreground=fg, background=bg, text="coins:")
        self.lbl_coins.grid(row=0, column=4, padx=5)
        self.coins_tvar = tkinter.Variable(master=self.mw, value="0")
        self.entry_coins= tkinter.Entry(master=self.frame_control, foreground=fg, background=bg, textvariable=self.coins_tvar)
        self.entry_coins.grid(row=0, column=5)

        self.lbl_last = tkinter.Label(master=self.frame_control, foreground=fg, background=bg, text="last:")
        self.lbl_last.grid(row=1, column=4, padx=5)
        self.last_tvar = tkinter.Variable(master=self.mw, value="")
        self.entry_last= tkinter.Entry(master=self.frame_control, foreground=fg, background=bg, textvariable=self.last_tvar)
        self.entry_last.grid(row=1, column=5)

        self.lbl_iters = tkinter.Label(master=self.frame_control, foreground=fg, background=bg, text="iterations:")
        self.lbl_iters.grid(row=0, column=6, padx=5)
        self.iters_tvar = tkinter.Variable(master=self.mw, value="10_000")
        self.entry_iters = tkinter.Entry(master=self.frame_control, foreground=fg, background=bg, textvariable=self.iters_tvar)
        self.entry_iters.grid(row=0, column=7)

        self.lbl_inc_iters = tkinter.Label(master=self.frame_control, foreground=fg, background=bg, text="increase iterations:")
        self.lbl_inc_iters.grid(row=1, column=6, padx=5)
        self.inc_iters_tvar = tkinter.Variable(master=self.mw, value="0")
        self.entry_inc_iters = tkinter.Entry(master=self.frame_control, foreground=fg, background=bg, textvariable=self.inc_iters_tvar)
        self.entry_inc_iters.grid(row=1, column=7)        

        """
        ui-elements for controlling the calculator
        """
        self.btn_flip_ctrl_dir = tkinter.Button(
            master=self.frame_control, foreground=fg, background=bg, text=f"mode:{self._ctrl_direction}", command=self._flip_ctrl_direction
        )
        self.btn_flip_ctrl_dir.grid(row=1, column=0)

        self.btn_calculate = tkinter.Button(
            master=self.frame_control, foreground=fg, background=bg, text=f"CALCULATE", command=self.calculate
        )
        self.btn_calculate.grid(row=1, column=1)

        self.debug_tvar = tkinter.IntVar(self.mw)
        self.checkbox_debug = tkinter.Checkbutton(
            master=self.frame_control, foreground=fg, background=bg, text="debug", variable=self.debug_tvar, onvalue=1, offvalue=0
        )
        self.checkbox_debug.grid(row=1, column=2)
        self.checkbox_debug.configure(state="normal", selectcolor=bg)

        """
        buttons for the game
        """
        self.buttons: dict[str, tkinter.Button] = {}
        self.btns_actions_ammounts = {name:0 for name in moveFinder.buttons_implemented}

        # numbers
        for i in range(0, 10):
            button = tkinter.Button(
                master=self.frame_basic_buttons, text=f"{i}: {self.btns_actions_ammounts[str(i)]}", foreground=fg, background=bg,
                command=(lambda i=i: self.handle_button(str(i)))
            )
            row = 3 if i == 0 else ((i-1) // 3)
            column = 1 if i == 0 else ((i-1) % 3)
            button.grid(row=row, column=column)
            self.buttons[f"{i}"] = button
        button = tkinter.Button(
            master=self.frame_basic_buttons, text=f"{10}: {self.btns_actions_ammounts['10']}", foreground=fg, background=bg,
            command=(lambda: self.handle_button("10"))
        )
        button.grid(row=3, column=2)
        self.buttons["10"] = button

        # operations
        placed_operations: set[str] = set()
        # simple operations
        for i, operation in [(0, "+"), (1, "-"), (2, "*"), (3, "/")]:
            button = tkinter.Button(
                master=self.frame_basic_buttons, text=f"{operation}: {self.btns_actions_ammounts[operation]}", foreground=fg, background=bg,
                command=(lambda operation=operation: self.handle_button(operation))
            )
            button.grid(row=i, column=3)
            placed_operations.add(operation)
            self.buttons[operation] = button
        
        # advanced operations
        # might require custom structure, like "{'%', 'sq', 'sqr', 'primes', 'X++', 'X--', 'swap', 'reverse', 'near', ...}"
        operations = (moveFinder.operations_simple | moveFinder.operations_with_argument) ^ placed_operations
        operations_list = sorted(list(operations))
        i = 4*4
        for operation in operations_list:
            button = tkinter.Button(
                master=self.frame_basic_buttons, text=f"{operation}: {self.btns_actions_ammounts[operation]}", foreground=fg, background=bg,
                command=(lambda operation=operation: self.handle_button(operation))
            )
            button.grid(row=(i // 4), column=(i % 4))
            self.buttons[operation] = button
            i += 1

        # replaces
        _replaces_in_game = ['2->4', '4->7', '7->3', '3->0', '0->8', '8->9', '9->1', '1->5', '5->6', '6->2']
        i = 0
        for name in _replaces_in_game:
            button = tkinter.Button(
                master=self.frame_replacement_buttons, text=f"{name}: {self.btns_actions_ammounts[name]}", foreground=fg, background=bg,
                command=(lambda name=name: self.handle_button(name))
            )
            button.grid(row=i, column=0)
            self.buttons[name] = button
            i += 1
        
        # prepend
        for i in range(1, 10):
            name = f"{i}X"
            button = tkinter.Button(
                master=self.frame_prepend_buttons, text=f"{name}: {self.btns_actions_ammounts[name]}", foreground=fg, background=bg,
                command=(lambda name=name: self.handle_button(name))
            )
            button.grid(row=((i-1) // 3), column=((i-1) % 3))
            self.buttons[name] = button
        
        # append
        for i in range(10):
            name = f"X{i}"
            button = tkinter.Button(
                master=self.frame_append_buttons, text=f"{name}: {self.btns_actions_ammounts[name]}", foreground=fg, background=bg,
                command=(lambda name=name: self.handle_button(name))
            )
            if i == 0: button.grid(row=3, column=1)
            else:      button.grid(row=((i-1) // 3), column=((i-1) % 3))
            self.buttons[name] = button

        '''
        ui-stuff for showing solutions
        '''
        self.text_box = scrolledtext.ScrolledText(self.frame_solution, wrap=tkinter.WORD, fg=fg, bg=bg)
        self.text_box.grid(row=0, column=0)#pack(expand=True, fill='both')
        self.text_box.configure(state="disabled")

        self.mw.mainloop()
    
    def _flip_ctrl_direction(self) -> None:
        if   self._ctrl_direction == "ADD": self._ctrl_direction = "SUB"
        elif self._ctrl_direction == "SUB": self._ctrl_direction = "ADD"
        else: raise ValueError(f"self._ctrl_direction can only be 'ADD' or 'SUB', not '{self._ctrl_direction}'")

        self.btn_flip_ctrl_dir.configure(text=f"mode: {self._ctrl_direction}")

    def handle_button(self, button_name:str) -> None:
        #print(f"pressed '{button_name}'")
        if   self._ctrl_direction == "ADD": self.btns_actions_ammounts[button_name] = max(0, self.btns_actions_ammounts[button_name] + 1)
        elif self._ctrl_direction == "SUB": self.btns_actions_ammounts[button_name] = max(0, self.btns_actions_ammounts[button_name] - 1)
        else: raise ValueError(f"self._ctrl_direction can only be 'ADD' or 'SUB', not '{self._ctrl_direction}'")

        self.buttons[button_name].configure(text=f"{button_name}: {self.btns_actions_ammounts[button_name]}")

    def calculate(self) -> None:
        buttons: list[str] = []
        for name in self.btns_actions_ammounts:
            # "ub" = "upper bound"
            if (ub:=self.btns_actions_ammounts[name]) <= 0: continue
            for _i in range(ub):
                buttons.append(name)
        
        number_current = str(self.num_curr_tvar.get()) # type: ignore
        number_current = int(number_current)
        number_target = str(self.num_tar_tvar.get()) # type: ignore
        number_target = int(number_target)
        coins = str(self.coins_tvar.get()) # type: ignore
        coins = int(coins)
        last = str(self.last_tvar.get()) # type: ignore
        last = int(last) if last.isdecimal() else None
        max_turns = str(self.iters_tvar.get()) # type: ignore
        max_turns = None if max_turns == "" else int(max_turns)
        iterations = str(self.iters_tvar.get()) # type: ignore
        iterations = int(iterations)
        inc_iterations = str(self.inc_iters_tvar.get()) # type: ignore
        inc_iterations = int(inc_iterations)
        debug = bool(self.debug_tvar.get()) # type: ignore

        solutions = moveFinder.brute_force_solution(
            buttons=buttons.copy(), number_current=number_current, number_target=number_target, coins=coins, last=last,
            max_iterations=iterations, increase_iterations=inc_iterations, debug=debug
        )
        solutions = reversed(sorted(solutions, key=lambda x: x[0]))
        #print(solutions)
        solutions_readable = [f"{tu[0]:.02f}: {tu[1]}" for tu in solutions]
        self.show_solutions(solutions=solutions_readable)

    def show_solutions(self, solutions:list[str]) -> None:
        self.text_box.configure(state="normal")
        self.text_box.insert("end", "----------------\n")
        for solution in solutions:
            self.text_box.insert("end", solution + "\n")
        self.text_box.yview('end') # type: ignore
        self.text_box.configure(state="disabled")



if __name__ == "__main__":
    gui = GUI()
    gui.create_gui()

