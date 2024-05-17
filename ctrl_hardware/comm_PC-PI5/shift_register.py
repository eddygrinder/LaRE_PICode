import gpiod
from gpiod.line import Direction, Value

import time

import warnings
#warnings.filterwarnings("ignore")

SER = 5              # GPIO 5 - SER/DS (serial data input, SPI data)
RCLK = 6             # GPIO 6 - RCLK/STCP
SRCLK = 13           # GPIO 13 - SRCLK/SHCP (storage register clock pin, SPI clock)
OE_ohm = 19              # GPIO 19 - Enable/Disable do SR - OHM
SRCLR = 26           # GPIO 26 - O registo de deslocamento � limpo (ACTIVO BAIXO)

OE_meiaonda = 23         # GPIO 23 - Enable/Disable do SR - MEIA ONDA

OFF = Value.INACTIVE
ON = Value.ACTIVE

# Valor por defeito de espera nas operações do registo de deslocamento
WaitTimeSR = 0.1

# Configuração para cada pino GPIO
configs = {
    SER: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    RCLK: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SRCLK: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    OE_ohm: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SRCLR: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    OE_meiaonda: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
}


 # Solicitação das linhas GPIO
request = gpiod.request_lines(
    "/dev/gpiochip4",
    consumer="controlo_GPIO's",
    config=configs
)
    
    #####################################################
    # Tabela de verdade do Registo de Deslocamento
    # SER | SRCLK | 'SRCLR | RCLK |  'OE | Sa�das/Fun��es
    #  X      X       X       X       H    Q's inactivas
    #  X      X       X       X       L    Q'S activos
    #  X      X       L       X       X    SR limpo
    #  L    + et      H       X       X    0 no SR
    #  H    + et      H       X       X    1 no SR
    #  X      X       X     +et       X   dados out
    ######################################################

# Limpa o registo de deslocamento
request.set_value(SRCLR, OFF)
time.sleep(WaitTimeSR)
request.set_value(SRCLR, ON)

# Ambos os Enables ficam desactivados por defeito
request.set_value(OE_ohm, ON)
request.set_value(OE_meiaonda, ON)

# Fun��o que verifica e desloca os bits para armazenar no registo de deslocamento
def commandRelays(checkshift:str):
    n_bits = len(checkshift)
    print(checkshift)

    # Converter a string recebida para binário
    binaryString = int(checkshift, 2)
    
    if n_bits == 8: #CRITÉRIO - número de bits corresponmdendete aos 8 reles da lei de ohm 
        # O critério para seleccionar qual o registo a activar é o número de bits recebido, caso 
        # fossem iguais, poderia ser enviado um bit adicional de controlo
        request.set_value(OE_ohm, OFF) # Activa o registo de deslocamento referente à lei de Ohm
    elif n_bits == 7: #CRITÉRIO - número de bits corresponmdendete aos 7 reles da lei de meia onda
        request.set_value(OE_meiaonda,OFF)  # Activa o registo de deslocamento referente à meia onda
    
    for i in range(n_bits):
        binaryShift = binaryString & 1
        print(binaryShift)

        if binaryShift == 1:
            print ("UM")
            WriteReg (ON, WaitTimeSR)
        else:
            print ("ZERO")
            WriteReg(OFF, WaitTimeSR)
        binaryString = binaryString >> 1
    OutputReg()

# Defini��o da fun��o que envia os dados para o registo de deslocamento,
# segundo o algoritmo descrito em baixo

### ALGORITMO ###
# Enviar um bit para o pino SER/DS
### Depois de enviado, � dado um impulso de clock (SRCLK/SHCP) e o bit armazenado nos registos
###### ... um segundo bit � enviado, repetindo os dois passos em cima - � repetido at� estarem armazenados 8 bits
######### Por ultimo � dado um impulso aos registos (RCLK/STCP) para obter os 8 bits na saida

def WriteReg (WriteBit, WaitTimeSR):
    request.set_value(SER, WriteBit) #GPIO.output (SER,WriteBit) # Envia o bit para o registo
    time.sleep (WaitTimeSR) # Espera 100ms
    request.set_value(SRCLK, ON) #GPIO.output(SRCLK,1)
    time.sleep(WaitTimeSR)
    request.set_value(SRCLK, OFF) #GPIO.output (SRCLK, 0)  # Clock - flanco POSITIVO

# Funcao que limpa o registo
def register_clear ():
    request.set_value(SRCLK,OFF) #GPIO.output(SRCLK, 0)
    time.sleep(WaitTimeSR) # espera 100ms
    request.set_value(SRCLK,ON) #GPIO.output(SRCLK, 1)

# Armazenar o valor no registo
def OutputReg ():
    request.set_value(RCLK, OFF) #GPIO.output(RCLK, 0)
    time.sleep(WaitTimeSR)
    request.set_value(RCLK, ON) #GPIO.output(RCLK, 1)
    #time.sleep(10)
    #request.release()
