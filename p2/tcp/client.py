import socket

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
split = []

def split_file(filename):
    with open("../files/"+filename, "rb") as in_file:
        bytes = in_file.read(200) 
        while bytes:
            split.append(bytes)
            bytes = in_file.read(200)

if __name__ == "__main__":
    try: ClientMultiSocket.connect((host, port))
    except socket.error as e: print(str(e))
    res = ClientMultiSocket.recv(1024)

    while True:
        f = input('Escribe el nombre del archivo: ')
        try: 
            split_file(f)
            ClientMultiSocket.send(str.encode(f))
            for i in split: 
                ClientMultiSocket.send(i)
                res = ClientMultiSocket.recv(1024)
                print(res.decode('utf-8'))
            break
        except: print('El archivo no existe!')
    print('El envio del archivo se ha completado!')
    ClientMultiSocket.close()