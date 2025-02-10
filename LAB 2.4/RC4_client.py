import socket
from arc4 import ARC4

# Configuration
HOST = '127.0.0.1'  # Server address (localhost)
PORT = 65432        # Server port
SECRET_KEY = b'secretkey123'  # RC4 encryption key

def encrypt_file(file_path):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
        cipher = ARC4(SECRET_KEY)
        encrypted_data = cipher.encrypt(file_data)
        return encrypted_data
    except Exception as e:
        print(f"Error during file encryption: {e}")
        return None

def main():
    file_path = "plaintext.txt.txt"  # File to be sent to the server

    try:
        # Encrypt the file
        encrypted_data = encrypt_file(file_path)
        if encrypted_data is None:
            print("Encryption failed. Exiting...")
            return
        
        print(f"File '{file_path}' encrypted. Sending {len(encrypted_data)} bytes of data...")

        # Create socket and connect to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Attempting to connect to {HOST}:{PORT}...")
            client_socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            # Send encrypted data
            client_socket.sendall(encrypted_data)
            print(f"File '{file_path}' sent successfully.")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the file path.")
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
    except TimeoutError:
        print("Connection timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
