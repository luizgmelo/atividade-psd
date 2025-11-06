import socket
import threading
import sys
from threading import Lock

def clear_line():
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()

def receive_messages(client_socket, print_lock):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
                
            clear_line()
            print(message, end='\n')
            sys.stdout.write('>> ')
            sys.stdout.flush()
            
        except Exception as e:
            print("\nError receiving message:", str(e))
            break

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 65432

    try:
        client.connect((server_ip, server_port))
        
        client_name = input("Enter your name: ")
        client.send(client_name.encode('utf-8'))
        
        print_lock = Lock()
        
        receive_thread = threading.Thread(target=receive_messages, args=(client, print_lock))
        receive_thread.daemon = True
        receive_thread.start()
        
        print("Connected to chat! Type 'exit' to quit.")
        
        while True:
            try:
                message = input('>> ')
                
                if message.lower() == 'exit':
                    client.send("exit".encode('utf-8'))
                    break
                    
                client.send(message.encode('utf-8'))
                
            except KeyboardInterrupt:
                client.send("exit".encode('utf-8'))
                break
            except Exception as e:
                print(f"Error: {e}")
                break
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Disconnected from server")

if __name__ == "__main__":
    run_client()