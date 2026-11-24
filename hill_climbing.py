
def calculate_cost(state):
    """
    Calculates heuristic cost h(s): the number of pairs of queens
    attacking each other directly or indirectly (row or diagonal).
    """
    attacking_pairs = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):
            # Check for same row attack
            if state[i] == state[j]:
                attacking_pairs += 1

            # Check for diagonal attack
            elif abs(state[i] - state[j]) == abs(i - j):
                attacking_pairs += 1

    return attacking_pairs


def get_successors(state):
    """
    Generates all successors by moving a single queen to another row
    in its column (4 * 3 = 12 successors for a 4x4 board).
    """
    successors = []
    n = len(state)

    for col in range(n):
        for row in range(n):
            if row != state[col]:
                next_state = list(state)
                next_state[col] = row
                successors.append(tuple(next_state))

    return successors


def hill_climbing(initial_state):
    """
    Steepest-descent Hill Climbing algorithm minimizing
    attacking pairs h(s).
    """
    current = tuple(initial_state)
    current_cost = calculate_cost(current)

    print(f"Initial State: {current}, Heuristic Cost (Attacking Pairs h): {current_cost}")

    step = 0

    while True:
        step += 1
        successors = get_successors(current)

        best_successor = None
        best_cost = current_cost

        for succ in successors:
            cost = calculate_cost(succ)

            if cost < best_cost:
                best_cost = cost
                best_successor = succ
        if best_successor is None:
            print(f"Terminated at step {step}: Local/Global optimum reached.")
            break

        print(f"Step {step}: Move from {current} (h = {current_cost}) -> {best_successor} (h={best_cost})")

        current = best_successor
        current_cost = best_cost

    return current, current_cost

initial_state = (1, 1, 0, 2)

final_state, final_cost = hill_climbing(initial_state)

print(f"\nFinal Answer State: {final_state}")
print(f"Final Cost h(s): {final_cost}")
