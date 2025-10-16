import socket
from datetime import datetime #for timestamping and delay calculation

HOST = '127.0.0.1'
PORT = 8082

def parse_timestamp(ts_str):
    # Split milliseconds from the main timestamp
    base, ms = ts_str.rsplit(':', 1)
    dt = datetime.strptime(base, "%Y-%m-%d %H:%M:%S")
    return dt.replace(microsecond=int(ms) * 1000)

def parse_response(response):
    body = response.split('\r\n\r\n')[1]
    return body

def main():
    avg_delay = [0,0]
    list_of_requests = [3148, 3744, 1237, 112, 56, 12328, 99, 104, 9999]
    i = 0
    while True:
        # user_input = input("Enter a number from the list [3148, 3744, 1237, 112, 56, 12328, 99, 104, 9999] or 'exit' to quit: ")
        # print()

        # if user_input.lower() == 'exit':
        #     print("Exiting the client.\n")
        #     break
        if(i >= len(list_of_requests)):
            break

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
            client_socket.connect((HOST, PORT))

            request_message = f"GET /{list_of_requests[i]} HTTP/1.0\r\nHost: {HOST}\r\n\r\n"
            client_socket.sendall(request_message.encode('utf-8'))

            sent_time = datetime.now()
            sent_time = sent_time.strftime("%Y-%m-%d %H:%M:%S") + f":{int(sent_time.microsecond / 1000):03d}"

            print(f"Number: {list_of_requests[i]} sent at: {sent_time}\n")
            print(request_message)
            
            response = client_socket.recv(4096).decode('utf-8')

            received_time = datetime.now()
            received_time = received_time.strftime("%Y-%m-%d %H:%M:%S") + f":{int(received_time.microsecond / 1000):03d}"

            print(f"{parse_response(response)}\n\nResponse received at: {received_time}\n")

            delay =  parse_timestamp(received_time) - parse_timestamp(sent_time)
            print(f"Delay: {delay.total_seconds():.3f} seconds\n")
            
            avg_delay[1] += 1
            avg_delay[0] += delay.total_seconds()/avg_delay[1]

        i += 1   

    print(f"Average Delay: {avg_delay[0]:3f} seconds over {avg_delay[1]} requests")


if __name__ == "__main__":
    main()