import socket
import time

HOST = '127.0.0.1'
PORT = 8082

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        while True:
            user_input = input("Enter a number from the list [3148, 3744, 1237, 112, 56, 12328, 99, 104, 9999] or 'exit' to quit: ")
            print()
            if user_input.lower() == 'exit':
                break
            
            request_message = f"GET /{user_input} HTTP/1.0\r\nHost: {HOST}\r\n\r\n"
            client_socket.sendall(request_message.encode('utf-8'))
            
            response = client_socket.recv(4096).decode('utf-8')
            print(f"Response:\n{response}\n")
            

if __name__ == "__main__":
    main()