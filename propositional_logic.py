
import itertools
import pandas as pd
import re

# Evaluate a logical expression
def pl_true(expr, model):
    expr = expr.replace("→", "=>")
    expr = expr.replace("¬", " not ")
    expr = expr.replace("V", " or ")

    # Replace implication
    if "=>" in expr:
        left, right = expr.split("=>", 1)
        expr = f"(not ({left.strip()}) or ({right.strip()}))"

    # Replace symbols with truth values
    for sym, val in model.items():
        expr = re.sub(rf'\b{sym}\b', str(val), expr)

    return eval(expr)


# Extract propositional symbols
def get_symbols(KB, alpha):
    symbols = set()

    for sentence in KB + [alpha]:
        for token in re.findall(r'\b[A-Z]\b', sentence):
            symbols.add(token)

    return sorted(symbols)


# Truth table enumeration
def tt_entails(KB, alpha):
    symbols = get_symbols(KB, alpha)
    rows = []
    entails = True

    for values in itertools.product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))

        # Evaluate each KB sentence separately
        kb_values = [pl_true(sentence, model) for sentence in KB]

        # Evaluate complete KB
        kb_val = all(kb_values)

        # Evaluate query
        alpha_val = pl_true(alpha, model)

        # Store individual sentence results
        row = {**model}

        for i, sentence in enumerate(KB):
            row[sentence] = kb_values[i]

        row["KB"] = kb_val
        row["Query"] = alpha_val

        rows.append(row)

        if kb_val and not alpha_val:
            entails = False

    # Display truth table
    df = pd.DataFrame(rows)

    print("\nTRUTH TABLE")
    print("=" * 60)
    print(df.to_string(index=False))
    print("=" * 60)

    if entails:
        print("KB ENTAILS QUERY: YES")
    else:
        print("KB ENTAILS QUERY: NO")

    return entails


# Main program
print("Enter Knowledge Base sentences separated by commas")
print("Operators: and, or, not, →, ¬, V")

kb_input = input("KB: ")
KB = [x.strip() for x in kb_input.split(",")]

alpha = input("Enter query: ")

tt_entails(KB, alpha)