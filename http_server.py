import socket

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
        body = '[' + ' '.join(map(str, sequence)) + ']'
        status = 'HTTP/1.0 200 OK' 

    else:
        body = 'Invalid Request'
        status = 'HTTP/1.0 400 Bad Request'

    return f"{status}\r\nConnection: close\r\n\r\n{body}"


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
    print(handle_request('GET /24 HTTP/1.0\r\nHost: localhost\r\n\r\n'))

if __name__ == '__main__':
    main()