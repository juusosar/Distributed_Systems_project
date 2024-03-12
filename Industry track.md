# Industry track

## Battleship the Game

## About the project
By Ville Ailunka, Juuso Herajärvi and Juuso Särkelä

The application is a 1vs1 Battleships game playable in the browser.

## Implemented components:
The game implements Client-Server architecture:
- The system consists of a server and at least two clients.

Participating nodes exchange information through Flask API and Ajax.
![Ajax](../.img/ajax.jpg)


Each node must be an independent entity and (partially) autonomous


Detailed descriptions of relevant principles covered in the course (architecture, processes, communication, naming, synchronization, consistency and replication, fault tolerance); irrelevant principles can be left out.

## Built with:
Detailed description of the system functionality and how to run the implementation

We use Docker for setting up the container for our server.
SQLite3 for the database.
Used programming languages: Python, Html, SQL, CSS, JavaScript

- If you are familiar with a particular container technology, feel free to use it (Docker is not mandatory)
- Any communication protocol / Internet protocol suite can be used: HTTP(S), MQTT, AMQP, CoAP, ..

## Getting Started:
Our application requires Docker to run.
Clone the repository and go to the Distributed_Systems_project folder.

Start the application with (it downloads all the requirements):
```console
$ docker compose up
```

Then go to http://127.0.0.1:5000 to access the game interface.


## Results of the tests:
Detailed description of the system evaluation
Evaluate your implementation using selected criteria, for example:
- Number of messages / lost messages, latencies, ...
- Request processing with different payloads, ..
- System throughput, ..

- We are aware of SQLite3's nonconcurrency so if we were to make the program more scalable, we would just switch to using MySQL, which supports concurrency operations. We chose SQLite3 for it's lightweight quality.


Design two evaluation scenarios that you compare with each other, for example:
- Small number / large number of messages
- Small payload / big payload

Collect numerical data of test cases:
- Collecting logs of container operations
- Conduct simple analysis for documentation purposes (e.g. plots or graphs)

## Acknowledgments:
list resources you find helpful

