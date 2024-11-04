import requests
import threading
import time
import os

SERVER_URL = 'URL OF YOUR SERVER'  

DOWNLOAD_DIR = r'C:\ipCHATv4' 
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
last_received_message = None  

def send_message():
    while True:
        message = input()  
        
        if message.strip().lower() == '/upload':
            upload_file()  
            continue
        
        full_message = f"{final_username}: {message}"
        response = requests.post(f"{SERVER_URL}/send", json={"message": full_message})
        
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")

def check_for_new_message():
    global last_received_message

    while True:
        try:
            response = requests.get(f"{SERVER_URL}/latest")
            if response.status_code == 200:
                latest_message = response.json().get("latest_message", "No messages yet.")
                if latest_message != last_received_message:  
                    print(f"\n{latest_message}")
                    last_received_message = latest_message
            else:
                print("\nFailed to retrieve the latest message.")
        except requests.exceptions.RequestException as e:
            print(f"Error while checking for new messages: {e}")
        
        time.sleep(1)  

def check_for_new_file():
    downloaded_files = set(os.listdir(DOWNLOAD_DIR))

    while True:
        try:
            
            response = requests.get(f"{SERVER_URL}/files")
            if response.status_code == 200:
                files = response.json().get('files', [])

                for file in files:
                    if file not in downloaded_files:
                       
                        file_response = requests.get(f"{SERVER_URL}/download/{file}")
                        if file_response.status_code == 200:
                            with open(os.path.join(DOWNLOAD_DIR, file), "wb") as filee:
                                filee.write(file_response.content)
                            print(f"{file} successfully downloaded")
                            downloaded_files.add(file)  
                        else:
                            print(f"Failed to download {file}: Status Code {file_response.status_code}")
            else:
                print("Failed to fetch files: Status Code", response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Error while checking for new files: {e}")

        time.sleep(2)  


def upload_file():
    path_of_file = input("Enter the path of the file to be uploaded: ")
    path_of_filee = path_of_file.replace('"', '')
    filepath = path_of_filee.replace("\\", "\\\\")

    try:
        with open(filepath, 'rb') as filee:
            response = requests.post(f"{SERVER_URL}/upload", files={'file': filee})
        print("Status Code:", response.status_code)
        print("JSON Response:", response.json())

    except FileNotFoundError:
        print("Error: The file was not found. Please check the path and try again.")
    except Exception as e:
        print("An error occurred while uploading the file:", str(e))

def download_file(filename):
    response = requests.get(f"{SERVER_URL}/files")
    if response.status_code == 200:
        files = response.json().get('files', [])
        print("Available files:", files)
        for dfile in files:
            file_response = requests.get(f"{SERVER_URL}/download/{dfile}")
            if file_response.status_code == 200:
                with open(dfile, "wb") as file:
                    file.write(file_response.content)
                print(f"{dfile} successfully downloaded")
            else:
                print(f"Failed to download {dfile}: {file_response.status_code}")
    else:
        print("Failed to retrieve file list.")




def main():
    global final_username
    print("Please log in through the website to start chatting.")

    while True:
        input("Press Enter after logging in through the website...")  
        
        
        final_username = input("Enter your username : ")

        
        response = requests.get(f"{SERVER_URL}/check_login", params={"username": final_username})
        if response.status_code == 200:
            print("Login verified. You can start chatting.")
            threading.Thread(target=check_for_new_message, daemon=True).start()
            send_message()
            break
        
        elif response.status_code == 401:
            print("Invalid username or session expired. Please log in again.")

        else:
            print("unexpected error occurred")

if __name__ == '__main__':
    main()
