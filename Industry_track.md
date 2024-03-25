# Industry track

## Battleship the Game

## About the project
By Ville Ailunka, Juuso Herajärvi and Juuso Särkelä

The application is a 1vs1 Battleships game playable in the browser.

## Implemented components:
The game implements Client-Server architecture:
- The system consists of a server which holds, authentication, taking commands from clients, creating matches between clients.
- For playing a game you need at least two clients connected to server, in client you will give input and it will send to client handle requests.
    -When creating game server creates a new thread for each game.


## Built with:
Detailed description of the system functionality and how to run the implementation

We use Docker for setting up the container for our server.
SQLite3 for the database.
Used programming languages: Python, Html, SQL, CSS, JavaScript

## Getting Started:
Clone the repository and go to the Distributed_Systems_project folder.

Start the application with (it downloads all the requirements) (and use sudo if needed):
```console
$ docker buildx build .
```

```console
$ docker image ls
```

```console
$ docker run <image-id>
```

Then go to http://172.17.0.2:5000 to access the game interface.


## REPORT:


In the world of gaming, there is no bound for innovation. From the humble beginnings of pixelated adventures to the immersive virtual realities of today, the landscape constantly evolves. One such evolution is the advent of distributed systems, reshaping how we interact with and experience multiplayer games. Among these, the timeless classic Battleship emerges as a prime candidate for a distributed makeover, weaving together nostalgia and cutting-edge technology into a seamless naval warfare experience.

1  Our solution

This chapter will tell you about our solution how we created a online battleship game to play againsts random people from all around world. We used simple client – server achitecture to create a classic battleship game experience for user to play. Participating nodes exchange information through Flask API and Ajax

![Ajax](./.img/ajax.jpg)

1.1	Server

Upon connecting to the server, players are prompted to either log in with existing credentials or register for a new account. The server utilizes SQLite3 for database management, verifying the user's existence or validating their credentials against stored data.

Furthermore, the server undertakes the responsibilities of managing gameplay elements such as ship placement, shooting, and game logic. When a player is prepared to engage in a match, a matchmaking thread enqueues them into a matchmaking queue. Once the queue accumulates two players, it dequeues the first two players and initiates a game thread for them to commence their match.

1.2	Client

In the client-side application, users either provide their credentials to log in or register with their desired credentials. Upon submission, the client sends a request to the server for authorization. Based on the response from the server, the appropriate HTML file is returned to the client, reflecting the authorization status.

Once authenticated, users proceed to create their game board. They start by selecting the orientation of their first ship on the board (horizontal or vertical). Then, they choose coordinates to place the ship. JavaScript code validates whether the selected coordinates are valid for ship placement. This process repeats until all ships are placed on the board.

After completing the board setup, the client sends a request to the server indicating readiness to start the game.

Once the game commences, users click on coordinates to target their opponent's ships. Each click triggers a request to the server with the chosen coordinates for processing. The server handles the attack, updating the game state accordingly, and sends the result back to the clients. This interactive gameplay continues until one player emerges victorious by sinking all opponent ships.


![Ajax](./.img/Architecture.jpg)


2 Scalability

If there is a lot of users who are trying to login or register, we are aware of SQLite3's nonconcurrency so if we were to make the program more scalable, we would just switch to using MySQL, which supports concurrency operations. We chose SQLite3 for it's lightweight quality. For each game server will create a thread so this is not a problem if there are not too many threads so basically it depends on hardware.



3 Princibles

Architecture:
The system is designed to operate in a client-server architecture where Flask serves as the server, handling HTTP requests from clients.
Threading is utilized to handle concurrent tasks, such as matchmaking and gameplay, enhancing scalability.

Processes:
The server-side processes include matchmaking, gameplay, and handling HTTP requests for user interaction.

Communication:
Communication between the client and server occurs over HTTP using Flask routes for various actions such as logging in, registering, setting up the game, and making moves.

Naming:
Meaningful variable and function names are used throughout the code, enhancing readability and maintainability.

Synchronization:
Threading mechanisms, are employed to ensure thread safety, particularly in scenarios where shared resources (e.g. matchmaking queue) are accessed concurrently.

Consistency and Replication:
The code focuses on maintaining consistency in game state and user data. For example, after a successful login, user session data is managed to maintain consistency across requests. Replication techniques are not explicitly implemented in code snippet, as it primarily focuses on the core functionality of the Battleship game.

Fault Tolerance:
The code demonstrates fault tolerance by using error handling mechanisms, such as try-except blocks, to handle exceptions and errors that may occur during database operations or other critical tasks.
