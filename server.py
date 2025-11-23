import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432

# Estruturas de dados
clients = {}  # {socket: nickname}
groups = {}  # {group_name: set(nicknames)}
offline_messages = {}  # {nickname: [messages]}
all_users = set()  # todos os usuários que já se conectaram


def get_socket_by_nickname(nickname):
    """Retorna o socket de um cliente pelo nickname"""
    for sock, nick in clients.items():
        if nick == nickname:
            return sock
    return None


def is_user_online(nickname):
    """Verifica se um usuário está online"""
    return nickname in clients.values()


def send_to_client(client_socket, message):
    """Envia mensagem para um cliente específico"""
    try:
        client_socket.send(message.encode('utf-8'))
        return True
    except:
        return False


def broadcast(message, sender=None):
    """Send message to all connected clients except the sender"""
    for client_socket, client_name in clients.items():
        try:
            if client_socket != sender:
                client_socket.send(message.encode('utf-8'))
        except:
            del clients[client_socket]


def handle_list_users(client_socket):
    """Lista todos os usuários online"""
    if not clients:
        send_to_client(client_socket, "Nenhum usuário conectado\n")
    else:
        online_users = list(clients.values())
        user_list = "Usuários online:\n" + "\n".join(f"- {user}" for user in online_users) + "\n"
        send_to_client(client_socket, user_list)


def handle_create_group(client_socket, client_name, group_name):
    """Cria um novo grupo"""
    if group_name in groups:
        send_to_client(client_socket, f"ERRO: Grupo '{group_name}' já existente\n")
    else:
        groups[group_name] = set()
        send_to_client(client_socket, f"Grupo '{group_name}' criado com sucesso\n")
        print(f"{client_name} created group '{group_name}'")


def handle_list_groups(client_socket):
    """Lista todos os grupos"""
    if not groups:
        send_to_client(client_socket, "ERRO: Nenhum grupo cadastrado\n")
    else:
        group_list = "Grupos disponíveis:\n" + "\n".join(f"- {group}" for group in groups.keys()) + "\n"
        send_to_client(client_socket, group_list)


def handle_list_group_users(client_socket, group_name):
    """Lista usuários de um grupo específico"""
    if group_name not in groups:
        send_to_client(client_socket, f"ERRO: Grupo '{group_name}' não cadastrado\n")
    else:
        members = groups[group_name]
        if not members:
            send_to_client(client_socket, f"Grupo '{group_name}' não possui membros\n")
        else:
            member_list = f"Membros do grupo '{group_name}':\n" + "\n".join(f"- {user}" for user in members) + "\n"
            send_to_client(client_socket, member_list)


def handle_join_group(client_socket, client_name, group_name):
    """Adiciona usuário a um grupo"""
    if group_name not in groups:
        send_to_client(client_socket, f"ERRO: Grupo '{group_name}' não existe\n")
    else:
        groups[group_name].add(client_name)
        send_to_client(client_socket, f"Você entrou no grupo '{group_name}'\n")
        print(f"{client_name} joined group '{group_name}'")


def handle_leave_group(client_socket, client_name, group_name):
    """Remove usuário de um grupo"""
    if group_name not in groups:
        send_to_client(client_socket, f"ERRO: Grupo '{group_name}' não existe\n")
    elif client_name not in groups[group_name]:
        send_to_client(client_socket, f"ERRO: Você não está no grupo '{group_name}'\n")
    else:
        groups[group_name].remove(client_name)
        send_to_client(client_socket, f"Você saiu do grupo '{group_name}'\n")
        print(f"{client_name} left group '{group_name}'")


def format_message(sender_nick, message_text, group_name=None):
    """Formata mensagem com (NICK, GRUPO, DATA/HORA) MENSAGEM"""
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if group_name:
        return f"({sender_nick}, {group_name}, {now}) {message_text}\n"
    else:
        return f"({sender_nick}, {now}) {message_text}\n"


def store_offline_message(recipient, message):
    """Armazena mensagem para usuário offline"""
    if recipient not in offline_messages:
        offline_messages[recipient] = []
    offline_messages[recipient].append(message)


def handle_direct_message(client_socket, client_name, args):
    """Envia mensagem direta para usuário ou grupo
    Formato: -msg U/G NICK/GRUPO MENSAGEM
    """
    parts = args.split(maxsplit=2)
    
    if len(parts) < 3:
        send_to_client(client_socket, "ERRO: Comando inválido. Use: -msg U/G NICK/GRUPO MENSAGEM\n")
        return
    
    msg_type = parts[0].upper()
    target = parts[1]
    message_text = parts[2]
    
    if msg_type == 'U':
        # Mensagem para usuário
        if target not in all_users:
            send_to_client(client_socket, f"ERRO: Usuário '{target}' não existe\n")
            return
        
        formatted_msg = format_message(client_name, message_text)
        
        if is_user_online(target):
            # Usuário online - envia diretamente
            target_socket = get_socket_by_nickname(target)
            if target_socket:
                send_to_client(target_socket, formatted_msg)
                send_to_client(client_socket, f"Mensagem enviada para {target}\n")
        else:
            # Usuário offline - armazena mensagem
            store_offline_message(target, formatted_msg)
            send_to_client(client_socket, f"Mensagem armazenada para {target} (offline)\n")
    
    elif msg_type == 'G':
        # Mensagem para grupo
        if target not in groups:
            send_to_client(client_socket, f"ERRO: Grupo '{target}' não existe\n")
            return
        
        if client_name not in groups[target]:
            send_to_client(client_socket, f"ERRO: Você não é membro do grupo '{target}'\n")
            return
        
        formatted_msg = format_message(client_name, message_text, target)
        members = groups[target]
        
        sent_count = 0
        offline_count = 0
        
        for member in members:
            if member != client_name:  # Não envia para si mesmo
                if is_user_online(member):
                    member_socket = get_socket_by_nickname(member)
                    if member_socket:
                        send_to_client(member_socket, formatted_msg)
                        sent_count += 1
                else:
                    store_offline_message(member, formatted_msg)
                    offline_count += 1
        
        send_to_client(client_socket, f"Mensagem enviada para grupo '{target}' ({sent_count} online, {offline_count} offline)\n")
    
    else:
        send_to_client(client_socket, "ERRO: Tipo inválido. Use U para usuário ou G para grupo\n")


