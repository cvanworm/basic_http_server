import socket
import time #for processing delay

HOST = '127.0.0.1'
PORT = 8082

def handle_request(request_message):
    requests = [3148, 3744, 1237, 112, 56, 12328,99,104,9999]
    requests =  list(map(str, requests))

    header = request_message.splitlines()[0]
    method, path, _ = header.split()

    if method != 'GET':
        return 'HTTP/1.0 400 Bad Request\r\nConnection: close\r\n\r\nInvalid Request'

    
    number = path.split('/')[1]


    if number in requests:
        sequence = compute_collatz_sequence(int(number))
        length = len(sequence)
        body = '[' + ' '.join(map(str, sequence)) + ']'
        status = 'HTTP/1.0 200 OK' 

    else:
        body = 'Invalid Request'
        status = 'HTTP/1.0 400 Bad Request'
        length = 0

    return f"{status}\r\nConnection: close\r\n\r\n{body}", length


def compute_collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Serving on http://{HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connection from {addr}\n")
                request = client_socket.recv(1024).decode('utf-8')
                print(f"Request:\n{request}")

                response, length = handle_request(request)
                # print(length)
                time.sleep(.1 * length)  # Simulate processing delay
                client_socket.sendall(response.encode('utf-8'))

                print(f"Response:\n{response}\n")

if __name__ == '__main__':
    main()