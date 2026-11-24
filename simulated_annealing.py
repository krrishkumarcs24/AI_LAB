import random
import math

def get_user_input(n):
    board = []
    print(f"Enter the row positions (0 to {n-1}) of the queens for each column:")
    for col in range(n):
        while True:
            try:
                row = int(input(f"Column {col}: "))
                if 0 <= row < n:
                    board.append(row)
                    break
                else:
                    print(f"Invalid input. Please enter a number between 0 and {n-1}.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
    return board

def print_board(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            line += " Q " if board[col] == row else " . "
        print(line)
    print()

def heuristic(board):
    n = len(board)
    attacks = 0
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks

def random_neighbor(board):
    n = len(board)
    neighbor = list(board)
    col = random.randint(0, n-1)
    row = random.randint(0, n-1)
    while row == neighbor[col]:
        row = random.randint(0, n-1)
    neighbor[col] = row
    return neighbor

def simulated_annealing(n=8, max_iter=100000, initial_temp=100, cooling_rate=0.995):
    current_board = get_user_input(n)
    current_heuristic = heuristic(current_board)
    temperature = initial_temp
    iteration = 0

    print(f"Initial heuristic: {current_heuristic}")
    print_board(current_board)

    while temperature > 0.1 and current_heuristic > 0 and iteration < max_iter:
        neighbor = random_neighbor(current_board)
        neighbor_heuristic = heuristic(neighbor)
        delta_e = current_heuristic - neighbor_heuristic

        if delta_e > 0:
            current_board = neighbor
            current_heuristic = neighbor_heuristic
        else:
            probability = math.exp(delta_e / temperature)
            if random.random() < probability:
                current_board = neighbor
                current_heuristic = neighbor_heuristic

        temperature *= cooling_rate
        iteration += 1

        if iteration % 1000 == 0:
            print(f"Iteration {iteration}, Temperature: {temperature:.2f}, Heuristic: {current_heuristic}")
            print_board(current_board)

    if current_heuristic == 0:
        print("Solution found!")
    else:
        print("Stopped without full solution. Best board found:")
    print(f"Final heuristic: {current_heuristic}")
    print_board(current_board)

if __name__ == "__main__":
    simulated_annealing()