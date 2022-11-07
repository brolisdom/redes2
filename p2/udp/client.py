
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host = socket.gethostname()
udp_port = 12345
split = []

def split_file(filename):
    with open("../files/"+filename, "rb") as in_file:
        bytes = in_file.read(200) 
        while bytes:
            split.append(bytes)
            bytes = in_file.read(200)

if __name__ == "__main__":
    while True:
        f = input('Escribe el nombre del archivo: ')
        try:
            chunk = 0
            split_file(f)
            sock.sendto(str.encode(f), (udp_host, udp_port))
            for i in split:
                sock.sendto(i, (udp_host, udp_port))
                print('Chunk '+str(chunk)+' almacenado')
                chunk += 1
            break
        except: print('El archivo no existe!')
    print('El envio del archivo se ha completado!')
    sock.sendto(b'', (udp_host, udp_port))

