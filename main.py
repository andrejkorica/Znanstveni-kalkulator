def infix_to_postfix(infix_equation):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

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

            postfix_equation, new_stack = pop_until_left_paren(postfix_equation, stack)
            return infix_to_postfix_helper(rest, precedence, postfix_equation, new_stack)

        elif token == 'e':
            return infix_to_postfix_helper(rest, precedence, postfix_equation + ('2.71828',), stack)

        else:
            def pop_lower_precedence(postfix, stack, current_token):
                if not stack or stack[-1] == '(' or precedence[current_token] > precedence[stack[-1]]:
                    return postfix, stack
                else:
                    return pop_lower_precedence(postfix + (stack[-1],), stack[:-1], current_token)

            postfix_equation, new_stack = pop_lower_precedence(postfix_equation, stack, token)
            return infix_to_postfix_helper(rest, precedence, postfix_equation, new_stack + (token,))

    infix_equation_list = list(infix_equation.replace(" ", ""))
    return infix_to_postfix_helper(infix_equation_list, precedence)


infix_expression = "34^3*7-(2+3)-4+e^45"
postfix_equation = infix_to_postfix(infix_expression)
print(postfix_equation)


def evaluate(expression, stack=()):
    operators = {'+': lambda x, y: x + y,
                 '-': lambda x, y: x - y,
                 '*': lambda x, y: x * y,
                 '/': lambda x, y: x / y,
                 '^': lambda x, y: x ** y}

    if not expression:
        return stack[0]

    token, *rest = expression

    if token.replace('.', '', 1).isdigit():
        new_stack = stack + (float(token),)
    elif token in operators:
        if token == 'e':
            operand = stack[-1]
            result = operators[token](operand)
            new_stack = stack[:-1] + (result,)
        else:
            operand2 = stack[-1]
            operand1 = stack[-2]
            result = operators[token](operand1, operand2)
            new_stack = stack[:-2] + (result,)
    else:
        new_stack = stack

    return evaluate(rest, new_stack)


print("evaluation: ", evaluate(postfix_equation))
