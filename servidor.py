import socket
import threading


host = '127.0.0.1'
port = 55556


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
mutex = threading.Semaphore(1)


clients = []
nicknames = []

help = '''
Comandos Disponíveis:
*/help - Mostra os comandos disponíveis
*/list - Lista os usuários online
*/quit - Para sair do chat
*/whisper - Envia uma mensagem privada (Ex: /whisper nomeDoDestinatario: nomeDeQuemEnvia: mensagem)'''

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
    msg = mensagem.split(":")
    usuario = msg[0]
    remetente = msg[1].replace(" ", "")
    mensagem = msg[2]
    if usuario in nicknames:
        posicao = nicknames.index(usuario)
        cliente = clients[posicao]
        cliente.send(f'Mensagem privada: {remetente}:{mensagem}'.encode('UTF-8'))
    else:
        posicao = nicknames.index(remetente)
        cliente = clients[posicao]
        cliente.send('Não foi possível enviar sua mensagem privada, este usuário não foi encontrado!'.encode('UTF-8'))
        
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
        client, address = server.accept()
        print("Conexão estabelecida com {}".format(str(address)))

        client.send('NICK'.encode('UTF-8'))
        nickname = client.recv(1024).decode('UTF-8')
        
        if nickname in nicknames:
            client.send('TESTE'.encode('UTF-8'))
            client.close()
            continue
        
        print("Seu Apelido é {}".format(nickname))
        broadcast("{} entrou na sala, dê as boas vindas!\n".format(nickname).encode('UTF-8'))
        client.send('Conexão estabelecida com o servidor! Seja bem-vindo'.encode('UTF-8'))
        
        mutex.acquire()   
        nicknames.append(nickname)
        clients.append(client)
        mutex.release()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Servidor online!!")
receive()        
        

