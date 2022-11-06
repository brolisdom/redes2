import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
count = 0

def save_into(client, chunk, bytes):
    if not os.path.exists("client"+client): 
        os.makedirs("client"+client)
    filename = "client"+client+"/chunk"+chunk
    f = open(filename, "wb")
    f.write(bytes)
    f.close()

def merge_files(filename, client, i):
    if not os.path.exists("res"): 
        os.makedirs("res")
    f = open("res/copy-"+filename, "wb")
    for chunk in range(i):
        filename = "client"+client+"/chunk"+str(chunk)
        tmp = open(filename, "rb")
        bytes = tmp.read(200)
        f.write(bytes)
    f.close()

def multi_threaded_client(connection, client):
    res = 'Se le ha asignado el cliente: '+client
    connection.send(str.encode(res))
    # print(res)
    i = -1
    while True:
        data = connection.recv(2048)
        if i < 0: filename = data.decode('utf-8')
        else:
            if not data: break
            save_into(client, str(i), data)
            response = 'Chunk '+str(i)+' almacenado'
            connection.sendall(str.encode(response))
        i += 1
    print('Reconstruyendo archivo del cliente '+client)
    merge_files(filename, client, i)
    print('Proceso de cliente '+client+' finalizado!')
    connection.close()

if __name__ == "__main__":
    try: ServerSideSocket.bind((host, port))
    except socket.error as e: print(str(e))
    print('Servidor en escucha')
    ServerSideSocket.listen(5)

    while True:
        count += 1
        Client, address = ServerSideSocket.accept()
        print('Nueva conexion: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, str(count)))
    ServerSideSocket.close()