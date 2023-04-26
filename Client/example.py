import socket

print("<<CLIENT FIELD>>")
while True:
    send_data = input("\nEnter: ")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (client_socket.connect(("127.0.0.1", 1111)) != 0):
        print("\nConnected")


    
    
    client_socket.sendall(bytes(send_data,"utf-8"))
    data = client_socket.recv(1024).decode("utf-8")
    print(f"Client send: {send_data}")
    
    print(f"Client recieved: {data}")

client_socket.close
