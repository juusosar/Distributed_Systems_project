import string
import ship



def create_board(n):
    """creates n x n sizes board"""
    board = []
    for x in range(n):
        board.append(["O"] * n)
    return board

def print_board(board):
    """prints board"""
    i = 1
    
    alphabet =  string.ascii_uppercase
    coordinates = "   "
    for y in range(len(board)):
        coordinates = coordinates + alphabet[y] + " "
    
    print(coordinates)


    for row in board:
        if i <= 9:
            print(f"{i}  " + " ".join(row))
        else:
            print(f"{i} " + " ".join(row))

        i = i + 1


def set_ship(board, ship):
    """set ships on board"""

    while True:
        #asking does player want to set ship vertical or horizontal
        direction = input("Do you want this ship vertical or horizontal: ")

        
        if direction == "horizontal":
                while True:
                    try:
                        row = int(input("Enter a row where you want to place your ship:")) - 1
                        if row > 4 or row < 0:
                            print("There are not that many rows! Enter a row that is in a board")
                        else:
                            break
                    except ValueError:
                        print("Enter a number!")

                while True:
                    try:
                        column = input(f"Enter a column character from {string.ascii_uppercase[0:len(board)]} ")
                        if column.isalpha():
                            if column in string.ascii_uppercase and string.ascii_uppercase.index(column) + ship.size <= len(board):
                                index = string.ascii_uppercase.index(column)
                                break
                            else:
                                print("Enter a right character")
                        else:
                            raise TypeError
                    except TypeError:
                        print("Give a alphabet!")
               
                flag = True

                for x in range(ship.size): 
                    if board[row][index + x] == "X":
                        print("has a ship already in this position")
                        flag = False
                        break
                if flag == True:
                    for x in range(ship.size):        
                        board[row][index + x] = "X"
                    break

       

        if direction == "vertical":
            
            while True:
                try:
                    row = int(input("Enter a row where you want to place your ship:")) - 1
                    if (row > 4 or row < 0):
                        print("There are not that many rows! Enter a row that is in a board")
                    if row + ship.size > 5:
                        print("There are not that many rows! Enter a row that is in a board")
                    else:
                        break
                except ValueError:
                    print("Enter a number!")

            while True:
                try:
                    column = input(f"Enter a column character from {string.ascii_uppercase[0:len(board)]} ")
                    if column.isalpha():
                        if column in string.ascii_uppercase and string.ascii_uppercase.index(column) + ship.size <= len(board):
                            index = string.ascii_uppercase.index(column)
                            break
                        else:
                            print("Enter a right character")
                    else:
                        raise TypeError
                except TypeError:
                    print("Give a alphabet!")

            flag = True

            for x in range(ship.size): 
                if board[row + x][index] == "X":
                    print("has a ship already in this position")
                    flag = False
                    break
            if flag == True:
                for x in range(ship.size):        
                    board[row + x][index] = "X"
                break

        
def shoot(board):
    """Return coordinates where player want to shoot"""
    while True:
        try:
            row = int(input("Enter a row where you want to shoot:")) - 1
            if (row > 4 or row < 0):
                print("There are not that many rows! Enter a row that is in a board")
            if row + ship.size > 5:
                print("There are not that many rows! Enter a row that is in a board")
            else:
                break
        except ValueError:
            print("Enter a number!")

    while True:
        try:
            column = input(f"Enter a column character from {string.ascii_uppercase[0:len(board)]} where you want shoot")
            if column.isalpha():
                if column in string.ascii_uppercase and string.ascii_uppercase.index(column) + ship.size <= len(board):
                    index = string.ascii_uppercase.index(column)
                    break
                else:
                    print("Enter a right character")
            else:
                raise TypeError
        except TypeError:
            print("Give a alphabet!")
    if board[row][index] == "X":
        return True
    else:
        return False



def check_if_hit(row, column, board):
    if board[row][column] == "X":
        return True
    else:
        return False



ship = ship.Ship("Destroyer", 3)
board = create_board(5)
set_ship(board, ship)
print_board(board)
print(shoot(board))




