import socket

HOST = 'localhost'
PORT = 1111       

while (True) :
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            message = '"DBname": "users", "Method": "INSERT", "param": {"email": "test@test.com", "pass": "123", "pass2": "123"}'
            print(message)
            #s.sendall(message.encode('utf-8'))
            s.sendall(bytes(message,"utf-8"))

            data = s.recv(1024)
            print('Received:', data.decode('utf-8'))
    except ConnectionRefusedError:
        print("Error")