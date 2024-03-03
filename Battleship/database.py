""" database.py """
import sqlite3
import typing
import os
import bcrypt


class Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            try:
                with open("./Battleship/schema.sql") as f:
                    self.connection.executescript(f.read())
            except sqlite3.Error as error:
                print("Error:", error)
            self.cursor = self.connection.cursor()
            print("Connected to database successfully!")
        except sqlite3.Error as error:
            print("Error:", error)

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        else:
            print("No database connection to close.")

    # Function to hash a password
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password, salt

    # Checks if an username is already taken, returns True/False
    def check_user(self, username):
        exists = False

        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))

        username_check = self.cursor.fetchone()
        if username_check[0] != 0:

            print('Username already taken')
            exists = True

        return exists
        

    # Function to add a new user
    def add_user(self, username, password, salt, registration_date):

        self.cursor.execute("""
            INSERT INTO users (username, hashed_password, salt, registration_date)
            VALUES (?, ?, ?, ?)
            """, (username, password, salt, registration_date))
        
        self.cursor.execute("""
            INSERT INTO user_game_stats (username, games_played, won, lost, win_percentage)
            VALUES (?, ?, ?, ?, ?)
            """, (username, 0, 0, 0, 0))


    # Function to delete a user
    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))

    # Function to update game statistics for a user
    def update_game_stats(self, username, result):

        # Checking if player won or lost to update accordingly
        if result == "w":
            self.cursor.execute("""
            UPDATE user_game_stats 
            SET games_played = games_played + 1, won = won + 1
            WHERE username = (?)
            """, (username,))
        else:
            self.cursor.execute("""
            UPDATE user_game_stats 
            SET games_played = games_played + 1, lost = lost + 1
            WHERE username = (?)
            """, (username,))
        
        # Updates the win percentage of the player
        self.cursor.execute("""
            UPDATE user_game_stats 
            SET win_percentage = won * 100 / games_played
            WHERE username = (?)
            """, (username,))

    # Function to verify user credentials during login
    def verify_user(self, username, password):
        verified = False
        # Retrieve hashed password and salt from the database for the given username
        self.cursor.execute("SELECT hashed_password, salt FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()

        if row:
            hashed_password = row[0]
            salt = row[1]

            # Hash the entered password with the retrieved salt
            entered_password_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

            # Compare the hashed passwords
            if hashed_password == entered_password_hashed:
                verified = True
        return verified


# Example usage
def main():
    db = Database('database.db')
    try:
        # Connect to the SQLite database
        db.connect()

        # Add a new user
        db.add_user("example_user", "password123", "2024-02-15")

        db.add_user("paavo", "sala", "2024-02-16")

        db.add_user("linnea", "sana", "2024-02-17")
        db.add_user("linnea", "sana", "2024-02-17")

        # A game was played
        db.update_game_stats("paavo", "w")
        db.update_game_stats("linnea", "l")

        # A game was played
        db.update_game_stats("paavo", "w")
        db.update_game_stats("linnea", "l")

        # A game was played
        db.update_game_stats("paavo", "l")
        db.update_game_stats("linnea", "w")

        # Commit the transaction
        db.connection.commit()
        print("Transaction committed successfully!")

        # Verify user credentials during login
        username = "example_user"
        password = "password123"
        if db.verify_user(username, password):
            print("Login successful!")
        else:
            print("Invalid username or password.")

    except sqlite3.Error as error:
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    main()
