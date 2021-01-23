#!/usr/bin/env python3
import socket, sys, time, os

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def send_google(payload):
    try:
        #define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        buffer_size = 4096

        #make the socket, get the ip, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip , port))
        
        #send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
        return full_data

    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()

def main():
    HOST = ""
    PORT = 8001
    BUFFER_SIZE = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(10)
        
        #continuously listen for connections
        i = 1
        while i <= 10:
            conn, addr = s.accept()
            child_pid = os.fork()

            if child_pid == 0:
                while True:
                    conn, addr = s.accept()
                    print(addr)
                    
                    #recieve data, wait a bit, then send it back
                    full_data = conn.recv(BUFFER_SIZE)

                    returned_data = send_google(full_data)
                    print(returned_data)
                    time.sleep(0.5)
                    conn.sendall(returned_data)
                    conn.close()
                    break
            else:
                i += 1


if __name__ == "__main__":
    main()

