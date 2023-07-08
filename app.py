from flask import Flask, Response
from obd import OBDStatus, commands, OBD
import time, sys

app = Flask(__name__)
port = "/dev/pts/1"

# Stream the data using Flask
@app.route('/stream')
def stream_data():
    pids = [
        commands.RPM,               # 0C
        commands.SPEED,             # 0D
        commands.COOLANT_TEMP,      # 05
        commands.THROTTLE_POS,      # 11
        commands.INTAKE_PRESSURE,   # 0B
        commands.RUN_TIME,          # 1F
    ]

    # Connect to the OBD-II adapter
    connection = OBD(port)
    if connection.status() == OBDStatus.NOT_CONNECTED:
        print("Failed to connect to the OBD-II adapter")
        exit()
    if connection.status() == OBDStatus.CAR_CONNECTED:
        print("The OBD-II adapter has established a connection with the vehicle!\nEntering execution mode...")
        time.sleep(3)  # Wait for 5 seconds for the vehicle to respond

    def generate_data():
        i = 0
        while True:
            read = []
            for pid in pids:
                response = connection.query(pid)
                data = {
                    "PID Name": pid.desc,
                    "unit": str(response.value.unit),
                    "magnitude": response.value.magnitude,
                    "string": str(response.value),
                }
                read.append(data)
            read = {"read": read}
            yield "<script> document.body.innerHTML = ''</script>"
            yield str(read)
            time.sleep(0.5)  # 0.5-second interval
    return Response(generate_data(), mimetype='text/html')

if __name__ == '__main__':
    # get port to use obd protocol
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(host='0.0.0.0')
