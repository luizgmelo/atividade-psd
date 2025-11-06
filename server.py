import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = {}


def broadcast(message, sender=None):
    """Send message to all connected clients except the sender"""
    for client_socket, client_name in clients.items():
        try:
            if client_socket != sender:
                client_socket.send(message.encode('utf-8'))
        except:
            del clients[client_socket]


def handle_client(client_socket, addr):
    """Handle a single client connection"""
    try:
        client_name = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = client_name
        print(f"{client_name} connected from {addr}")
        broadcast(f"{client_name} joined the chat!\n", client_socket)
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message or message.lower() == 'exit':
                break
                
            formatted_message = f"{client_name}: {message}\n"
            print(f"{formatted_message.strip()}")
            broadcast(formatted_message, client_socket)
            
    except Exception as e:
        print(f"Error when handling client {addr}: {e}")
    finally:
        if client_socket in clients:
            name = clients[client_socket]
            del clients[client_socket]
            broadcast(f"{name} left the chat\n")
        client_socket.close()
        print(f"Connection to {addr} closed")


def run_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Chat server is running on {HOST}:{PORT}")
        print("Waiting for connections...")

        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()
        print("Server closed")


if __name__ == "__main__":
    run_server()