import tkinter as tk

N = 8
sol = [[-1 for _ in range(N)] for _ in range(N)]

# Check if place is in range and not assigned yet
def isValid(x, y):
    return (x >= 0 and x < N and y >= 0 and y < N and sol[x][y] == -1)

# Function to print the solution in the terminal
def printSolution():
    for i in range(N):
        for j in range(N):
            print(f"{sol[i][j]:2}", end=" ")
        print()

# Recursive function to solve the Knight's Tour problem
def knightTour(x, y, move, xMove, yMove):
    if move == N * N:  # If all squares are visited
        printSolution()  # Print the solution in the terminal
        return True

    for k in range(8):  # Try all possible moves
        xNext = x + xMove[k]
        yNext = y + yMove[k]
        if isValid(xNext, yNext):
            sol[xNext][yNext] = move
            updateBoard(xNext, yNext, move)  # Update GUI board
            if knightTour(xNext, yNext, move + 1, xMove, yMove):  # Recursion
                return True
            sol[xNext][yNext] = -1  # Backtracking
            updateBoard(xNext, yNext, -1)  # Update GUI board

    return False  # If no moves lead to a solution, return False

# Function to update the GUI board
def updateBoard(x, y, move):
    if move == -1:
        buttons[x][y].config(text="", bg="white")
    else:
        buttons[x][y].config(text=str(move), bg="lightblue")
    window.update_idletasks()

# Start the Knight's Tour
def findKnightTourSol():
    resetBoard()
    xMove = [2, 1, -1, -2, -2, -1, 1, 2]
    yMove = [1, 2, 2, 1, -1, -2, -2, -1]
    sol[0][0] = 0
    updateBoard(0, 0, 0)
    if not knightTour(0, 0, 1, xMove, yMove):
        label_status.config(text="Solution does not exist")
    else:
        label_status.config(text="Solution Found")

# Function to reset the board
def resetBoard():
    for i in range(N):
        for j in range(N):
            sol[i][j] = -1
            buttons[i][j].config(text="", bg="white")
    label_status.config(text="")

# Set up the main GUI window
window = tk.Tk()
window.title("Knight's Tour")

