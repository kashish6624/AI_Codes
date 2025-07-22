import tkinter as tk
from tkinter import messagebox

# Define constants
X = 3  # Computer's move
O = 5  # User's move
BLANK = 2
board = [BLANK] * 10  # 1-based index; ignore index 0
turn = 1
user_symbol = None
computer_symbol = None
buttons = []

def reset_board():
    global board, turn, buttons
    board = [BLANK] * 10
    turn = 1
    for button in buttons:
        button.config(text="", state="normal")
    choose_symbol()

def check_winner():
    # Possible winning combinations
    winning_combinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Rows
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
        [1, 5, 9], [3, 5, 7]              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != BLANK:
            return board[combo[0]]
    return None

def end_game(winner):
    if winner == computer_symbol:
        messagebox.showinfo("Game Over", "Computer wins!")
    elif winner == user_symbol:
        messagebox.showinfo("Game Over", "You win!")
    else:
        messagebox.showinfo("Game Over", "It's a draw!")
    reset_board()

def make2():
    if board[5] == BLANK:
        return 5
    for i in [2, 4, 6, 8]:
        if board[i] == BLANK:
            return i
    return -1

def posswin(p):
    # Rows
    for i in [1, 4, 7]:
        product = board[i] * board[i+1] * board[i+2]
        if product == p * p * BLANK:
            for j in range(i, i+3):
                if board[j] == BLANK:
                    return j

    # Columns
    for i in [1, 2, 3]:
        product = board[i] * board[i+3] * board[i+6]
        if product == p * p * BLANK:
            for j in [i, i+3, i+6]:
                if board[j] == BLANK:
                    return j

    # Diagonals
    product = board[1] * board[5] * board[9]
    if product == p * p * BLANK:
        for i in [1, 5, 9]:
            if board[i] == BLANK:
                return i

    product = board[3] * board[5] * board[7]
    if product == p * p * BLANK:
        for i in [3, 5, 7]:
            if board[i] == BLANK:
                return i

    return 0

def go(n, symbol):
    global turn
    board[n] = symbol
    buttons[n-1].config(text="X" if symbol == X else "O", state="disabled")
    turn += 1

def play_computer():
    global turn
    if turn == 1:
        go(1, computer_symbol)
    elif turn == 2:
        go(5 if board[5] == BLANK else 1, computer_symbol)
    elif turn == 3:
        go(9 if board[9] == BLANK else 3, computer_symbol)
    elif turn == 4:
        if posswin(computer_symbol):
            go(posswin(computer_symbol), computer_symbol)
        else:
            go(make2(), computer_symbol)
    elif turn == 5:
        if posswin(computer_symbol):
            go(posswin(computer_symbol), computer_symbol)
        elif posswin(user_symbol):
            go(posswin(user_symbol), computer_symbol)
        else:
            go(7 if board[7] == BLANK else 3, computer_symbol)
    elif turn == 6:
        if posswin(user_symbol):
            go(posswin(user_symbol), computer_symbol)
        elif posswin(computer_symbol):
            go(posswin(computer_symbol), computer_symbol)
        else:
            go(make2(), computer_symbol)
    elif turn == 7:
        if posswin(computer_symbol):
            go(posswin(computer_symbol), computer_symbol)
        elif posswin(user_symbol):
            go(posswin(user_symbol), computer_symbol)
        else:
            for i in range(1, 10):
                if board[i] == BLANK:
                    go(i, computer_symbol)
                    break
    elif turn == 8:
        if posswin(user_symbol):
            go(posswin(user_symbol), computer_symbol)
        elif posswin(computer_symbol):
            go(posswin(computer_symbol), computer_symbol)
        else:
            for i in range(1, 10):
                if board[i] == BLANK:
                    go(i, computer_symbol)
                    break
    elif turn == 9:
        if posswin(computer_symbol):
            go(posswin(computer_symbol), computer_symbol)
        elif posswin(user_symbol):
            go(posswin(user_symbol), computer_symbol)
        else:
            for i in range(1, 10):
                if board[i] == BLANK:
                    go(i, computer_symbol)
                    break
    winner = check_winner()
    if winner or turn > 9:
        end_game(winner)

def on_button_click(index):
    go(index+1, user_symbol)
    winner = check_winner()
    if winner or turn > 9:
        end_game(winner)
    else:
        play_computer()

def choose_symbol():
    global user_symbol, computer_symbol, turn
    choice = messagebox.askquestion("Choose Symbol", "Do you want to be X?")
    if choice == "yes":
        user_symbol = X
        computer_symbol = O
    else:
        user_symbol = O
        computer_symbol = X
    
    play_first = messagebox.askquestion("Play First?", "Do you want to play first?")
    if play_first == "no":
        turn = 1
        play_computer()
    else:
        turn = 1

