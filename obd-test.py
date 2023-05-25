import obd
from obd import OBDStatus
import time
import csv

# Define os PIDs
pids = [
    obd.commands.RPM,               # 0C
    obd.commands.SPEED,             # 0D
    obd.commands.COOLANT_TEMP,      # 05
    obd.commands.THROTTLE_POS,      # 11
    obd.commands.INTAKE_PRESSURE,   # 0B
    obd.commands.RUN_TIME,          # 1F
]

# Conecta com o adaptador OBD-II
connection = obd.OBD("/dev/pts/2")
if connection.status() == OBDStatus.NOT_CONNECTED:
    print("Não foi possível conectar ao adaptador OBD-II")
    exit()
if connection.status() == OBDStatus.CAR_CONNECTED:
    print("O adaptador OBD-II iniciou a conexão com o veículo!\nEntrando em modo de execução...")
    time.sleep(3)  # Aguarda 5 segundos para o veículo responder

# Cria uma lista para armazenar os dados
data = []

# Faz a leitura e armazenamento dos dados
def read_and_store_data():
    row = []
    for pid in pids:
        response = connection.query(pid)
        print(f"{pid.desc}: {response.value}")
        row.append(response.value.magnitude)
    data.append(row)

# Realiza leitura e armazenamento dos dados continuamente
try:
    while True:
        read_and_store_data()
        time.sleep(0.5)  # Intervalo de 0.5 segundos
        print("\033c", end="")  # Limpa o terminal
except KeyboardInterrupt:
    # Exporta os dados para um arquivo CSV
    with open('obd_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow([pid.desc for pid in pids])
        for row in data:
            writer.writerow(row)
