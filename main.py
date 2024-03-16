from functools import reduce
import math
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

root = tk.Tk()
root.geometry("312x324")
root.title("Znanstveni kalkulator")


def infix_to_postfix(infix_equation):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'log': 4}

    def extract_number(tokens, number=''):
        if tokens and (tokens[0].isdigit() or tokens[0] == '.'):
            return extract_number(tokens[1:], number + tokens[0])
        return number, tokens

    def infix_to_postfix_helper(tokens, precedence, postfix_equation=(), stack=()):
        if not tokens:
            return postfix_equation + tuple(stack[::-1])

        token, *rest = tokens

        if token.isdigit() or token == '.':
            number, remaining_tokens = extract_number(tokens)
            return infix_to_postfix_helper(remaining_tokens, precedence, postfix_equation + (number,), stack)

        elif token == '(':
            return infix_to_postfix_helper(rest, precedence, postfix_equation, stack + (token,))

        elif token == ')':
            def pop_until_left_paren(postfix, stack):
                if not stack or stack[-1] == '(':
                    return postfix, stack[:-1]
                else:
                    return pop_until_left_paren(postfix + (stack[-1],), stack[:-1])

            postfix_equation, new_stack = pop_until_left_paren(
                postfix_equation, stack)
            return infix_to_postfix_helper(rest, precedence, postfix_equation, new_stack)

        elif token == 'e':
            return infix_to_postfix_helper(rest, precedence, postfix_equation + ('2.71828',), stack)

        elif token == 'l' and rest[:2] == ['o', 'g']:
            # Skip the 'o' and 'g' tokens and push 'log' onto the stack
            if rest[2].isdigit():
                number, remaining_tokens = extract_number(rest[2:])
                return infix_to_postfix_helper(remaining_tokens, precedence, postfix_equation, stack + ('log' + number,))
            else:
                return infix_to_postfix_helper(rest[2:], precedence, postfix_equation, stack + ('log',))

        else:
            def pop_lower_precedence(postfix, stack, current_token):
                if not stack or stack[-1] == '(' or precedence[current_token] > precedence[stack[-1]]:
                    return postfix, stack
                else:
                    return pop_lower_precedence(postfix + (stack[-1],), stack[:-1], current_token)

            postfix_equation, new_stack = pop_lower_precedence(
                postfix_equation, stack, token)
            return infix_to_postfix_helper(rest, precedence, postfix_equation, new_stack + (token,))

    infix_equation_list = list(infix_equation.replace(" ", ""))
    return infix_to_postfix_helper(infix_equation_list, precedence)


infix_expression = "34^3*7-(2+3)-4+log2(45 + 5)"
postfix_equation = infix_to_postfix(infix_expression)
print(postfix_equation)


operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '^': lambda x, y: x ** y,
    'log': lambda x, base: math.log(x, base)
}


def evaluate(expression):
    def process(stack, token):
        if token.replace('.', '', 1).isdigit():
            return stack + (float(token),)
        elif token.startswith('log'):
            base = 10 if len(token) == 3 else int(token[3:])
            operand = stack[-1]
            result = operators['log'](operand, base)
            return stack[:-1] + (result,)
        elif token in operators:
            operand2 = stack[-1]
            operand1 = stack[-2]
            result = operators[token](operand1, operand2)
            return stack[:-2] + (result,)
        else:
            return stack

    stack = reduce(process, expression, ())
    return stack[0] if stack else None


def pressBtn(value):
    global expression
    expression = expression + str(value)
    textDisplay.set(expression)


def clear():
    global expression
    textDisplay.set("0")
    expression = ""


def result():
    try:
        global expression
        expression = str(evaluate(infix_to_postfix(expression)))
        textDisplay.set(expression)
    except Exception as e:
        textDisplay.set("Error")

def delete_last():
    global expression
    if expression:
        expression = expression[:-1]
        textDisplay.set(expression)


expression = ""
textDisplay = tk.StringVar()
textDisplay.set("0")

buttonFrame = tk.Frame(root)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)
buttonFrame.columnconfigure(3, weight=1)

# INPUT FIELD

inputField = tk.Entry(root, font=("Arial", 18),
                      textvariable=textDisplay, justify="right")
inputField.grid(row=0, column=0, columnspan=4, sticky="nsew")

inputField.pack(fill="both")

# PRVI RED
btnLog = tk.Button(buttonFrame, text="log", font=(
    "Arial", 18), command=lambda: pressBtn("log"))
