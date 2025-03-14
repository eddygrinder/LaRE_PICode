import gpiod
from gpiod.line import Direction, Value

import time

import warnings
#warnings.filterwarnings("ignore")

RCLK = 6             # GPIO 6 - RCLK/STCP - 17
SRCLK = 13           # GPIO 13 - SRCLK/SHCP (storage register clock pin, SPI clock) - 4
SRCLR = 26           # GPIO 26 - O registo de deslocamento � limpo (ACTIVO BAIXO) - 11

RCLK_MEIAONDA = 17   # GPIO 11
SRCLK_MEIAONDA = 4   # GPIO 4
SRCLR_MEIAONDA = 11  # GPIO 11

SER_OHM = 5              # GPIO 5 - SER/DS (serial data input, SPI data)
OE_OHM = 19          # GPIO 19 - Enable/Disable do SR - OHM

SER_MEIAONDA = 27    # GPIO 12 - SER/DS (serial data input, SPI data)
OE_MEIAONDA = 22     # GPIO 23 - Enable/Disable do SR - MEIA ONDA

OFF = Value.INACTIVE
ON = Value.ACTIVE

# Valor por defeito de espera nas operações do registo de deslocamento
WaitTimeSR = 0.01

# Configuração para cada pino GPIO
configs = {
    SER_OHM: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    OE_OHM: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SER_MEIAONDA: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    RCLK: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SRCLK: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SRCLR: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    RCLK_MEIAONDA: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SRCLK_MEIAONDA: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    SRCLR_MEIAONDA: gpiod.LineSettings(
        direction=Direction.OUTPUT, output_value=Value.ACTIVE
    ),
    OE_MEIAONDA: gpiod.LineSettings(
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

# Limpa os registos de deslocamento
request.set_value(SRCLR, OFF)
time.sleep(WaitTimeSR)
request.set_value(SRCLR, ON)

request.set_value(SRCLR_MEIAONDA, OFF)
time.sleep(2)
request.set_value(SRCLR_MEIAONDA, ON)

# Ambos os Enables ficam desactivados por defeito
request.set_value(OE_OHM, ON)
request.set_value(OE_MEIAONDA, ON)


# Fun��o que verifica e desloca os bits para armazenar no registo de deslocamento
def commandRelays(checkshift:str):
    n_bits = len(checkshift)
    #print (n_bits)
    #print(checkshift)

    # Converter a string recebida para binário
    binaryString = int(checkshift, 2)
    
    if n_bits == 8: #CRITÉRIO - número de bits corresponmdendete aos 8 reles da lei de ohm 
        # O critério para seleccionar qual o registo a activar é o número de bits recebido, caso 
        # fossem iguais, poderia ser enviado um bit adicional de controlo
        SER_pin_ctrl = SER_OHM
        SERCLK_pin_ctrl = SRCLK
        RCLK_pin_ctrl = RCLK
        request.set_value(OE_MEIAONDA, ON) # Desactiva o registo de deslocamento referente à meia onda
        request.set_value(OE_OHM, OFF) # Activa o registo de deslocamento referente à lei de Ohm
    elif n_bits == 13: #CRITÉRIO - número de bits corresponmdendete aos 7 reles da lei de meia onda
        SER_pin_ctrl = SER_MEIAONDA
        SERCLK_pin_ctrl = SRCLK_MEIAONDA
        RCLK_pin_ctrl = RCLK_MEIAONDA
        request.set_value(OE_OHM, ON)
        request.set_value(OE_MEIAONDA, OFF)  # Activa o registo de deslocamento referente à meia onda
    
    for i in range(n_bits):
        binaryShift = binaryString & 1
        #print(binaryShift)
        #time.sleep(5)

        if binaryShift == 1:
            WriteReg (ON, SERCLK_pin_ctrl, SER_pin_ctrl, WaitTimeSR)
        else:
            WriteReg(OFF, SERCLK_pin_ctrl, SER_pin_ctrl, WaitTimeSR)
        binaryString = binaryString >> 1
    OutputReg(RCLK_pin_ctrl)
    return True # Fim da transmissão da trama de bits, relés activados

# Defini��o da fun��o que envia os dados para o registo de deslocamento,
# segundo o algoritmo descrito em baixo

### ALGORITMO ###
# Enviar um bit para o pino SER/DS
### Depois de enviado, � dado um impulso de clock (SRCLK/SHCP) e o bit armazenado nos registos
###### ... um segundo bit � enviado, repetindo os dois passos em cima - � repetido at� estarem armazenados 8 bits
######### Por ultimo � dado um impulso aos registos (RCLK/STCP) para obter os 8 bits na saida

def WriteReg (WriteBit, SERCLK_pin_ctrl, SER_pin_ctrl:int, WaitTimeSR:float):
    request.set_value(SER_pin_ctrl, WriteBit) #GPIO.output (SER,WriteBit) # Envia o bit para o registo
    time.sleep (WaitTimeSR) # Espera 100ms
    request.set_value(SERCLK_pin_ctrl, ON) #GPIO.output(SRCLK,1)
    time.sleep(WaitTimeSR)
    request.set_value(SERCLK_pin_ctrl, OFF) #GPIO.output (SRCLK, 0)  # Clock - flanco POSITIVO

# Funcao que limpa o registo
def register_clear ():
    request.set_value(SRCLK_MEIAONDA,OFF) #GPIO.output(SRCLK, 0)
    time.sleep(WaitTimeSR) # espera 100ms
    request.set_value(SRCLK_MEIAONDA,ON) #GPIO.output(SRCLK, 1)

# Armazenar o valor no registo
def OutputReg (RCLK_pin_ctrl:int):
    request.set_value(RCLK_pin_ctrl, OFF) #GPIO.output(RCLK, 0)
    time.sleep(WaitTimeSR)
    request.set_value(RCLK_pin_ctrl, ON) #GPIO.output(RCLK, 1)
    #time.sleep(10)
    #request.release()
