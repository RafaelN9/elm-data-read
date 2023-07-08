from flask import Flask, Response, jsonify
from obd import OBDStatus, commands, OBD
import time

app = Flask(__name__)

# Stream the data using Flask
@app.route('/stream')
def stream_data():
    # Define the PIDs
    pids = [
        commands.RPM,               # 0C
        commands.SPEED,             # 0D
        commands.COOLANT_TEMP,      # 05
        commands.THROTTLE_POS,      # 11
        commands.INTAKE_PRESSURE,   # 0B
        commands.RUN_TIME,          # 1F
    ]

    # # Connect to the OBD-II adapter
    # connection = OBD("/dev/ttys009")
    # if connection.status() == OBDStatus.NOT_CONNECTED:
    #     print("Failed to connect to the OBD-II adapter")
    #     exit()
    # if connection.status() == OBDStatus.CAR_CONNECTED:
    #     print("The OBD-II adapter has established a connection with the vehicle!\nEntering execution mode...")
    #     time.sleep(3)  # Wait for 5 seconds for the vehicle to respond

    def generate_data():
        i = 0
        while True:
            # row = []
            # for pid in pids:
            #     response = connection.query(pid)
            #     data = f"{pid.desc}: {response.value}"
            #     yield data + '\n'
            #     row.append(response.value.magnitude)
            i += 1
            yield f"Hello World{i}\n"
            time.sleep(0.5)  # 0.5-second interval

    return Response(generate_data(), mimetype='text/plain')

@app.route('/bar-size', methods=['GET'])
def get_bar_size():
    # Replace this with your logic to determine the bar size
    bar_size = 0.1

    response = {
        'barSize': bar_size
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