btnLog.grid(row=1, column=0, sticky="nsew")
btnPower = tk.Button(buttonFrame, text="^", font=(
    "Arial", 18), command=lambda: pressBtn("^"))
btnPower.grid(row=1, column=1, sticky="nsew")

btnDel = tk.Button(buttonFrame, text="Del", font =("Arial", 18), command=delete_last)
btnDel.grid(row=1, column=2, sticky="nsew")
btnClear = tk.Button(buttonFrame, text="C", font=("Arial", 18), command=clear)
btnClear.grid(row=1, column=3, sticky="nsew")

# DRUGI RED
btnBO = tk.Button(buttonFrame, text="(", font=(
    "Arial", 18), command=lambda: pressBtn("("))
btnBO.grid(row=2, column=0, sticky="nsew")
btnBC = tk.Button(buttonFrame, text=")", font=(
    "Arial", 18), command=lambda: pressBtn(")"))
btnBC.grid(row=2, column=1, sticky="nsew")
btn9 = tk.Button(buttonFrame, text="e", font=("Arial", 18))
btn9.grid(row=2, column=2, sticky="nsew")
btnDevide = tk.Button(buttonFrame, text="÷", font=(
    "Arial", 18), command=lambda: pressBtn("/"))
btnDevide.grid(row=2, column=3, sticky="nsew")


# TREĆI RED
btn7 = tk.Button(buttonFrame, text="7", font=(
    "Arial", 18), command=lambda: pressBtn(7))
btn7.grid(row=3, column=0, sticky="nsew")
btn8 = tk.Button(buttonFrame, text="8", font=(
    "Arial", 18), command=lambda: pressBtn(8))
btn8.grid(row=3, column=1, sticky="nsew")
btn9 = tk.Button(buttonFrame, text="9", font=(
    "Arial", 18), command=lambda: pressBtn(9))
btn9.grid(row=3, column=2, sticky="nsew")
btnX = tk.Button(buttonFrame, text="×", font=(
    "Arial", 18), command=lambda: pressBtn("*"))
btnX.grid(row=3, column=3, sticky="nsew")

# ČETVRTI RED
btn4 = tk.Button(buttonFrame, text="4", font=(
    "Arial", 18), command=lambda: pressBtn(4))
btn4.grid(row=4, column=0, sticky="nsew")
btn5 = tk.Button(buttonFrame, text="5", font=(
    "Arial", 18), command=lambda: pressBtn(5))
btn5.grid(row=4, column=1, sticky="nsew")
btn6 = tk.Button(buttonFrame, text="6", font=(
    "Arial", 18), command=lambda: pressBtn(6))
btn6.grid(row=4, column=2, sticky="nsew")
btnMinus = tk.Button(buttonFrame, text="-", font=("Arial",
                     18), command=lambda: pressBtn("-"))
btnMinus.grid(row=4, column=3, sticky="nsew")


# PETI RED
btn1 = tk.Button(buttonFrame, text="1", font=(
    "Arial", 18), command=lambda: pressBtn(1))
btn1.grid(row=5, column=0, sticky="nsew")
btn2 = tk.Button(buttonFrame, text="2", font=(
    "Arial", 18), command=lambda: pressBtn(2))
btn2.grid(row=5, column=1, sticky="nsew")
btn3 = tk.Button(buttonFrame, text="3", font=(
    "Arial", 18), command=lambda: pressBtn(3))
btn3.grid(row=5, column=2, sticky="nsew")
btnPlus = tk.Button(buttonFrame, text="+", font=("Arial",
                    18), command=lambda: pressBtn("+"))
btnPlus.grid(row=5, column=3, sticky="nsew")

# PETI RED
btn1 = tk.Button(buttonFrame, text="", font=("Arial", 18))
btn1.grid(row=6, column=0, sticky="nsew")
btn0 = tk.Button(buttonFrame, text="0", font=(
    "Arial", 18), command=lambda: pressBtn(0))
btn0.grid(row=6, column=1, sticky="nsew")
btn3 = tk.Button(buttonFrame, text=".", font=(
    "Arial", 18), command=lambda: pressBtn("."))
btn3.grid(row=6, column=2, sticky="nsew")
btnEqual = tk.Button(buttonFrame, text="=", font=("Arial", 18), command=result)
btnEqual.grid(row=6, column=3, sticky="nsew")




buttonFrame.pack(fill="x")

root.mainloop()

print("evaluation: ", evaluate(postfix_equation))
