import requests
import threading
import time

SERVER_URL = 'URL_OF_YOUR_SERVER'  



last_received_message = None  

def send_message():
    while True:
        message = input()  
        full_message = f"{final_username}: {message}"
        response = requests.post(f"{SERVER_URL}/send", json={"message": full_message})
        
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")

def check_for_new_message():
    global last_received_message
    while True:
        response = requests.get(f"{SERVER_URL}/latest")
        if response.status_code == 200:
            latest_message = response.json().get("latest_message", "No messages yet.")
            if latest_message != last_received_message:  
                print(f"\n{latest_message}")
                last_received_message = latest_message
        else:
            print("\nFailed to retrieve the latest message.")
        
        time.sleep(1)  

def verify(user_input, path="user_db.txt"):
    global final_username
    username, password = user_input.split()
    with open(path, "r") as f:
        for line in f:
            userr, pswdr = line.strip().split(":")
            if userr == username and pswdr == password:
                print("Login successful")
                final_username = username
                return True
            
    print("Login failed")
    return False

if __name__ == '__main__':
    
    ask1 = input("REGISTER OR LOGIN\n")
    if ask1.lower() == "register":
        user_input = input("Enter username and password using space between them: ")
        userr, pswdr = user_input.split()
        with open("user_db.txt", "a") as f:
            f.write(f"{userr}:{pswdr}\n")

    elif ask1.lower() == "login":
        user_input = input("Enter username and password using space between them: ")
        userr, pswdr = user_input.split()
        if verify(user_input):
            
            threading.Thread(target=check_for_new_message, daemon=True).start()

            
            send_message()
        else:
            print("You need to register first before logging in.")
    else:
        print("Invalid input")
