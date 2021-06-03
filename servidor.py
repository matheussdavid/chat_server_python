import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55558

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('UTF-8').startswith('HELP'):
                client.send('Comandos Disponíveis:\n*/help - Mostra os comandos disponíveis\n*/list - Lista os usuários online\n*/quit nomeDoUsuario - Para sair do chat'.encode('UTF-8'))
            elif msg.decode('UTF-8').startswith('LIST'):
                client.send(f'LIST {nicknames}'.encode('UTF-8'))
            elif msg.decode('UTF-8').startswith('QUIT'):
                usuario = msg.decode('UTF-8')[5:]
                sair(usuario)
                client.send('QUIT'.encode('UTF-8'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.send('QUIT'.encode('UTF-8'))
            client.close()
            nickname = nicknames[index]
            broadcast('{} saiu da sala!'.format(nickname).encode('UTF-8'))
            nicknames.remove(nickname)            
            break
        
def sair(usuario):
    if usuario in clients:
        index = clients.index(usuario)
        clients.remove(usuario)
        usuario.close()
        nickname = nicknames[index]
        broadcast('{} saiu da sala!'.format(nickname).encode('UTF-8'))
        nicknames.remove(nickname)    
        
def receive():
    while True:
        print("Servidor online!!")
        client, address = server.accept()
        print("Conexão estabelecida com {}".format(str(address)))

        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(client)
        
        print("Seu Apelido é {}".format(nickname))
        broadcast("{} entrou na sala, dê as boas vindas!\n".format(nickname).encode('UTF-8'))
        client.send('Conexão estabelecida com o servidor! Seja bem-vindo'.encode('UTF-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()        
        

