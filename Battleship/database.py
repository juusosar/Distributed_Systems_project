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
            try:
                with open("schema.sql") as f:
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

    def create_database(self):
        try:
            # Check if the database file already exists
            #if os.path.exists(self.db_name):
            #    print("Database file already exists.")
            #else:
            # Create the database file
                with open("schema.sql") as f:
                    self.connection.executescript(f.read())
                print("Database file created successfully!")
        except Exception as error:
            print("Error:", error)

    # Function to hash a password
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password, salt

    # Function to add a new user
    def add_user(self, username, password, registration_date):
        hashed_password, salt = self.hash_password(password)
        self.cursor.execute("""
            INSERT INTO users (username, hashed_password, salt, registration_date)
            VALUES (?, ?, ?, ?)
        """, (username, hashed_password, salt, registration_date))

    # Function to delete a user
    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    # Function to update game statistics for a user
    def update_game_stats(self, user_id, games_played, won, lost):
        self.cursor.execute("""
            INSERT INTO user_game_stats (user_id, games_played, won, lost)
            VALUES (?, ?, ?, ?)
        """, (user_id, games_played, won, lost))

    # Function to verify user credentials during login
    def verify_user(self, username, password):
        # Retrieve hashed password and salt from the database for the given username
        self.cursor.execute("SELECT hashed_password, salt FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()

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
    db = Database('database.db')
    try:
        # Connect to the SQLite database
        db.connect()

        # Add a new user
        db.add_user("example_user", "password123", "2024-02-15")

        # Update game statistics for a user
        db.update_game_stats(1, 1, 1, 0)

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