# Create a grid of buttons
buttons = [[None for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        button = tk.Button(window, text="", width=4, height=2, bg="white",
                           font=("Helvetica", 16))
        button.grid(row=i, column=j)
        buttons[i][j] = button

# Add a status label
label_status = tk.Label(window, text="", font=("Helvetica", 16))
label_status.grid(row=N, column=0, columnspan=N)

# Add a start button
button_start = tk.Button(window, text="Start", command=findKnightTourSol, font=("Helvetica", 16))
button_start.grid(row=N + 1, column=0, columnspan=N//2)

# Add a reset button
button_reset = tk.Button(window, text="Reset", command=resetBoard, font=("Helvetica", 16))
button_reset.grid(row=N + 1, column=N//2, columnspan=N//2)

# Start the GUI loop
window.mainloop()



# # Size of the chessboard
# N = 8

# # Initialize the solution matrix with -1 (unvisited)
# sol = [[-1 for _ in range(N)] for _ in range(N)]

# # Possible moves for a knight
# xMove = [2, 1, -1, -2, -2, -1, 1, 2]
# yMove = [1, 2, 2, 1, -1, -2, -2, -1]

# # Check if x, y are valid indices for the N*N chessboard
# def isValid(x, y):
#     return (x >= 0 and x < N and y >= 0 and y < N and sol[x][y] == -1)

# # Function to print the solution matrix
# def printSolution():
#     for i in range(N):
#         for j in range(N):
#             print(f"{sol[i][j]:2}", end=" ")
#         print()

# # Recursive function to solve the Knight's Tour problem
# def knightTour(x, y, move):
#     # If all squares are visited
#     if move == N * N:
#         return True

#     # Try all possible moves from the current position
#     for k in range(8):
#         xNext = x + xMove[k]
#         yNext = y + yMove[k]
#         if isValid(xNext, yNext):
#             sol[xNext][yNext] = move
#             if knightTour(xNext, yNext, move + 1):  # Recursion
#                 return True
#             sol[xNext][yNext] = -1  # Backtracking

#     return False

# # Function to initiate the Knight's Tour
# def solveKnightTour():
#     # Start the knight at the first block (0, 0)
#     sol[0][0] = 0

#     # Start the tour from position (0, 0) and move number 1
#     if knightTour(0, 0, 1):
#         print("Solution exists:")
#         printSolution()
#     else:
#         print("Solution does not exist")

# # Start the Knight's Tour problem
# solveKnightTour()



"""import tkinter as tk

N = 8
sol = [[-1 for _ in range(N)] for _ in range(N)]

# Check if place is in range and not assigned yet
def isValid(x, y):
    return (x >= 0 and x < N and y >= 0 and y < N and sol[x][y] == -1)

# Recursive generator function to solve the problem
def knightTour(x, y, move, xMove, yMove):
    if move == N * N:
        yield True
    for k in range(8):
        xNext = x + xMove[k]
        yNext = y + yMove[k]
        if isValid(xNext, yNext):
            sol[xNext][yNext] = move
            updateBoard(xNext, yNext, move)  # Update GUI board
            yield from knightTour(xNext, yNext, move + 1, xMove, yMove)
            sol[xNext][yNext] = -1  # Backtracking
            updateBoard(xNext, yNext, -1)  # Update GUI board
    yield False

# Function to update the GUI board
def updateBoard(x, y, move):
    if move == -1:
        buttons[x][y].config(text="", bg="white")
    else:
        buttons[x][y].config(text=str(move), bg="lightblue")
    window.update_idletasks()

# Start the Knight's Tour
def findKnightTourSol():
    resetBoard()
    xMove = [2, 1, -1, -2, -2, -1, 1, 2]
    yMove = [1, 2, 2, 1, -1, -2, -2, -1]
    sol[0][0] = 0
    updateBoard(0, 0, 0)
    global tour_generator
    tour_generator = knightTour(0, 0, 1, xMove, yMove)
    window.after(1, nextMove)

# Function to make the next move
def nextMove():
    try:
        result = next(tour_generator)
        if result:
            label_status.config(text="Solution Found")
        else:
            window.after(1, nextMove)
    except StopIteration:
        label_status.config(text="Solution does not exist")

# Function to reset the board
def resetBoard():
    for i in range(N):
        for j in range(N):
            sol[i][j] = -1
            buttons[i][j].config(text="", bg="white")
    label_status.config(text="")

# Set up the main GUI window
window = tk.Tk()
window.title("Knight's Tour")

# Create a grid of buttons
buttons = [[None for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        button = tk.Button(window, text="", width=4, height=2, bg="white",
                           font=("Helvetica", 16))
        button.grid(row=i, column=j)
        buttons[i][j] = button

# Add a status label
label_status = tk.Label(window, text="", font=("Helvetica", 16))
label_status.grid(row=N, column=0, columnspan=N)

# Add a start button
button_start = tk.Button(window, text="Start", command=findKnightTourSol, font=("Helvetica", 16))
button_start.grid(row=N + 1, column=0, columnspan=N//2)

# Add a reset button
button_reset = tk.Button(window, text="Reset", command=resetBoard, font=("Helvetica", 16))
button_reset.grid(row=N + 1, column=N//2, columnspan=N//2)

# Start the GUI loop
window.mainloop()
"""
"""import tkinter as tk

# Initial position of Knight
x, y = 0, 0
# Define the chessboard size
N = 8
# A 2D chessboard
chessboard = [[-1 for x in range(N)] for y in range(N)]
# Move patterns of Knight
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

# Function to check if the move is valid
def is_valid(x, y, chessboard):
    if x < 0 or y < 0 or x >= N or y >= N or chessboard[x][y] != -1:
        return False
    return True

# Function for Knight's Tour
def knight_tour(x, y, movei, chessboard, gui_update_func):
    chessboard[x][y] = movei
    gui_update_func(chessboard)  # Update the GUI after each move
    if movei == N*N-1:
        return True

    for i in range(8):
        new_x = x + dx[i]
        new_y = y + dy[i]
        if is_valid(new_x, new_y, chessboard):
            if knight_tour(new_x, new_y, movei+1, chessboard, gui_update_func):
                return True

    chessboard[x][y] = -1
    gui_update_func(chessboard)  # Revert the GUI if backtracking
    return False

# Function to update the GUI
def update_gui(chessboard):
    for i in range(N):
        for j in range(N):
            if chessboard[i][j] == -1:
                buttons[i][j].config(text="", bg="white")
            else:
                buttons[i][j].config(text=str(chessboard[i][j]), bg="lightblue")
    root.update()

def start_tour():
    reset_board()
    if knight_tour(x, y, 0, chessboard, update_gui):
        message_label.config(text="Solution Found!")
    else:
        message_label.config(text="Solution Not Found!")

def reset_board():
    global chessboard
    chessboard = [[-1 for x in range(N)] for y in range(N)]
    update_gui(chessboard)
    message_label.config(text="")

# Create the GUI
root = tk.Tk()
root.title("Knight's Tour")

buttons = [[None for _ in range(N)] for _ in range(N)]

for i in range(N):
    for j in range(N):
        button = tk.Button(root, text="", width=4, height=2, font=("Arial", 14), bg="white")
        button.grid(row=i, column=j, padx=1, pady=1)
        buttons[i][j] = button

start_button = tk.Button(root, text="Start Tour", command=start_tour, font=("Arial", 14))
start_button.grid(row=N, column=0, columnspan=N//2)

reset_button = tk.Button(root, text="Reset", command=reset_board, font=("Arial", 14))
reset_button.grid(row=N, column=N//2, columnspan=N//2)

message_label = tk.Label(root, text="", font=("Arial", 14))
message_label.grid(row=N+1, column=0, columnspan=N)

root.mainloop()"""