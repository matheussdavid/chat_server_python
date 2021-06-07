import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55557

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
mutex = threading.Semaphore(1)

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

help = '''
Comandos Disponíveis:
*/help - Mostra os comandos disponíveis
*/list - Lista os usuários online
*/quit - Para sair do chat
*/whisper - envia uma mensagem privada (Ex: nomeDoUsuario: mensagem'''

def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('UTF-8').startswith('HELP'):
                client.send(help.encode('UTF-8'))
            elif msg.decode('UTF-8').startswith('LIST'):
                client.send(f'LIST {nicknames}'.encode('UTF-8'))
            elif msg.decode('UTF-8').startswith('QUIT'):
                usuario = msg.decode('UTF-8')[5:]
                sair(usuario, client)
                broadcast('{} saiu da sala!'.format(nickname).encode('UTF-8'))
                client.send('QUIT'.encode('UTF-8'))
            elif msg.decode('UTF-8').startswith('WHISPER'):
                mensagem = msg.decode('UTF-8')[8:]
                whisper(mensagem)            
            else:
                broadcast(message)
        except:
            mutex.acquire()
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} saiu da sala!'.format(nickname).encode('UTF-8'))
            nicknames.remove(nickname)
            mutex.release()         
            break
        
def whisper(mensagem):
    teste = mensagem.split(":")
    usuario = teste[0]
    sender = teste[1]
    mensagem = teste[2]
    if usuario in nicknames:
        posicao = nicknames.index(usuario)
        cliente = clients[posicao]
        cliente.send(f'Mensagem privada: {sender}: {mensagem}'.encode('UTF-8'))
    else:
        client.send()
        
def sair(usuario, client):
    if usuario in clients:
        mutex.acquire()
        index = clients.index(usuario)
        clients.remove(usuario)
        client.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)    
        mutex.release()   
        
def receive():
    while True:
        print("Servidor online!!")
        client, address = server.accept()
        print("Conexão estabelecida com {}".format(str(address)))

        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        
        print("Seu Apelido é {}".format(nickname))
        broadcast("{} entrou na sala, dê as boas vindas!\n".format(nickname).encode('UTF-8'))
        client.send('Conexão estabelecida com o servidor! Seja bem-vindo'.encode('UTF-8'))
        
        mutex.acquire()   
        nicknames.append(nickname)
        clients.append(client)
        mutex.release()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()        
        

