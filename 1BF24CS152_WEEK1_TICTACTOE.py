board = [" " for i in range(0, 9)]


def display_board():

    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("---------")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("---------")
    print(f"{board[6]} | {board[7]} | {board[8]}")


def check_winner():

    if board[0] == board[1] == board[2] != " ":
        return board[0]

    elif board[3] == board[4] == board[5] != " ":
        return board[3]

    elif board[6] == board[7] == board[8] != " ":
        return board[6]

    elif board[0] == board[3] == board[6] != " ":
        return board[0]

    elif board[1] == board[4] == board[7] != " ":
        return board[1]

    elif board[2] == board[5] == board[8] != " ":
        return board[2]

    elif board[0] == board[4] == board[8] != " ":
        return board[0]

    elif board[2] == board[4] == board[6] != " ":
        return board[2]

    return None


display_board()

# There can be maximum 9 moves
for i in range(0, 9):

    # Player 1
    while True:

        position1 = int(input("Enter position for Player 1 (0-8): "))

        if position1 >= 0 and position1 <= 8:

            if board[position1] == " ":
                board[position1] = "X"
                break

            else:
                print("Space is occupied")

        else:
            print("Enter position between 0 and 8")

    display_board()

    # Check Player 1 winner
    winner = check_winner()

    if winner is not None:
        print(f"Player {winner} wins")
        break

    # Check draw after Player 1's move
    if i == 4:
        print("Draw")
        break


    # Player 2
    while True:

        position2 = int(input("Enter position for Player 2 (0-8): "))

        if position2 >= 0 and position2 <= 8:

            if board[position2] == " ":
                board[position2] = "O"
                break

            else:
                print("Space is occupied")

        else:
            print("Enter position between 0 and 8")

    display_board()

    # Check Player 2 winner
    winner = check_winner()

    if winner is not None:
        print(f"Player {winner} wins")
        break

else:
    print("Draw")