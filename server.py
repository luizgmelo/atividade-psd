import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((HOST, PORT))
   s.listen()           
   print(f"Servidor escutando em {HOST}:{PORT}")


   while True: 
       conn, addr = s.accept()
       with conn:
           print(f"Conectado por {addr}")
           while True:
               data = conn.recv(1024)
               if not data:
                   break 
               print(data.decode('utf-8'))
               conn.sendall(data)