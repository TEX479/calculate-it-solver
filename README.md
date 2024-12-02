### Contents
- [Why?](#why)
- [Setup](#setup)
- [Usage](#usagee)


# Why?
So I saw a video about a game called ["Calculate It"](https://store.steampowered.com/app/3043740/Calculate_It/). A rougelike game about calculating. The base game mechanic is a limit for each button and a shop where you can re-buy these buttons, among some new ones. The person playing the game sometimes said things along the lines of "I don't think I am playing the most optimal way". That got me thinking. There are some buttons that have random effects, but most of them are strictly defined in their function ("+" never devide the number; unlike "add random ammount between 1 and 10" or "add use to random button"). Since most of the game's solutions are predictable, I could probably create a program that finds the most optimal solution to a given set of buttons that are allowed and a inital number that needs to be turned into a given target number. Well this project contains my attempts at finding out if I could.

# Setup
First things first I will not release any builds any time soon (except if there is a huge demand for it), so you'll have to run it from source. That means you will have to download the sourcecode install python and this projects dependencies and run the python files you are interested in.\
\
DISCLAIMER: I am just a dude who doesn't know what he's doing. I don't take any kind of responsibility for any damages caused by following any of my advice at all. I belive every step that is required for running this tool is harmless, but I can only say "works on my machine" as every PC is different.\
\
All good? You still want to do this?\
\
\
Ok so first you'll have to install python. I'd reccomend visiting their official website ([python.org](https://www.python.org/)), they got instructions on how to do that over there. I am using python 3.11, you can use newer versions too. Older versions might also work as I will neither deliberately test and fix this program for older versions, nor will I intentionally break it for them. (I just don't bother testing other versions, because why would I?)\
\
Next you'll want to download this project. If you have git installed, `git clone https://github.com/TEX479/calculate-it-solver.git` should do the trick. If you have no idea what that last sentence even meant, you can also just download this project [here](https://github.com/TEX479/calculate-it-solver/archive/refs/heads/main.zip)\
\
Now you need to install this projects dependencies.\
If you are using linux and have pip installed, navigate a terminal to the projects folder and use the following command to install the dependencies:
```bash
pip install -r requirements.txt
```
If you are not using linux, I can only apologize and tell you to search the web on how to install requirements from a file using pip on your OS.\
\
Depending on your luck, you might need to install tkinter manually. The program will raise an error if that is the case. You'll probably find solutions by just pasting the error message to your search engine of choice and visiting the first stackexchange question that shows up.\
\
To run the UI, just use the command
```bash
python3 ui.py
```
in the root folder of the project.\
\
This should be all. If you run into any issues, you can check the issues tab [over here](https://github.com/TEX479/calculate-it-solver/issues) and check if anyone else has the same problem. If not, feel free to open a new issue and describe you problem as detailed as possible.

# Usage
This program is currently only a prototype. If you want to use it (I encourage you to do so if you know what you are doing) here is a quick overview.\
Remember, this program is not a finished product. Everything is WIP and I did not intend on shipping a perfect system that plays the game for you.\
\
If you are not a dev and just want to find solutions to your games, you are probably interested in the UI.

## how to use the ui
NOTE: The UI is subject to change. This guide may be outdated.\
\
The UI has a few entry boxes (where you can enter text) at the top. They are `current` (the number your calculator currently shows), `target` (the number you have to match), `iterations` (thing about how much the algorithm should search. bigger number means longer time to compute) and `increase iterations` (if you want to know how this is used, look at the source code). Usually you only have to change `current` and `target`. If the tool does not find a solution and you have many buttons, consider increasing the number of `iterations`.\
\
Next you have some buttons/options that controll what the program does. The `mode` changes the click-behaviour of the buttons that are underneath these controll buttons. `CALCULATE` starts the search for a solution to your maths problem. `debug` changes wether the program prints some debug info into the terminal or not (you shouldn't need this).\
\
Ok so based on what `mode` you are in, clicking any of the calculator-buttons either adds one to their ammount or subtracts one. Use this to set up the tool to have the same ammounts of each button that your in-gae calculator has. If a button is not shown, it is not yet implemented.\
\
Lastly the big box at the bottom. This wil show you the solutions it found once you hit `CALCULATE`. The output may look something like the following:
```
----------------
4.00: ['X++']
3.60: ['sub', '8', 'reverse']
3.48: ['add', '3', 'primes']
3.48: ['primes', 'add', '2']
3.48: ['add', '2', 'primes']
```
This shows all the solutions it found and how much the program likes the solution. The first number is the "cost". Lower values of "cost" mean that the solution next to it will be more optimal (for example wasting fewer buttons or not using buttons that have fewer uses left). Next to that is a list (starting and ending with square brackets `[]`). The elements of that list are showing what steps the program took to solve the puzzle. Note that this program does not show when the user has to press the evaluate button `->`, but this should be pretty straight forward: whenever there is a new operation (so not a number) after any number, just press `->`.\
\
If the program only shows
```
----------------
```
that means it did not find any solution. This can have three reasons.
1. There are no solutions that exist with the provided buttons.
2. The search interval is not big enough.
3. There is a bug somewhere preventing the code to find the solution.

The fixes corresponding to the issues are:
1. Try out buttons that are not implemented or restart the run.
2. Increase the number that is shown next to the `iterations` label
3. Get someone to fix the bug or do it yourself or open a new issue on github.
