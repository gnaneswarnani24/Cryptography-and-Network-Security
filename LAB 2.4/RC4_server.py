import socket
from arc4 import ARC4

# Configuration
HOST = '127.0.0.1'  # Server address (localhost)
PORT = 65432        # Port to listen on
SECRET_KEY = b'secretkey123'  # RC4 encryption key

def decrypt_file(data):
    cipher = ARC4(SECRET_KEY)
    decrypted_data = cipher.decrypt(data)
    with open("received_decrypted_file.txt", "wb") as f:
        f.write(decrypted_data)
    print("File decrypted and saved as 'received_decrypted_file.txt'.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            file_data = b""
            
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                print(f"Received {len(data)} bytes of data.")
                file_data += data
            
            if file_data:
                print("File received. Decrypting...")
                decrypt_file(file_data)
            else:
                print("No data received.")

if __name__ == "__main__":
    main()
