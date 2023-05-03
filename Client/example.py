import socket
import time
print("<<CLIENT FIELD>>")
while True:
    send_data = '{"DBname": "users", "Method": "INSERT", "param": {"email": "test@test.com", "pass": "123", "pass2": "123"}}'
            
        
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (client_socket.connect(("127.0.0.1", 1111)) != 0):
        print("\nConnected")

    time.sleep(4)
    
    print("send")
    client_socket.sendall(bytes(send_data,"utf-8"))
    #data = client_socket.recv(1024).decode("utf-8")
    print(f"Client send: {send_data}")
    
    #print(f"Client recieved: {data}")

    client_socket.close()
