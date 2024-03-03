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

def turn(username, player_board, player_shoot_board, target_board):
    print(f"{username}'s turn")  
    print_board(player_board)
    print_board(player_shoot_board)
    result = shoot(target_board, player_shoot_board)
    return result


def start_game(player1_username, player2_username, ship_list, board_size):
    
    player1_hits = 0
    player2_hits = 0
    hitpoints = 0
    for x in range(0, len(ship_list)):
        hitpoints += ship_list[x].size

    player1_board = create_board(board_size)
    player1_shoot_board = create_board(board_size)
    player2_board = create_board(board_size)
    player2_shoot_board = create_board(board_size)

    for x in ship_list:
        print(f"{player1_username}'s turn to set ships on board!")
        set_ship(player1_board, x)
        print_board(player1_board)

    for y in ship_list:
        print(f"{player2_username}'s turn to set ships on board!") 
        set_ship(player2_board, y)
        print_board(player2_board)

    while player1_hits < hitpoints and player2_hits < hitpoints:

        while player1_hits < hitpoints and player2_hits < hitpoints:
            
            result = turn(player1_username, player1_board, player1_shoot_board, player2_board)
            if result == False:
                break
            else:
                player1_hits = player1_hits + 1
                continue
        
        while player1_hits < hitpoints and player2_hits < hitpoints:
            result = turn(player2_username, player2_board, player2_shoot_board, player1_board)
            if result == False:
                break
            else:
                player2_hits = player2_hits + 1
                continue

    if player1_hits == hitpoints:
        return player1_username, player2_username
    else:
        return player2_username, player1_username


ship_list = list()
ship1 = ship.Ship("Destroyer", 3)
ship2 = ship.Ship("Tanker", 4)
ship_list.append(ship1)
ship_list.append(ship2)
start_game("juuso", "ville", ship_list, 5)


#board = create_board(5)
#set_ship(board, ship)
#print_board(board)
#print(shoot(board))
#print_board(board)




