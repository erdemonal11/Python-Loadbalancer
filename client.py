import json, socket, time, sys
import os


class Client():
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip: str, port: int, lb: bool = False) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        if not lb:
            while True:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((ip, port))
                self.sock.settimeout(5)
                time.sleep(1.25)
                try:
                    choice: int = self.get_request_input()
                    if choice == 1:
                        response_dir = self.request_directory()
                        if response_dir:
                            print("Server's directory: ", response_dir)
                        else:
                            print("No directory was returned or directory was empty.")
                    elif choice == 2:
                        file_name = input(
                            "\nEnter name of the file you want from the server with its extension e.g:'file.txt'\n")
                        if self.request_file(file_name):
                            print("File was successfully downloaded from the server.")
                        else:
                            print("No file was returned from the server or it does not exist.")
                    elif choice == 3:
                        secs = ""
                        while True:
                            secs = input("\nHow many seconds do you want the computation to take:\n")
                            if secs.isnumeric():
                                secs = int(secs)
                                break
                            print("Enter a numeric value:")
                        self.request_computation(seconds=secs)
                        print("Computation request is sent.")
                        time.sleep(secs)

                except socket.timeout as e:
                    print("Server timeout. Returning to the load balancer....\n")
                    self.sock.close()
                    self.connect(ip=self.lb_ip, port=self.lb_port, lb=True)

                if input("\nDo you want to make another request? (Y/N)\n").lower() == "n":
                    print("Program terminated.")
                    self.sock.close()
                    self.sock.shutdown()
                    break
                self.sock.close()

        else:
            self.lb_ip = ip
            self.lb_port = port
            print("Asking the load balancer for the server ip...")
            self.sock.connect((ip, port))
            self.sock.send(bytes("req_sv_loc", "utf-8"))
            res = self.sock.recv(1024)
            new_loc = json.loads(res)
            if new_loc:
                self.sock.close()
                print(f"Connecting to the server with address: {new_loc[0]}:{new_loc[1]}")
                self.connect(new_loc[0], new_loc[1], lb=False)
            else:
                print("No server location was returned, none accessible.")
                self.sock.shutdown(2)
                self.sock.close()

    def request_directory(self) -> dict:
        self.sock.send(str.encode("req_dir", "utf-8"))
        res = self.sock.recv(1024)
        if res:
            res = json.loads(res)
            return res
        else:
            return None

    def request_computation(self, seconds) -> None:
        self.sock.send(str.encode(f"req_comp%{seconds}"))

    def get_request_input(self) -> int:
        choice: str = None
        while True:
            choice = input(("""Which request do you want to make?\n
              1) Request server's directory listing\n
              2) Request file\n
              3) Request a computation\n
             """
                            ))
            if not choice.isnumeric():
                print("Select a valid option.")
                continue
            break
        return int(choice)

    def request_file(self, file_name: str) -> bool:

        self.sock.send(str.encode(f"req_file%{file_name}"))

        file = open(file_name.split(".")[0] + "_new." + file_name.split(".")[1], "wb")
        while True:
            print("Receiving the file...\n")
            data = self.sock.recv(1024)
            if data == b"DONE":
                self.sock.shutdown(2)
                self.sock.close()
                file.close()
                return True
            if data == b"NONE":
                self.sock.shutdown(2)
                self.sock.close
                file.close()
                return False
            file.write(data)
            time.sleep(0.5)


if __name__ == "__main__":
    client = Client()
    if (len(sys.argv) < 2):
        ip = input("Enter ip:")
        port = int(input("Enter port"))
        client.connect(ip, port, True)
    else:
        address = sys.argv[1:]
    client.connect(address[0], int(address[1]), True)
    os.system("pause")


