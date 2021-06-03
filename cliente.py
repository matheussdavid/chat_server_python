import socket
import threading
import sys

# Choosing Nickname
print("Bem vindo ao Humortadela!!")
nickname = input("Como deseja ser chamado: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55558))

encerrar_conexao = False

# Listening to Server and Sending Nickname
def receive():
    while True:
        global encerrar_conexao
        if encerrar_conexao:
            break
        
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            elif message == 'QUIT':
                print("Conexão encerrada")
                client.close()
                encerrar_conexao = True
                exit(0)
            else:
                print(message)
        except:
            # Close Connection When Error
            print("Aconteceu um problema!")
            client.close()
            exit(0)
            break

# Sending Messages To Server
def write():
    while True:
        if encerrar_conexao:
            break
        
        message = '{}: {}'.format(nickname, input(''))
        if message[len(nickname)+2:].startswith('/'):
            if message[len(nickname)+2:].startswith('/help'):
                client.send('HELP'.encode('UTF-8'))
            elif message[len(nickname)+2:].startswith('/list'):
                client.send('LIST'.encode('UTF-8'))
            elif message[len(nickname)+2:].startswith('/quit'):
                client.send(f'QUIT {message[len(nickname)+2+6]}'.encode('UTF-8'))
            else:
                print("Comando inválido, use /help para ver os comandos disponíveis")    
        else:
            client.send(message.encode('UTF-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()