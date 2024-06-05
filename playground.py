import threading, time, random
from client import Client
from server import Server
from loadbalancer import LoadBalancer
import subprocess


def start_client(client: Client, lb: LoadBalancer, server_location: str) -> None:
    client.connect(lb.cs_ip, lb.cs_port, lb=True, server_location=server_location)


def start_load_balancer(lb: LoadBalancer) -> None:
    lb.listen()


def start_server(server: Server) -> None:
    server.listen()


def add_servers_to_load_balancer(servers: list, lb: LoadBalancer) -> None:
    print("Random weights between [1-9] assigning to the servers...")
    for server in servers:
        weight = random.randint(1, 9)
        lb.add_server(server=server, weight=weight)
        print(f"Created the server at location {server.get_location()} with weight {weight}")


if __name__ == "__main__":
    lb_recv_ip = "127.0.0.1"
    lb_algorithm = ""

    while True:
        bal_method = input("\nChoose the balancing method:\nPress 1 for Static or Press 2 for Dynamic\n")
        if bal_method == "1":
            while True:
                algorithm_choice = input(
                    "\nChoose the static balancing algorithm \nPress 1 for Round Robin or Press 2 for Weighted Round Robin\n")
                if algorithm_choice in ["1", "2"]:
                    lb_algorithm = "round_robin" if algorithm_choice == "1" else "weighted_round_robin"
                    break
                else:
                    print("Invalid input. Please enter '1' for Round Robin or '2' for Weighted Round Robin.\n")
            break
        elif bal_method == "2":
            while True:
                algorithm_choice = input(
                    "\nChoose the dynamic balancing algorithm\nPress 1 for Weighted Response Time or Press 2 for Weighted Least Connection\n")
                if algorithm_choice in ["1", "2"]:
                    lb_algorithm = "weighted_response_time" if algorithm_choice == "1" else "weighted_least_connection"
                    break
                else:
                    print(
                        "Invalid input. Please enter '1' for Weighted Response Time or '2' for Weighted Least Connection.\n")
            break
        else:
            print("Invalid input. Please enter '1' for Static or '2' for Dynamic.")

    lb = LoadBalancer(lb_recv_ip, port=9000, algorithm=lb_algorithm)

    while True:
        try:
            num_clients = int(input("\nHow many clients do you plan to create? (1-50)\n"))
            if 1 <= num_clients <= 50:
                break
            else:
                print("Invalid client count. Please enter a value between 1 and 50.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    servers = []

    while True:
        try:
            num_servers = int(input("\nHow many servers do you plan to create? (1-50)\n"))
            if 1 <= num_servers <= 50:
                break  # Valid input, exit the loop
            else:
                print("Invalid server count. Please enter a value between 1 and 50.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    for i in range(num_servers):
        server = Server(lb_recv_ip, port=0, lb_ip=lb_recv_ip, lb_port=lb.get_location()[1])
        servers.append(server)

    for server in servers:
        threading.Thread(target=start_server, args=[server]).start()

    time.sleep(1)

    add_servers_to_load_balancer(servers, lb)

    load_balancer_thread = threading.Thread(target=start_load_balancer, args=[lb])
    load_balancer_thread.start()

    time.sleep(1)

    for client in range(num_clients):
        sv_location = lb.get_location()
        subprocess.Popen(['cmd.exe', '/K', 'start', 'python', 'client.py', sv_location[0], str(sv_location[1])],
                         shell=True)
        print(f"[LOBA] A server's location ({sv_location[0]}:{sv_location[1]}) has been sent to the client.\n")

    load_balancer_thread.join()