def quit_game():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def create_gui():
    global buttons, root
    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    # Title Label
    title_label = tk.Label(root, text="Tic-Tac-Toe", font="Arial 24 bold", pady=10)
    title_label.grid(row=0, column=0, columnspan=3)

    # Tic-Tac-Toe Buttons
    for i in range(9):
        button = tk.Button(root, text="", font="Arial 20 bold", height=3, width=6, bg="#f0f0f0",
                           activebackground="#e0e0e0", command=lambda i=i: on_button_click(i))
        button.grid(row=(i//3) + 1, column=i%3, padx=5, pady=5)
        buttons.append(button)

    # Reset Button
    reset_button = tk.Button(root, text="Reset", font="Arial 15", bg="#d9534f", fg="white",
                             activebackground="#c9302c", command=reset_board)
    reset_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Quit Button
    quit_button = tk.Button(root, text="Quit", font="Arial 15", bg="#5bc0de", fg="white",
                            activebackground="#31b0d5", command=quit_game)
    quit_button.grid(row=4, column=2, pady=10)

    choose_symbol()
    
    root.mainloop()

create_gui()




# import random

# def drawBoard(board):
#     """Prints out the board that it was passed."""
#     print('   |   |')
#     print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
#     print('   |   |')
#     print('-----------')
#     print('   |   |')
#     print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
#     print('   |   |')
#     print('-----------')
#     print('   |   |')
#     print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
#     print('   |   |')

# def inputPlayerLetter():
#     """Lets the player type which letter they want to be."""
#     letter = ''
#     while letter not in ['X', 'O']:
#         print('Do you want to be X or O?')
#         letter = input().upper()
#     return ['X', 'O'] if letter == 'X' else ['O', 'X']

# def whoGoesFirst():
#     """Randomly choose the player who goes first."""
#     return 'computer' if random.randint(0, 1) == 0 else 'player'

# def playAgain():
#     """Returns True if the player wants to play again, otherwise False."""
#     print('Do you want to play again? (yes or no)')
#     return input().lower().startswith('y')

# def makeMove(board, letter, move):
#     board[move] = letter

# def isWinner(board, letter):
#     """Returns True if the player has won."""
#     return (
#         (board[7] == letter and board[8] == letter and board[9] == letter) or  # across the top
#         (board[4] == letter and board[5] == letter and board[6] == letter) or  # across the middle
#         (board[1] == letter and board[2] == letter and board[3] == letter) or  # across the bottom
#         (board[7] == letter and board[4] == letter and board[1] == letter) or  # down the left side
#         (board[8] == letter and board[5] == letter and board[2] == letter) or  # down the middle
#         (board[9] == letter and board[6] == letter and board[3] == letter) or  # down the right side
#         (board[7] == letter and board[5] == letter and board[3] == letter) or  # diagonal
#         (board[9] == letter and board[5] == letter and board[1] == letter)     # diagonal
#     )

# def getBoardCopy(board):
#     """Make a duplicate of the board list and return it."""
#     return board[:]

# def isSpaceFree(board, move):
#     """Return True if the passed move is free on the passed board."""
#     return board[move] == ' '

# def getPlayerMove(board):
#     """Let the player type in their move."""
#     move = ' '
#     while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
#         print('What is your next move? (1-9)')
#         move = input()
#     return int(move)

# def chooseRandomMoveFromList(board, movesList):
#     """Returns a valid move from the passed list on the passed board."""
#     possibleMoves = [i for i in movesList if isSpaceFree(board, i)]
#     return random.choice(possibleMoves) if possibleMoves else None

# def getComputerMove(board, computerLetter):
#     """Determine where the computer should move and return that move."""
#     playerLetter = 'O' if computerLetter == 'X' else 'X'

#     # Check if computer can win in the next move
#     for i in range(1, 10):
#         copy = getBoardCopy(board)
#         if isSpaceFree(copy, i):
#             makeMove(copy, computerLetter, i)
#             if isWinner(copy, computerLetter):
#                 return i

#     # Check if player could win on their next move, and block them
#     for i in range(1, 10):
#         copy = getBoardCopy(board)
#         if isSpaceFree(copy, i):
#             makeMove(copy, playerLetter, i)
#             if isWinner(copy, playerLetter):
#                 return i

#     # Try to take one of the corners, if they are free
#     move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
#     if move is not None:
#         return move

#     # Try to take the center, if it is free
#     if isSpaceFree(board, 5):
#         return 5

#     # Move on one of the sides
#     return chooseRandomMoveFromList(board, [2, 4, 6, 8])

# def isBoardFull(board):
#     """Return True if every space on the board has been taken."""
#     return all(not isSpaceFree(board, i) for i in range(1, 10))

# print('Welcome to Tic Tac Toe!')

# while True:
#     # Reset the board
#     theBoard = [' '] * 10
#     playerLetter, computerLetter = inputPlayerLetter()
#     turn = whoGoesFirst()
#     print('The ' + turn + ' will go first.')

#     gameIsPlaying = True

#     while gameIsPlaying:
#         if turn == 'player':
#             # Player’s turn
#             drawBoard(theBoard)
#             move = getPlayerMove(theBoard)
#             makeMove(theBoard, playerLetter, move)

#             if isWinner(theBoard, playerLetter):
#                 drawBoard(theBoard)
#                 print('Hooray! You have won the game!')
#                 gameIsPlaying = False
#             else:
#                 if isBoardFull(theBoard):
#                     drawBoard(theBoard)
#                     print('The game is a tie!')
#                     break
#                 else:
#                     turn = 'computer'
#         else:
#             # Computer’s turn
#             move = getComputerMove(theBoard, computerLetter)
#             makeMove(theBoard, computerLetter, move)

#             if isWinner(theBoard, computerLetter):
#                 drawBoard(theBoard)
#                 print('The computer has beaten you! You lose.')
#                 gameIsPlaying = False
#             else:
#                 if isBoardFull(theBoard):
#                     drawBoard(theBoard)
#                     print('The game is a tie!')
#                     break
#                 else:
#                     turn = 'player'

#     if not playAgain():
#         break


