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

def print_help():
    """Exibe ajuda com todos os comandos disponíveis"""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║                    COMANDOS DISPONÍVEIS                        ║
╠════════════════════════════════════════════════════════════════╣
║ -listarusuarios                                                ║
║   Lista todos os usuários online                               ║
║                                                                ║
║ -criargrupo NOME_DO_GRUPO                                      ║
║   Cria um novo grupo                                           ║
║                                                                ║
║ -listargrupos                                                  ║
║   Lista todos os grupos disponíveis                            ║
║                                                                ║
║ -listausrgrupo NOME_DO_GRUPO                                   ║
║   Lista todos os membros de um grupo                           ║
║                                                                ║
║ -entrargrupo NOME_GRUPO                                        ║
║   Entra em um grupo existente                                  ║
║                                                                ║
║ -sairgrupo NOME_GRUPO                                          ║
║   Sai de um grupo                                              ║
║                                                                ║
║ -msg U NICKNAME MENSAGEM                                       ║
║   Envia mensagem para um usuário específico                    ║
║                                                                ║
║ -msg G GRUPO MENSAGEM                                          ║
║   Envia mensagem para um grupo (precisa ser membro)            ║
║                                                                ║
║ -msgt C MENSAGEM                                               ║
║   Envia mensagem para todos os usuários online                 ║
║                                                                ║
║ -msgt D MENSAGEM                                               ║
║   Envia mensagem para todos os usuários offline                ║
║                                                                ║
║ -msgt T MENSAGEM                                               ║
║   Envia mensagem para todos os usuários (online e offline)     ║
║                                                                ║
║ -ajuda ou -help                                                ║
║   Exibe esta mensagem de ajuda                                 ║
║                                                                ║
║ exit                                                           ║
║   Sai do chat                                                  ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 65432

    try:
        client.connect((server_ip, server_port))
        
        client_name = input("Digite seu nome (nickname): ")
        client.send(client_name.encode('utf-8'))
        
        print_lock = Lock()
        
        receive_thread = threading.Thread(target=receive_messages, args=(client, print_lock))
        receive_thread.daemon = True
        receive_thread.start()
        
        print("\n╔════════════════════════════════════════════════════════════════╗")
        print("║          Conectado ao chat! Digite -ajuda para ver comandos   ║")
        print("╚════════════════════════════════════════════════════════════════╝\n")
        
        while True:
            try:
                message = input('>> ')
                
                if not message.strip():
                    continue
                
                if message.lower() == 'exit':
                    client.send("exit".encode('utf-8'))
                    break
                
                if message.lower() in ['-ajuda', '-help']:
                    print_help()
                    continue
                    
                client.send(message.encode('utf-8'))
                
            except KeyboardInterrupt:
                print("\n\nEncerrando...")
                client.send("exit".encode('utf-8'))
                break
            except Exception as e:
                print(f"Erro: {e}")
                break
            
    except Exception as e:
        print(f"Erro ao conectar: {e}")
    finally:
        client.close()
        print("Desconectado do servidor")

if __name__ == "__main__":
    run_client()