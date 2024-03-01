CREATE TABLE users (
    id int PRIMARY KEY,
    username varchar(25) NOT NULL,
    hashed_password varchar(256) NOT NULL,
    salt varchar(100) NOT NULL,
    registration_date date
);

CREATE TABLE user_game_stats (
    user_id int,
    games_played int,
    won int,
    lost int,
    win_percentage AS (won/games_played),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
