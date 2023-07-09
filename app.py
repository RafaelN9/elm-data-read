from flask import Flask, Response
from obd import OBDStatus, commands, OBD
import time, sys

app = Flask(__name__)
port = "/dev/pts/1"

# Stream the data using Flask
@app.route('/stream')
def stream_data():
    ETHANOL_AFR = 9.8
    ETHANOL_DENSITY = 789.45
    GASOLINE_AFR = 14.7
    GASOLINE_DENSITY = 748.9
    KPA_TO_GRAMS_PER_SECOND_CONSTANT = 340.29

    pid_mapping = {
        'Run Time': commands.RUN_TIME,
        'Fuel Type': commands.FUEL_TYPE,
        'Throttle': commands.THROTTLE_POS,
        'MAF': commands.MAF,
        'RPM': commands.RPM,
        'Speed': commands.SPEED,
        'Ethanol %': commands.ETHANOL_PERCENT,
        'Torque': commands.ENGINE_TORQUE,
        'Fuel Rate': commands.ENGINE_FUEL_RATE,
        'Load %': commands.ABSOLUTE_LOAD,
        'Intake Pressure': commands.INTAKE_PRESSURE,
    }

    # Connect to the OBD-II adapter
    connection = OBD(port)
    if connection.status() == OBDStatus.NOT_CONNECTED:
        print("Failed to connect to the OBD-II adapter")
        exit()
    if connection.status() == OBDStatus.CAR_CONNECTED:
        print("The OBD-II adapter has established a connection with the vehicle!\nEntering execution mode...")
        time.sleep(3)  # Wait for 5 seconds for the vehicle to respond

    def generate_data():
        while True:
            # Get the data from the OBD-II adapter
            run_time = connection.query(pid_mapping['Run Time']).value
            throttle = connection.query(pid_mapping['Throttle']).value
            fuel_type = connection.query(pid_mapping['Fuel Type']).value
            air_intake = connection.query(pid_mapping['MAF']).value
            if not air_intake:
                air_intake = connection.query(pid_mapping['Intake Pressure']).value
            rpm = connection.query(pid_mapping['RPM']).value
            speed = connection.query(pid_mapping['Speed']).value
            ethanol = connection.query(pid_mapping['Ethanol %']).value
            fuel_rate = connection.query(pid_mapping['Fuel Rate']).value
            load = connection.query(pid_mapping['Load %']).value

            # Calculate litres per hour using air intake
            if fuel_type == 'Gasoline':
                grams_per_second = air_intake * KPA_TO_GRAMS_PER_SECOND_CONSTANT * GASOLINE_AFR
                estimated_fuel_rate = (grams_per_second * 3600) / GASOLINE_DENSITY
            elif fuel_type == 'Ethanol':
                grams_per_second = air_intake * KPA_TO_GRAMS_PER_SECOND_CONSTANT * ETHANOL_AFR
                estimated_fuel_rate = (grams_per_second * 3600) / ETHANOL_DENSITY
            else:
                estimated_fuel_rate = None

            # Calculate fuel efficiency
            fuel_efficiency = speed * (load if load else 1) / (fuel_rate if fuel_rate else estimated_fuel_rate if estimated_fuel_rate else 1)
            read = {
                'time': time.strftime("%H:%M:%S", time.localtime()),
                'data': {
                    'Run Time': run_time,
                    'Fuel Type': fuel_type,
                    'Throttle': throttle,
                    'Air Intake': air_intake,
                    'RPM': rpm,
                    'Speed': speed,
                    'Ethanol %': ethanol if ethanol else 'N/A',
                    'Fuel Efficiency': fuel_efficiency,
                }
            }
            yield "<script> document.body.innerHTML = ''</script>"
            yield str(read)
            time.sleep(0.5)  # 0.5-second interval
    return Response(generate_data(), mimetype='text/html')

if __name__ == '__main__':
    # get port to use obd protocol
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(host='0.0.0.0')
