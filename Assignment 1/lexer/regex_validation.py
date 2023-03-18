def validate_expression(expression: str):
    if expression == '':
        return True, 'EMPTY_STRING'

    expr = expression.replace(" ", "")

    # format symbols to $
    expr = expr.replace("*", "$")
    expr = expr.replace("+", "$")
    expr = expr.replace("?", "$")

    # replace chars
    for i, char in enumerate(expr):
        if char.isalnum():
            expr = expr[:i] + '@' + expr[i + 1:]

    changed = True
    while changed:
        old_expr = expr
        expr = expr.replace('@$', 'R')
        changed = not (old_expr == expr)

    changed = True
    while changed:
        old_expr = expr
        expr = expr.replace('@', 'R')
        changed = not(old_expr == expr)

    # apply recursion rules
    changing = True
    older_expression = ''
    while changing:
        older_expression = expr

        changed = True
        while changed:
            old_expr = expr
            expr = expr.replace('R|R', 'R')
            changed = not (old_expr == expr)

        changed = True
        while changed:
            old_expr = expr
            expr = expr.replace('RR', 'R')
            changed = not (old_expr == expr)

        changed = True
        while changed:
            old_expr = expr
            expr = expr.replace('(R)$', 'R')
            changed = not (old_expr == expr)

        changed = True
        while changed:
            old_expr = expr
            expr = expr.replace('(R)', 'R')
            changed = not (old_expr == expr)

        changing = not(older_expression == expr)
        older_expression = expr

    return older_expression == 'R', older_expression

