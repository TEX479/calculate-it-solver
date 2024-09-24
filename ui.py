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

        self.nbr_diplays = tkinter.Frame(master=self.mw, background=bg)
        self.nbr_diplays.grid(row=0, column=0, padx=5, pady=5)

        self.btns_ctrl = tkinter.Frame(master=self.mw, background=bg)
        self.btns_ctrl.grid(row=1, column=0, padx=5, pady=5)

        self.btns_calc = tkinter.Frame(master=self.mw, background=bg)
        self.btns_calc.grid(row=2, column=0, padx=5, pady=5)
        
        self.disp_solutions = tkinter.Frame(master=self.mw, background=bg)
        self.disp_solutions.grid(row=3, column=0, padx=5, pady=5)

        """
        number-displays for showing the current and target number
        """
        self.lbl_num_curr = tkinter.Label(master=self.nbr_diplays, foreground=fg, background=bg, text="current:")
        self.lbl_num_curr.grid(row=0, column=0)
        self.num_curr_tvar = tkinter.Variable(master=self.mw, value="0")
        self.entry_num_curr = tkinter.Entry(master=self.nbr_diplays, foreground=fg, background=bg, textvariable=self.num_curr_tvar)
        self.entry_num_curr.grid(row=0, column=1)

        self.lbl_num_tar = tkinter.Label(master=self.nbr_diplays, foreground=fg, background=bg, text="target:")
        self.lbl_num_tar.grid(row=1, column=0)
        self.num_tar_tvar = tkinter.Variable(master=self.mw, value="0")
        self.entry_num_tar = tkinter.Entry(master=self.nbr_diplays, foreground=fg, background=bg, textvariable=self.num_tar_tvar)
        self.entry_num_tar.grid(row=1, column=1)

        self.lbl_num_mt = tkinter.Label(master=self.nbr_diplays, foreground=fg, background=bg, text="max turns:")
        self.lbl_num_mt.grid(row=2, column=0)
        self.num_mt_tvar = tkinter.Variable(master=self.mw, value="")
        self.entry_num_mt = tkinter.Entry(master=self.nbr_diplays, foreground=fg, background=bg, textvariable=self.num_mt_tvar)
        self.entry_num_mt.grid(row=2, column=1)

        """
        ui-elements for controlling the calculator
        """
        self.btn_flip_ctrl_dir = tkinter.Button(
            master=self.btns_ctrl, foreground=fg, background=bg, text=f"mode:{self._ctrl_direction}", command=self._flip_ctrl_direction
        )
        self.btn_flip_ctrl_dir.grid(row=0, column=0)

        self.btn_calculate = tkinter.Button(
            master=self.btns_ctrl, foreground=fg, background=bg, text=f"CALCULATE", command=self.calculate
        )
        self.btn_calculate.grid(row=0, column=1)

        """
        buttons for the game
        """
        # generate a sorted list because "moveFinder.buttons_implemented" is a set and therefore not ordered
        buttons = sorted(list(moveFinder.buttons_implemented))
        if "=" in buttons: buttons.remove("=")

        # calculate the width of the rectangle that will contain all the buttons so that it is thee closest to a square
        buttons_rectangle_x = len(buttons) ** 0.5
        buttons_rectangle_x = int(buttons_rectangle_x) + (0 if ((buttons_rectangle_x % 1) == 0) else 1)

        # initialize ammounts of each button to 0
        self.btns_actions_ammounts = {name:0 for name in buttons}
        # initialize dict that contains all the action buttons in a complicated "one-liner"
        self.btns_actions = {
            name: btn
            for i in range(len(buttons)) if (
                (
                    btn := tkinter.Button(
                        master=self.btns_calc, text=((name:=buttons[i])+":"+str(self.btns_actions_ammounts[name])), foreground=fg, background=bg,
                        command=(lambda name=name:self.handle_button(name))
                    )
                ).grid(
                    row=(i // buttons_rectangle_x), column=(i % buttons_rectangle_x))
            ) == None
        }

        '''
        ui-stuff for showing solutions
        '''
        self.text_box = scrolledtext.ScrolledText(self.disp_solutions, wrap=tkinter.WORD, fg=fg, bg=bg)
        self.text_box.grid(row=0, column=0)#pack(expand=True, fill='both')
        self.text_box.configure(state="disabled")

        self.mw.mainloop()
    
    def _flip_ctrl_direction(self) -> None:
        if   self._ctrl_direction == "ADD": self._ctrl_direction = "SUB"
        elif self._ctrl_direction == "SUB": self._ctrl_direction = "ADD"
        else: raise ValueError(f"self._ctrl_direction can only be 'ADD' or 'SUB', not '{self._ctrl_direction}'")

        self.btn_flip_ctrl_dir.configure(text=f"mode:{self._ctrl_direction}")

    def handle_button(self, button_name:str) -> None:
        #print(f"pressed '{button_name}'")
        if   self._ctrl_direction == "ADD": self.btns_actions_ammounts[button_name] += 1
        elif self._ctrl_direction == "SUB": self.btns_actions_ammounts[button_name] -= 1
        else: raise ValueError(f"self._ctrl_direction can only be 'ADD' or 'SUB', not '{self._ctrl_direction}'")

        self.btns_actions[button_name].configure(text=f"{button_name}:{self.btns_actions_ammounts[button_name]}")

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
        max_turns = str(self.num_mt_tvar.get()) # type: ignore
        max_turns = None if max_turns == "" else int(max_turns)

        solutions = moveFinder.brute_force_solution(
            buttons=buttons.copy(), number_current=number_current, number_target=number_target, max_turns=max_turns, debug=True
        )
        solutions = reversed(sorted(solutions, key=lambda x: x[0]))
        #print(solutions)
        solutions_readable = [f"{tu[0]:.02f}: {tu[1]}" for tu in solutions]
        self.show_solutions(solutions=solutions_readable)

    def show_solutions(self, solutions:list[str]) -> None:
        self.text_box.configure(state="normal")
        self.text_box.insert("end", "----------------")
        for solution in solutions:
            self.text_box.insert("end", "\n" + solution)
        self.text_box.yview('end') # type: ignore
        self.text_box.configure(state="disabled")



if __name__ == "__main__":
    gui = GUI()
    gui.create_gui()

