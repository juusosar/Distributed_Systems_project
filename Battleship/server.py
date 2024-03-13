from flask import *
import sqlite3
from database import Database
from datetime import date
import bcrypt
import threading
import queue
import time

app = Flask(__name__, static_url_path='/static')
session = {'ships': [],
           'ship_indexes': []}

db = Database('database.db')

# Matchmaking queue and lock
matchmaking_queue = queue.Queue()
matchmaking_lock = threading.Lock()

# List of players waiting for a match
# This allows direct interaction with waiting players, such as notifying them of their 
# current status or allowing them to cancel their matchmaking requests in find_match/flask_handle.
waiting_players = []


# Player class to hold player data
class Player:
    def __init__(self, player_id, player_board):
        self.player_id = player_id
        self.player_board = player_board


# Define a class to represent a game instance
# This class could be moved to another file with the game logic (battleships.py)
class GameInstance:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def start_game(self):
        print(f"Starting game between {self.player1.player_id} and {self.player2.player_id}")
        # Game logic goes here

        print(f"Game between {self.player1.player_id} and {self.player2.player_id} finished")

        winner = self.player1.player_id
        loser = self.player2.player_id
        return [winner, loser]


# Matchmaking function
def find_match(player):
    # If there are no waiting players, add the current player to the waiting list
    if not waiting_players:
        waiting_players.append(player)
        return False  # No match found yet

    # Remove the opponent from the waiting list
    try:
        opponent = waiting_players.pop(0)
        return opponent

    except IndexError as error:
        return False  # No match found yet


# Thread function for processing matchmaking requests matched_player
def matchmaking_thread():
    while True:
        player = matchmaking_queue.get()
        with matchmaking_lock:
            opponent = find_match(player)
            if opponent:
                print(f"Match found: {player.player_id} vs {opponent.player_id}")
                # Start a new thread for the game instance
                game_thread = threading.Thread(target=start_game_instance, args=(player, opponent))
                game_thread.start()
            else:
                print("Waiting for other players to join...")
        matchmaking_queue.task_done()


# Function to start a game instance between two players
def start_game_instance(player1, player2):
    game = GameInstance(player1, player2)
    result = game.start_game()
    # These should be carried to the database
    print(f"{result[0]} + won and  + {result[1]} + lost.")


# Function to hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password, salt


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        message = ''
        return render_template('login.html', message=message)
    if request.method == 'POST':
        if request.form['name'] != "" and request.form['password'] != "":
            username = request.form['name']
            password = request.form['password']

            # Check user and password from database
            try:
                db.connect()

                if db.verify_user(username, password):
                    message = 'Logged in successfully !'
                    session['loggedin'] = True
                else:
                    message = 'Invalid username or password.'
                    session['loggedin'] = False

                session['userid'] = username

            except sqlite3.Error as error:
                message = 'Something went wrong !'
                session['loggedin'] = False

            finally:
                db.close()

            if session["loggedin"]:
                response = make_response(render_template('user.html', user=session["userid"]))
                response.set_cookie('userid', session["userid"])
                response.headers["location"] = url_for('user')
                return response
            else:
                message = 'Incorrect username or password'
                return render_template('login.html', message=message)
        else:
            message = 'Please enter username / password !'
            return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session['loggedin'] = False
    session.pop('userid', None)
    res = make_response(render_template('login.html'), )
    res.set_cookie('userid', max_age=0)
    return res


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        if request.form['name'] != "" and request.form['password'] != "":
            username = request.form['name']
            password = request.form['password']

            # Checking if user already exists
            username_check = False
            try:
                db.connect()
                username_check = db.check_user(username)
            except sqlite3.Error as error:
                message = 'Something went wrong !'
            finally:
                db.close()

            if username_check:
                message = 'Account already exists !'

            # TODO: Password requirements check

            elif not username or not password:
                message = 'Please fill out the form !'

            else:
                # Current implementation of adding users
                today = date.today()
                hashed_password, salt = hash_password(password)
                try:
                    db.connect()
                    db.add_user(username, hashed_password, salt, today)
                    db.connection.commit()
                    message = 'You have successfully registered!'

                except sqlite3.Error as error:
                    message = 'Something went wrong !'

                finally:
                    db.close()

            return render_template('login.html', message=message)

        else:
            message = 'Please fill out the form !'
        return render_template('register.html', message=message)


@app.route("/user", methods=["GET", "POST"])
def user():
    userid = request.cookies.get("userid")
    if request.method == "GET":
        session['ships'], session['ship_indexes'] = {}, []
        if userid:
            return render_template("user.html", user=userid)
        else:
            return redirect(url_for('login'))

    if request.method == "POST":
        ship_lengths = [5, 4, 3, 2, 1]
        if request.form['startsetup'] == "start":
            return render_template("gamesetup.html", user=userid, ships=ship_lengths)



@app.route("/game", methods=["GET"])
def game():
    userid = request.cookies.get("userid")
    if request.method == "GET":
        #print("QUEUING")
        #matchmaking_queue.put(Player(userid, session['ships']))
        #print("JOINING")
        #matchmaking_queue.join()
        print(session['ship_indexes'])
        return render_template("game.html", user=userid, ships=session['ship_indexes'])


# Matchmaking route
@app.route('/matchmaking', methods=['POST'])
def matchmaking():
    player_data = request.json
    player_id = player_data.get('player_id')
    # Player board in list format
    player_board = player_data.get('player_board')
    player = Player(player_id, player_board)
    matchmaking_queue.put(player)
    matchmaking_queue.join()
    return jsonify({'message': 'Matchmaking request received'})


@app.route('/cell_click', methods=['POST'])
def handle_click():
    try:
        data = request.json
        player = request.cookies.get('userid')
        row = data['row']
        col = data['col']
        direction = data['orientation']
        length = data['length']
        # state = data['state']

        session['ships'].append({
            'row': row,
            'col': col,
            'direction': direction,
            'length': length
        })

        for ship in data['ship_indexes']:
            if ship not in session['ship_indexes']:
                session['ship_indexes'].append(ship)

        print(col, row, player)
        # Perform server-side logic here

        return jsonify({'message': 'Cell clicked successfully',
                        'col': col,
                        'row': row})

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error'})


if __name__ == '__main__':
    app.run(debug=True)
    # Start matchmaking thread
    matchmaking_thread = threading.Thread(target=matchmaking_thread)
    matchmaking_thread.daemon = True
    matchmaking_thread.start()
