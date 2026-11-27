
import math

def alpha_beta(depth, node, is_maximizing, values, alpha, beta):
    # Base case: Leaf node
    if depth == 3:
        return values[node]

    if is_maximizing:
        best = -math.inf

        for i in range(2):
            val = alpha_beta(
                depth + 1,
                node * 2 + i,
                False,
                values,
                alpha,
                beta
            )

            best = max(best, val)
            alpha = max(alpha, best)

            # Beta cutoff
            if beta <= alpha:
                break

        return best

    else:
        best = math.inf

        for i in range(2):
            val = alpha_beta(
                depth + 1,
                node * 2 + i,
                True,
                values,
                alpha,
                beta
            )

            best = min(best, val)
            beta = min(beta, best)

            # Alpha cutoff
            if beta <= alpha:
                break

        return best


# Leaf node values
values = [3, 5, 6, 9, 1, 2, 0, -1]

result = alpha_beta(
    0, 0, True, values, -math.inf, math.inf
)

print("Optimal value:", result)
