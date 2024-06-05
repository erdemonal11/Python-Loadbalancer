import json, socket, threading, time


class Server():
    def listen(self) -> None:
        self.sock.listen()
        while True:
            client, address = self.sock.accept()
            print(f"[SERVER] Client connected with address: {address[0]}:{address[1]}\n")
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        try:
            req = client.recv(1024)
            req = req.decode("utf-8")

            if req and req == "test_response_time":
                client.send(str.encode("alive", "utf-8"))
                client.close()
                return

            elif req and req == "req_dir":
                client.send(str.encode(json.dumps(self.directory)))
                client.close()

            elif req and req.split("%")[0] == "req_file":
                self.send_file(sock=client, file_name=req.split("%")[1])
                client.close()

            elif req and req.split("%")[0] == "req_comp":
                self.compute(secs=int(req.split("%")[1]))
                client.close()
            client.close()
        except:
            client.close()

    def __init__(self, ip: str, port: int, lb_ip: str, lb_port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.sock.bind((ip, port))
        self.port = self.get_location()[1]
        self.directory = {"doc.txt": "text_file"}
        self.lb_ip = lb_ip
        self.lb_port = lb_port
        self.lb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_location(self) -> tuple:
        return (self.sock.getsockname()[0], self.sock.getsockname()[1])

    def send_file(self, sock: socket, file_name: str) -> None:

        try:
            file = open(file_name, "rb")
            data = file.read(1024)
            while data:
                print("[SERVER] Sending the file: " + file_name)
                sock.send(data)
                data = file.read(1024)
            file.close()
            time.sleep(1)
            sock.send(b"DONE")
            print("[SERVER] File sent.")
            sock.shutdown(2)
            sock.close()
        except:
            sock.send(b"NONE")
            sock.shutdown(2)
            sock.close()

    def compute(self, secs: int) -> None:
        print(f"[SERVER] Server is busy performing computation for {secs} seconds...\n")
        self.leave_load_balancer()
        time.sleep(secs)
        self.join_load_balancer()
        print("[SERVER] Computation completed.\n")

    def leave_load_balancer(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.lb_ip, self.lb_port))
        sock.send(str.encode(f"DEAD%{self.ip}:{self.port}"))
        sock.close()

    def join_load_balancer(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.lb_ip, self.lb_port))
        sock.send(str.encode(f"JOIN%{self.ip}:{self.port}"))
        sock.close()

    def __str__(self) -> str:
        return (f'IP:{self.ip} | PORT:{self.port}')
