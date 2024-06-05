# Python Load Balancer

This project implements a simple Python-based load balancer system with various algorithms for load distribution. Below is a guide to understanding and running the project effectively.

## Project Structure

The project consists of the following components:

- Load Balancer
- Client
- Server
- Playground

## Load Balancer

The load balancer is responsible for distributing incoming requests among available servers. It employs various algorithms for load distribution, including:

### Static Algorithms

- Round-Robin
- Weighted-Round-Robin

### Dynamic Algorithms

- Weighted-Response-Time
- Weighted-Least-Connection

## Client

The client module facilitates communication with the load balancer and servers. Key functionalities include:

- Connecting to the load balancer to request server locations.
- Handling different types of requests to servers.
- Automatically switching to another server if a request fails or the server is unresponsive.

## Server

The server module listens for incoming requests from clients and processes them accordingly. Important features include:

- Communicating with the load balancer to test response times.
- Utilizing JSON serialization for transmitting data such as tuples, lists, and dictionaries.
- Employing TCP for all connection protocols to ensure reliable file transactions.

## Playground

The playground serves as an environment for testing the load balancer system. It allows users to instantiate multiple servers and clients, providing input to simulate real-world scenarios. Each instance runs on a separate thread to maintain responsiveness and prevent freezing.

## How to Run the Project

To test the project, follow these steps:

1. Run the `playground.py` file.
2. Input the desired number of servers.
3. Instantiate one or more clients and provide input as required.
4. Observe the communication between clients, the load balancer, and servers.

## Repository Structure

The repository includes the following files:

- `load_balancer.py`: Implementation of the load balancer.
- `client.py`: Implementation of the client.
- `server.py`: Implementation of the server.
- `playground.py`: Main script to initiate testing.
- `README.md`: Instructions and overview of the project.

## Dependencies

Ensure you have Python installed on your system. No additional dependencies are required for running this project.

Feel free to contribute to the project by forking the repository and submitting pull requests with your improvements or suggestions.

![image](https://github.com/erdemonal11/Python-Loadbalancer/assets/137915983/a9c60e0a-e4f4-46c2-bf74-e50e700e4d9d)
