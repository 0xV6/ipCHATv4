# ipCHATv4

ipCHATv4 is a simple chat application that allows users to send and receive messages over a network. The application features a command-line interface and utilizes a Flask server to handle message exchange between clients. User credentials are stored in a text file for authentication.

## Features

- **User Registration and Login**: Users can register and log in using their credentials.
- **Message Sending**: Users can send messages to each other.
- **Real-time Messaging**: Users receive the latest message only if they did not send it.
- **Cross-Platform**: The application runs on Windows, Linux, and MacOS and Android(using Termux).

## Installation

### Requirements

- Python 3.x
- `pip` (Python package installer)

### Steps to Install

1. Clone this repository:

   ```bash
   git clone https://github.com/ipRMNv4/ipCHATv4.git
   cd ipCHATv4
   ```

2. Install the required packages:

   ```bash
   pip install Flask requests
   ```

3. (Optional) Install PyInstaller for creating an executable:

   ```bash
   pip install pyinstaller
   ```

## Usage

### Running the Application
1. **Configuring the server (for dynamic IP)**:
   - use ngrok and execute the following command (provide the port you want you use for the server:
   ```
   ngrok http PORT
   ```
   - copy the linkk given to you and paste it in the **client.py**
    
2. **Run the Server**:
   - Navigate to the directory where your server script is located.
   - Run the server script:

   ```
   python server.py
   ```

3. **Run the Client**:
   - In a separate terminal or command prompt, navigate to the client directory.
   - Run the client script:

   ```bash
   python client.py
   ```

### Creating an Executable

To create a standalone executable, navigate to the project directory and run:

```
pyinstaller --onefile --console --add-data "user_db.txt;." client.py
```

After running this command, you will find the executable in the `dist` folder.

### Running the Executable

1. Navigate to the `dist` directory:

   ```
   cd dist
   ```

2. Run the executable:

   ```
   client.exe
   ```

## Configuration

- User credentials are stored in `user_db.txt`. Each entry should be in the format `username:password`.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[ipRMNv4](https://github.com/ipRMNv4)
