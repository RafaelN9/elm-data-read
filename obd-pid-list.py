import obd

# Connect to the OBD-II adapter
connection = obd.OBD("/dev/pts/2")

# Function to check if a PID is supported
def is_pid_supported(pid):
    response = connection.query(pid)
    return response.is_null() == False

# Iterate through all PIDs and check if they are supported
supported_pids = []
for pid in obd.commands.__dict__.values():
    if isinstance(pid, obd.OBDCommand) and is_pid_supported(pid):
        supported_pids.append(pid)

# Print the supported PIDs
for pid in supported_pids:
    print(f"{pid.command}: {pid.desc}")
