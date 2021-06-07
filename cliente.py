import socket
import threading


print("Bem vindo ao Humortadela!!")
nickname = input("Como deseja ser chamado: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55559))


mutex = threading.Semaphore(1)


encerrar_conexao = False


def trata_mensagem(mensagem):
    users = mensagem.replace("LIST", "")
    users = users.replace(",", "\n")
    users = users.replace("'", "")
    users = users.replace("[", "")
    users = users.replace("]", "")
    users = users.replace(" ", "")
    return users


def receive():
    while True:
        global encerrar_conexao
        if encerrar_conexao:
            break

        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            elif message == 'QUIT':
                print("Conexão encerrada")
                mutex.acquire()
                client.close()
                encerrar_conexao = True
                mutex.release()
            elif message == 'TESTE':
                print('O apelido já está em uso, escolha outro.!')
                client.close()
                encerrar_conexao = True
            elif message.startswith('LIST'):
                lista_usuarios = trata_mensagem(message)
                print(f'Usuários ativos:\n{lista_usuarios}')
            else:
                print(message)
        except:
            print("Aconteceu um problema!")
            client.close()
            break


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
                client.send(f'QUIT {message[len(nickname)]}'.encode('UTF-8'))
            elif message[len(nickname)+2:].startswith('/whisper'):
                client.send(f'WHISPER {message[len(nickname)+2+9:]}'.encode('UTF-8'))
            else:
                print("Comando inválido, use /help para ver os comandos disponíveis")    
        else:
            client.send(message.encode('UTF-8'))
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()