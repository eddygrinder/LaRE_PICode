import socket

from shift_register import commandRelays

# Endereço IP e porta de escuta
HOST = ''  # Todos os endereços disponíveis
PORT = 12345  # Porta de escuta

def send_confirmation_back (acknowledge:str):
    # Envia a string para o Raspberry PC
    # Endereço IP e porta do Raspberry PC
    HOST = '192.168.1.88'  # Substitua pelo endereço IP do Raspberry servidor
    PORT = 12345  # Porta de escuta no Raspberry Pi 
    
        # Criar um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar-se ao servidor (Raspberry Pi)
        s.connect((HOST, PORT))
        
        # Enviar a mensagem
        s.sendall(acknowledge.encode())
        print("Mensagem enviada com sucesso.")

# Criar um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Vincular o socket ao endereço e porta de escuta
    s.bind((HOST, PORT))
    
    # Aguardar por conexões de clientes
    s.listen()
    
    print("Aguardando conexões...")
    while True:
        # Aceitar a conexão
        conn, addr = s.accept()
        print('Conectado por', addr)
        
        while True:
            # Receber a mensagem
            data = conn.recv(1024)
            if not data:    
                break
                
            string = data.decode()
            print("Msg recebida:", string)
            # Processar o comando
            acknowledgment = commandRelays(string)
            # Enviar confirmação de volta ao cliente
            confirmation = 'True' if acknowledgment else 'False'
            conn.sendall(confirmation.encode())
        conn.close()

