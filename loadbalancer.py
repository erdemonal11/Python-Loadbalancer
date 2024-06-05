import json, socket, time
from server import Server


class LoadBalancer():
    def __init__(self, ip: str, port: int = 0, algorithm: str = "round_robin") -> None:
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs_ip = ip
        self.cs_port = port
        self.client_sock.bind((ip, port))
        self.cs_port = self.get_location()[1]
        self.algorithm = algorithm
        self.servers = []
        self.server_weights = {}
        self.num_servers = 0
        self.sv_index = 0
        self.weight_counter = 0
        self.server_response_times = {}
        self.server_connections = {}

    def add_server(self, server: Server = None, weight: int = None, location: tuple = None) -> None:
        if server:
            self.num_servers += 1
            self.servers.append(server)
            self.server_connections[server] = 0
        elif location:
            self.num_servers += 1
            server = Server(ip=location[0], port=location[1], lb_ip=self.cs_ip, lb_port=self.cs_port)
            self.servers.append(server)
            self.server_connections[server] = 0
        if weight and (server or location):
            self.server_weights[server] = weight
        elif not weight and (server or location):
            self.server_weights[server] = -1

    def remove_server(self, location: tuple) -> bool:
        if self.server_exists(location):
            self.server_weights.pop(list(filter(lambda sv: ((sv.ip, sv.port) == location), self.servers))[0])
            self.server_response_times.pop(list(filter(lambda sv: ((sv.ip, sv.port) == location), self.servers))[0])
            self.servers = list(filter(lambda sv: ((sv.ip, sv.port) != location), self.servers))
            self.num_servers -= 1
            return True
        return False

    def printServers(self):
        for sv in self.servers:
            print(sv.ip)

    def server_exists(self, location: tuple) -> bool:
        return len([sv for sv in self.servers if (sv.ip, sv.port) == location]) != 0

    def listen(self) -> None:
        self.client_sock.listen()

        while True:
            client, address = self.client_sock.accept()

            req = client.recv(1024)
            req = req.decode('utf-8')
            if req:
                if req == "req_sv_loc":
                    print(f"[LOBA] Client connected with address: {address[0]}:{address[1]}\n")
                    sv_location = self.determine_server()
                    if sv_location:
                        res = str.encode(json.dumps(sv_location))
                        client.send(res)
                        print(
                            f"[LOBA] A server's location ({sv_location[0]}:{sv_location[1]}) has been sent to the client.\n")
                if req.split("%")[0] == "DEAD":
                    sv_location = (req.split("%")[1].split(":")[0], req.split("%")[1].split(":")[1])
                    self.remove_server(sv_location)
                    print(f"[LOBA] Server left the network with address: {address[0]}:{address[1]}\n")
                if req.split("%")[0] == "JOIN":
                    sv_location = (req.split("%")[1].split(":")[0], int(req.split("%")[1].split(":")[1]))
                    if not self.server_exists(sv_location):
                        self.add_server(location=sv_location)
                        self.server_connections[
                            Server(ip=sv_location[0], port=sv_location[1])] = 0  # Initialize connections to 0
                        print(f"[LOBA] Server joined the network with address: {address[0]}:{address[1]}\n")

                print(f"Handling request from client {address[0]}:{address[1]}")

    def determine_server(self) -> tuple:
        selected_server = None

        print("determining server...")

        if self.num_servers == 1:
            selected_server = (self.servers[0].ip, self.servers[0].port)

        if self.num_servers > 0:
            if self.algorithm == "round_robin":
                self.sv_index += 1
                if self.sv_index > self.num_servers:
                    self.sv_index = 0
                selected_server = (self.servers[self.sv_index - 1].ip, self.servers[self.sv_index - 1].port)

            if self.algorithm == "weighted_round_robin":
                num_weighted_servers = len(self.server_weights.values())
                if self.weight_counter >= self.server_weights[self.servers[self.sv_index]]:
                    self.sv_index += 1
                    self.weight_counter = 0
                    if self.sv_index >= self.num_servers:
                        self.sv_index = 0
                self.weight_counter += 1

                selected_server = list(self.server_weights.keys())[self.sv_index].get_location()

            if self.algorithm == "weighted_response_time":
                self.update_response_time_dict()
                selected_server = list(
                    filter(lambda sv: self.server_response_times[sv] == min(self.server_response_times.values()),
                           self.servers))[0].get_location()

            if self.algorithm == "weighted_least_connection":
                selected_server = self.allocate_by_least_connection()

        server = list(filter(lambda server: server.get_location() == selected_server, self.servers))[0]
        self.server_connections[server] += 1

        print(
            f"Selected server address {selected_server}, Connections: {self.server_connections[server]}")
        return selected_server

    def allocate_by_least_connection(self) -> tuple:
        min_connections = float('inf')
        selected_server = None

        for server in self.servers:
            connections = self.server_connections[server]
            weighted_connections = connections / self.server_weights[server]

            if weighted_connections < min_connections:
                min_connections = weighted_connections
                selected_server = server

        return selected_server.get_location()

    def get_response_time(self, server: Server) -> float:
        time_1 = time.time()
        sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sv_sock.connect(server.get_location())
        sv_sock.send(bytes("test_response_time", "utf-8"))
        sv_sock.settimeout(2)
        while True:
            try:
                print("loop")
                res = sv_sock.recv(1024)
                print("loop end")
                if res and res.decode("utf-8") and res.decode("utf-8") == "alive":
                    return int(time.time() - time_1)
            except:
                self.servers.remove(server)
                self.server_weights.pop(server)
                self.num_servers -= 1
                return -1

    def update_response_time_dict(self) -> None:
        for sv in self.servers:
            response_time = self.get_response_time(sv)
            if response_time >= 0:
                self.server_response_times[sv] = self.get_response_time(sv)
            else:
                self.server_response_times.pop(sv)

    def get_location(self) -> tuple:
        return (self.client_sock.getsockname()[0], self.client_sock.getsockname()[1])
