import socket
import os

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host = socket.gethostname()
udp_port = 12345
client = {}
count = 0

def save_into(c, bytes):
    if not os.path.exists("client"+c[0]): 
        os.makedirs("client"+c[0])
    filename = "client"+c[0]+"/chunk"+str(c[2])
    f = open(filename, "wb")
    f.write(bytes)
    f.close()

def merge_files(c):
	if not os.path.exists("res"): 
		os.makedirs("res")
	f = open("res/copy-"+c[1], "wb")
	for chunk in range(c[2]):
		try:
			filename = "client"+c[0]+"/chunk"+str(chunk)
			tmp = open(filename, "rb")
			bytes = tmp.read(200)
			f.write(bytes)
		except: pass
	f.close()
	print('Proceso de cliente '+c[0]+' finalizado!')

if __name__ == "__main__":
	sock.bind((udp_host, udp_port))
	print ("Servidor en escucha...")

	while True:
		data, addr = sock.recvfrom(1024)
		if addr not in client:
			count += 1
			filename = data.decode('utf-8')
			client[addr] = [str(count), filename, 0]
			print('Almacenando info del cliente '+client[addr][0])
		else:
			if data:
				chunk = client[addr][2]
				save_into(client[addr], data)
				client[addr][2] = chunk+1
			else: merge_files(client[addr])