
import re

def parse_input(expr_str):
    expr_str = expr_str.strip()

    if not expr_str:
        raise ValueError("Empty expression")

    tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|[(),]', expr_str)

    if ''.join(tokens) != re.sub(r'\s+', '', expr_str):
        raise ValueError("Invalid expression syntax")

    pos = 0

    def parse_term():
        nonlocal pos

        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")

        name = tokens[pos]

        if name in '(),':
            raise ValueError("Expected a term")

        pos += 1

        if pos < len(tokens) and tokens[pos] == '(':
            pos += 1
            args = []

            if pos < len(tokens) and tokens[pos] == ')':
                pos += 1
                return [name]

            while True:
                args.append(parse_term())

                if pos >= len(tokens):
                    raise ValueError("Missing closing parenthesis")

                if tokens[pos] == ',':
                    pos += 1
                elif tokens[pos] == ')':
                    pos += 1
                    break
                else:
                    raise ValueError("Expected comma or closing parenthesis")

            return [name] + args

        return name

    result = parse_term()

    if pos != len(tokens):
        raise ValueError("Unexpected extra tokens")

    return result


def is_variable(x):
    return isinstance(x, str) and x[0].islower()


def apply_substitution(theta, expr):

    if is_variable(expr):
        if expr in theta:
            return apply_substitution(theta, theta[expr])
        return expr

    if isinstance(expr, list):
        return [
            expr[0]
        ] + [
            apply_substitution(theta, arg)
            for arg in expr[1:]
        ]

    return expr


def occurs_in(var, expr, theta):

    expr = apply_substitution(theta, expr)

    if var == expr:
        return True

    if isinstance(expr, list):
        return any(
            occurs_in(var, arg, theta)
            for arg in expr[1:]
        )

    return False

def format_expr(expr):

    if isinstance(expr, list):
        return (
            expr[0] + "(" +
            ", ".join(format_expr(arg) for arg in expr[1:]) +
            ")"
        )

    return str(expr)


def format_theta(theta):

    if not theta:
        return "theta={}"

    items = []

    for key, value in theta.items():
        items.append(
            f"{key}/{format_expr(apply_substitution(theta, value))}"
        )

    return "theta={ " + ", ".join(items) + " }"


def unify(expr1, expr2, theta, trace_steps):

    expr1 = apply_substitution(theta, expr1)
    expr2 = apply_substitution(theta, expr2)

    if expr1 == expr2:
        return theta

    if is_variable(expr1):

        if occurs_in(expr1, expr2, theta):
            return None

        theta = theta.copy()
        theta[expr1] = expr2

        trace_steps.append(
            (
                format_expr(expr1),
                format_expr(expr2),
                format_theta(theta)
            )
        )

        return theta

    if is_variable(expr2):

        if occurs_in(expr2, expr1, theta):
            return None

        theta = theta.copy()
        theta[expr2] = expr1

        trace_steps.append(
            (
                format_expr(expr2),
                format_expr(expr1),
                format_theta(theta)
            )
        )

        return theta

    # Case 4: Both are compound expressions
    if isinstance(expr1, list) and isinstance(expr2, list):

        if expr1[0] != expr2[0]:
            return None

        if len(expr1) != len(expr2):
            return None

        for i in range(1, len(expr1)):

            theta = unify(
                expr1[i],
                expr2[i],
                theta,
                trace_steps
            )

            if theta is None:
                return None

        return theta

    # Case 5: Constants do not match
    return None


def run_unification_trace(expr1, expr2):

    print("\nInput 1:", format_expr(expr1))
    print("Input 2:", format_expr(expr2))

    theta = {}
    trace_steps = []

    print("\nS0 = {" +
          format_expr(expr1) + ", " +
          format_expr(expr2) + "}")

    print(format_theta(theta))

    success = unify(
        expr1,
        expr2,
        theta,
        trace_steps
    )

    if success is not None:

        for i, (var, value, substitution) in enumerate(
            trace_steps, start=1
        ):
            print(f"\nS{i} = {{ {var} = {value} }}")
            print(substitution)

        print("\nFinal Substitution:")
        print(format_theta(success))

        print("\nSUCCESS")

    else:
        print("\nFAILURE")
        print("Expressions cannot be unified.")


if __name__ == "__main__":

    print("-----------------------------------------")
    print(" FIRST ORDER LOGIC UNIFICATION")
    print(" Nested Functions Supported")
    print("-----------------------------------------")

    try:
        raw_input1 = input(
            "\nEnter Input 1 (e.g., F(G(x),H(y))): "
        )

        raw_input2 = input(
            "Enter Input 2 (e.g., F(z,H(Apple))): "
        )

        parsed_f1 = parse_input(raw_input1)
        parsed_f2 = parse_input(raw_input2)

        run_unification_trace(parsed_f1, parsed_f2)

    except ValueError as error:
        print("\nInput Error:", error)
