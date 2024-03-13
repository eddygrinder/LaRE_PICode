import socket

# Endereço IP e porta de escuta
HOST = ''  # Todos os endereços disponíveis
PORT = 12345  # Porta de escuta

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
       
        conn.close()
