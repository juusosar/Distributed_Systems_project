CREATE TABLE users (
    username varchar(25) PRIMARY KEY,
    hashed_password varchar(256) NOT NULL,
    salt varchar(100) NOT NULL,
    registration_date date
);

CREATE TABLE user_game_stats (
    username varchar(25),
    games_played int,
    won int,
    lost int,
    win_percentage float,
    FOREIGN KEY (username) REFERENCES users(username)
);
