import socket
import threading


print("Bem vindo ao Chat da massa!!")
nickname = input("Como deseja ser chamado: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55556))
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
            mensagem = client.recv(1024).decode('UTF-8')
            if mensagem == 'NICK':
                client.send(nickname.encode('UTF-8'))
            elif mensagem == 'QUIT':
                print("Conexão encerrada")
                mutex.acquire()
                client.close()
                encerrar_conexao = True
                mutex.release()
            elif mensagem == 'TESTE':
                print('O apelido já está em uso, escolha outro.!')
                mutex.acquire()
                client.close()
                encerrar_conexao = True
                mutex.release()
            elif mensagem.startswith('LIST'):
                lista_usuarios = trata_mensagem(mensagem)
                print(f'Usuários ativos:\n{lista_usuarios}')
            else:
                print(mensagem)
        except:
            print("Aconteceu um problema!")
            client.close()
            break


def write():
    while True:
        if encerrar_conexao:
            break
        
        mensagem = '{}: {}'.format(nickname, input(''))
        
        if mensagem[len(nickname)+2:].startswith('/'):
            if mensagem[len(nickname)+2:].startswith('/help'):
                client.send('HELP'.encode('UTF-8'))
            elif mensagem[len(nickname)+2:].startswith('/list'):
                client.send('LIST'.encode('UTF-8'))
            elif mensagem[len(nickname)+2:].startswith('/quit'):
                client.send(f'QUIT {mensagem[len(nickname)]}'.encode('UTF-8'))
            elif mensagem[len(nickname)+2:].startswith('/whisper'):
                client.send(f'WHISPER {mensagem[len(nickname)+2+9:]}'.encode('UTF-8'))
            else:
                print("Comando inválido, use /help para ver os comandos disponíveis")    
        else:
            client.send(mensagem.encode('UTF-8'))
        

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()