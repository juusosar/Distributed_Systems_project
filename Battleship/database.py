""" database.py """
import sqlite3
import datetime
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

    def create_database(self):
        try:
            # Check if the database file already exists
            if os.path.exists(self.db_name):
                print("Database file already exists.")
            else:
                # Create the database file
                with open(self.db_name, 'w'):
                    pass
                with open("Battleship/schema.sql") as f:
                    self.connection.executescript(f.read())
                print("Database file created successfully!")
        except Exception as error:
            print("Error:", error)
    
    # Function to hash a password
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password, salt

    # Function to add a new user
    def add_user(cursor, username, password, registration_date):
        hashed_password, salt = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, hashed_password, salt, registration_date)
            VALUES (?, ?, ?, ?)
        """, (username, hashed_password, salt, registration_date))

    # Function to delete a user
    def delete_user(cursor, user_id):
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    # Function to update game statistics for a user
    def update_game_stats(cursor, user_id, games_played, won, lost):
        cursor.execute("""
            INSERT INTO user_game_stats (user_id, games_played, won, lost)
            VALUES (?, ?, ?, ?)
        """, (user_id, games_played, won, lost))

    # Function to verify user credentials during login
    def verify_user(cursor, username, password):
        # Retrieve hashed password and salt from the database for the given username
        cursor.execute("SELECT hashed_password, salt FROM users WHERE username=?", (username,))
        row = cursor.fetchone()

        if row:
            hashed_password = row[0]
            salt = row[1]

            # Hash the entered password with the retrieved salt
            entered_password_hashed = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))

            # Compare the hashed passwords
            if hashed_password == entered_password_hashed:
                return True
        return False


# Example usage
def main():
    try:
        db = Database('database.db')

        db.connect()
    
        # Connect to the SQLite database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Add a new user
        Database.add_user(cursor, "example_user", "password123", "2024-02-15")

        # Update game statistics for a user
        Database.update_game_stats(cursor, 1, 1, 1, 0)

        # Commit the transaction
        connection.commit()
        print("Transaction committed successfully!")

        # Verify user credentials during login
        username = "example_user"
        password = "password123"
        if Database.verify_user(cursor, username, password):
            print("Login successful!")
        else:
            print("Invalid username or password.")

    except sqlite3.Error as error:
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    main()
