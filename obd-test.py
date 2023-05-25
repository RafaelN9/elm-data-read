import obd
import time

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

# Leitura e exibição dos dados
def read_and_display_data():
    for pid in pids:
        response = connection.query(pid)
        print(f"{pid.desc}: {response.value}")

# Leitura e exibição dos dados contínua
while True:
    read_and_display_data()
    time.sleep(0.5)  # Tempo de atualização
    print("\033c", end="")  # Limpa o terminal