def handle_broadcast_message(client_socket, client_name, args):
    """Envia mensagem broadcast
    Formato: -msgt C/D/T MENSAGEM
    C = usuários online
    D = usuários desconectados (offline)
    T = todos os usuários
    """
    parts = args.split(maxsplit=1)
    
    if len(parts) < 2:
        send_to_client(client_socket, "ERRO: Comando inválido. Use: -msgt C/D/T MENSAGEM\n")
        return
    
    broadcast_type = parts[0].upper()
    message_text = parts[1]
    formatted_msg = format_message(client_name, message_text)
    
    if broadcast_type == 'C':
        # Mensagem para todos online
        sent_count = 0
        for sock, nick in clients.items():
            if nick != client_name:
                send_to_client(sock, formatted_msg)
                sent_count += 1
        send_to_client(client_socket, f"Mensagem enviada para {sent_count} usuários online\n")
    
    elif broadcast_type == 'D':
        # Mensagem para todos offline
        online_users = set(clients.values())
        offline_users = all_users - online_users
        
        for user in offline_users:
            store_offline_message(user, formatted_msg)
        
        send_to_client(client_socket, f"Mensagem armazenada para {len(offline_users)} usuários offline\n")
    
    elif broadcast_type == 'T':
        # Mensagem para todos (online e offline)
        online_count = 0
        for sock, nick in clients.items():
            if nick != client_name:
                send_to_client(sock, formatted_msg)
                online_count += 1
        
        online_users = set(clients.values())
        offline_users = all_users - online_users
        
        for user in offline_users:
            store_offline_message(user, formatted_msg)
        
        send_to_client(client_socket, f"Mensagem enviada para {online_count} online e {len(offline_users)} offline\n")
    
    else:
        send_to_client(client_socket, "ERRO: Tipo inválido. Use C (online), D (offline) ou T (todos)\n")


def process_message(client_socket, client_name, message):
    """Processa comandos e mensagens do cliente"""
    if message.startswith('-'):
        # É um comando
        process_command(client_socket, client_name, message)
    else:
        # Mensagem sem comando - erro
        send_to_client(client_socket, "ERRO: Use -msg ou -msgt para enviar mensagens\n")


def process_command(client_socket, client_name, command):
    """Processa comandos do cliente"""
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    
    if cmd == '-listarusuarios':
        handle_list_users(client_socket)
    elif cmd == '-criargrupo':
        if len(parts) < 2:
            send_to_client(client_socket, "ERRO: Comando inválido. Use: -criargrupo NOME_DO_GRUPO\n")
        else:
            handle_create_group(client_socket, client_name, parts[1].strip())
    elif cmd == '-listargrupos':
        handle_list_groups(client_socket)
    elif cmd == '-listausrgrupo':
        if len(parts) < 2:
            send_to_client(client_socket, "ERRO: Comando inválido. Use: -listausrgrupo NOME_DO_GRUPO\n")
        else:
            handle_list_group_users(client_socket, parts[1].strip())
    elif cmd == '-entrargrupo':
        if len(parts) < 2:
            send_to_client(client_socket, "ERRO: Comando inválido. Use: -entrargrupo NOME_GRUPO\n")
        else:
            handle_join_group(client_socket, client_name, parts[1].strip())
    elif cmd == '-sairgrupo':
        if len(parts) < 2:
            send_to_client(client_socket, "ERRO: Comando inválido. Use: -sairgrupo NOME_GRUPO\n")
        else:
            handle_leave_group(client_socket, client_name, parts[1].strip())
    elif cmd == '-msg':
        if len(parts) < 2:
            send_to_client(client_socket, "ERRO: Comando inválido. Use: -msg U/G NICK/GRUPO MENSAGEM\n")
        else:
            handle_direct_message(client_socket, client_name, parts[1])
    elif cmd == '-msgt':
        if len(parts) < 2:
            send_to_client(client_socket, "ERRO: Comando inválido. Use: -msgt C/D/T MENSAGEM\n")
        else:
            handle_broadcast_message(client_socket, client_name, parts[1])
    else:
        send_to_client(client_socket, "ERRO: Comando inexistente\n")


def handle_client(client_socket, addr):
    """Handle a single client connection"""
    client_name = None
    try:
        # Recebe o nickname
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        
        # Verifica se o usuário já está conectado
        if client_name in clients.values():
            send_to_client(client_socket, "ERRO: Usuário já conectado\n")
            client_socket.close()
            return
        
        # Adiciona o cliente
        clients[client_socket] = client_name
        all_users.add(client_name)
        print(f"{client_name} connected from {addr}")
        send_to_client(client_socket, f"Bem-vindo {client_name}!\n")
        
        # Envia mensagens offline se houver
        if client_name in offline_messages:
            for msg in offline_messages[client_name]:
                send_to_client(client_socket, msg)
            del offline_messages[client_name]
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message or message.lower() == 'exit':
                break
            
            # Processa comandos ou mensagens
            process_message(client_socket, client_name, message.strip())
            
    except Exception as e:
        print(f"Error when handling client {addr}: {e}")
    finally:
        if client_socket in clients:
            name = clients[client_socket]
            del clients[client_socket]
            print(f"{name} disconnected")
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