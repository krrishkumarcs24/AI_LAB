
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

# Knowledge Base
KB = {
    ("American", "Robert"),
    ("Missile", "T1"),
    ("Owns", "A", "T1"),
    ("Enemy", "A", "America")
}

# Rules: (premises, conclusion)
rules = [
    (
        [
            ("American", "?p"),
            ("Weapon", "?q"),
            ("Sells", "?p", "?q", "?r"),
            ("Hostile", "?r")
        ],
        ("Criminal", "?p")
    ),
    (
        [
            ("Missile", "?x"),
            ("Owns", "A", "?x")
        ],
        ("Sells", "Robert", "?x", "A")
    ),
    (
        [("Missile", "?x")],
        ("Weapon", "?x")
    ),
    (
        [("Enemy", "?x", "America")],
        ("Hostile", "?x")
    )
]


# Check whether a term is a variable
def is_variable(term):
    return isinstance(term, str) and term.startswith("?")


# Resolve variable substitutions
def resolve(term, substitution):
    while is_variable(term) and term in substitution:
        new_term = substitution[term]
        if new_term == term:
            break
        term = new_term
    return term


# Unification function
def unify(pattern, fact, substitution):
    if len(pattern) != len(fact):
        return None

    if pattern[0] != fact[0]:
        return None

    substitution = substitution.copy()

    for p, f in zip(pattern[1:], fact[1:]):
        p = resolve(p, substitution)
        f = resolve(f, substitution)

        if p == f:
            continue

        if is_variable(p):
            substitution[p] = f
        elif is_variable(f):
            substitution[f] = p
        else:
            return None

    return substitution


# Apply substitutions
def substitute(predicate, substitution):
    return tuple(
        resolve(term, substitution)
        for term in predicate
    )


# Match all premises of a rule
def match_premises(premises, facts):
    substitutions = [{}]

    for premise in premises:
        new_substitutions = []

        for substitution in substitutions:
            for fact in facts:
                result = unify(
                    substitute(premise, substitution),
                    fact,
                    substitution
                )

                if result is not None:
                    new_substitutions.append(result)

        substitutions = new_substitutions

        if not substitutions:
            break

    return substitutions


# Forward Chaining Algorithm
def forward_chaining(KB, rules, query):

    KB = set(KB)
    iteration = 1

    print("Initial Facts:")
    for fact in sorted(KB):
        print(fact)

    while True:

        new_facts = set()

        print(f"\nIteration {iteration}:")

        for premises, conclusion in rules:

            substitutions = match_premises(
                premises, KB
            )

            for substitution in substitutions:

                derived_fact = substitute(
                    conclusion, substitution
                )

                if derived_fact not in KB:
                    new_facts.add(derived_fact)

                    print("Matched:", [
                        substitute(p, substitution)
                        for p in premises
                    ])

                    print("Derived:", derived_fact)

        # Remove facts already in KB
        new_facts -= KB

        if not new_facts:
            print("No new facts. Stopping.")
            break

        KB.update(new_facts)
        iteration += 1

    print("\nFinal Knowledge Base:")

    for fact in sorted(KB):
        print(fact)

    print("\nQuery:", query)

    if query in KB:
        print("Result: TRUE")
        print("Robert is a criminal.")
    else:
        print("Result: FALSE")
        print("Could not prove that Robert is a criminal.")

    return KB


# Main function
def main():

    output = StringIO()

    with redirect_stdout(output):
        forward_chaining(
            KB,
            rules,
            ("Criminal", "Robert")
        )

    result = output.getvalue()

    print(result, end="")

    output_path = Path("output.txt")
    output_path.write_text(result, encoding="utf-8")

    print("\nOutput saved to:", output_path.resolve())


if __name__ == "__main__":
    main()
