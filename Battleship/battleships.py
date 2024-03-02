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
                    if board[row][index + x] == "S":
                        print("has a ship already in this position")
                        flag = False
                        break
                if flag == True:
                    for x in range(ship.size):        
                        board[row][index + x] = "S"
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
                if board[row + x][index] == "S":
                    print("has a ship already in this position")
                    flag = False
                    break
            if flag == True:
                for x in range(ship.size):        
                    board[row + x][index] = "S"
                break

        
def shoot(target_board, player_board):
    """Returns true if hit if not returns false"""
    while True:
        try:
            row = int(input("Enter a row where you want to shoot: ")) - 1
            if (row > 4 or row < 0):
                print("There are not that many rows! Enter a row that is in a board")
            else:
                break
        except ValueError:
            print("Enter a number!")

    while True:
        try:
            column = input(f"Enter a column character from {string.ascii_uppercase[0:len(target_board)]} where you want shoot: ")
            if column.isalpha():
                if column in string.ascii_uppercase and string.ascii_uppercase.index(column) < len(target_board):
                    index = string.ascii_uppercase.index(column)
                    break
                else:
                    print("Enter a right character")
            else:
                raise TypeError
        except TypeError:
            print("Give a alphabet!")
    if target_board[row][index] == "S":
        player_board[row][index] = "H"
        print("HIT!")
        return True
    else:
        player_board[row][index] = "M"
        print("MISS!")
        return False




def start_game(player1_username, player2_username, board_size):
    print(ship.size)
    player1_hits = 0
    player2_hits = 0

    player1_board = create_board(board_size)
    player1_shoot_board = create_board(board_size)
    player2_board = create_board(board_size)
    player2_shoot_board = create_board(board_size)

    print("Player 1 turn to set ships on board!")
    set_ship(player1_board, ship)
    print_board(player1_board)

    print("Player 2 turn to set ships on board!") 
    set_ship(player2_board, ship)
    print_board(player2_board)

    while player1_hits < ship.size and player2_hits < ship.size:

        while player1_hits < ship.size and player2_hits < ship.size:
            print("player 1 turn")
            print(player1_hits)
            print_board(player1_board)
            print_board(player1_shoot_board)
            if shoot(player2_board, player1_shoot_board) == False:
                break
            else:
                player1_hits = player1_hits + 1
                continue
        
        while player1_hits < ship.size and player2_hits < ship.size:
            print("player 2 turn")
            print(player2_hits)
            print_board(player2_board)
            print_board(player2_shoot_board)
            if shoot(player1_board, player2_shoot_board) == False:
                break
            else:
                player2_hits = player2_hits + 1
                continue

    if player1_hits == ship.size:
        return "player1", "player2"
    else:
        return "player2", "player1"

ship = ship.Ship("Destroyer", 3)

print(start_game(ship, 5))
#board = create_board(5)
#set_ship(board, ship)
#print_board(board)
#print(shoot(board))
#print_board(board)




