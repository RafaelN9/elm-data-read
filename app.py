from flask import Flask, Response
from obd import OBDStatus, commands, OBD, Async
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
        'Fuel Rate': commands.FUEL_RATE,
        'Load %': commands.ENGINE_LOAD,
        'Intake Pressure': commands.INTAKE_PRESSURE,
    }
    try:

        # Connect to the OBD-II adapter
        connection = OBD(port)
        if connection.status() == OBDStatus.NOT_CONNECTED:
            print("Failed to connect to the OBD-II adapter")
            exit()
        if connection.status() == OBDStatus.CAR_CONNECTED:
            print("The OBD-II adapter has established a connection with the vehicle!\nEntering execution mode...")
            time.sleep(1)  # Wait for the vehicle to respond
    except:
        print("Failed to connect to the OBD-II adapter")
        exit()

    def generate_data():
        def run_command(connection, command):
            if connection.supports(command):
                return connection.query(command).value
            return None

        while True:
            try:
                # Get the data from the OBD-II adapter
                run_time = run_command(connection, pid_mapping['Run Time'])
                throttle = run_command(connection, pid_mapping['Throttle'])
                fuel_type = run_command(connection, pid_mapping['Fuel Type'])
                air_intake = run_command(connection, pid_mapping['MAF'])
                if not air_intake:
                    air_intake = run_command(connection, pid_mapping['Intake Pressure'])
                rpm = run_command(connection, pid_mapping['RPM'])
                speed = run_command(connection, pid_mapping['Speed'])
                ethanol = run_command(connection, pid_mapping['Ethanol %'])
                fuel_rate = run_command(connection, pid_mapping['Fuel Rate'])
                load = run_command(connection, pid_mapping['Load %'])

                # Calculate litres per hour using air intakeelse:

                estimated_fuel_rate = None
                if fuel_type == None or fuel_type == 'Gasoline':
                    grams_per_second = air_intake.magnitude * KPA_TO_GRAMS_PER_SECOND_CONSTANT * GASOLINE_AFR
                    estimated_fuel_rate = (grams_per_second * 3600) / GASOLINE_DENSITY
                elif fuel_type == 'Ethanol':
                    grams_per_second = air_intake.magnitude * KPA_TO_GRAMS_PER_SECOND_CONSTANT * ETHANOL_AFR
                    estimated_fuel_rate = (grams_per_second * 3600) / ETHANOL_DENSITY

                # Calculate fuel efficiency
                load = load.magnitude if load != None else 1
                if fuel_rate == None:
                    fuel_rate = estimated_fuel_rate if estimated_fuel_rate != None else 1
                fuel_efficiency = speed.magnitude * load / fuel_rate
                read = {
                    'time': time.strftime("%H:%M:%S", time.localtime()),
                    'data': {
                        'Run Time': {
                            "magnitude": run_time.magnitude,
                            "unit": str(run_time.units),
                            "string": str(run_time)
                        },
                        'Fuel Type': str(fuel_type),
                        'Throttle': {
                            "magnitude": throttle.magnitude,
                            "unit": str(throttle.units),
                            "string": str(throttle)
                        },
                        'Air Intake': {
                            "magnitude": air_intake.magnitude,
                            "unit": str(air_intake.units),
                            "string": str(air_intake)
                        },
                        'RPM': {
                            "magnitude": rpm.magnitude,
                            "unit": str(rpm.units),
                            "string": str(rpm)
                        },
                        'Speed': {
                            "magnitude": speed.magnitude,
                            "unit": str(speed.units),
                            "string": str(speed)
                        },
                        'Ethanol %': ethanol.magnitude if ethanol else 'N/A',
                        'Fuel Efficiency': fuel_efficiency
                    }
                }
                yield "<script> document.body.innerHTML = ''</script>"
                yield str(read)
                time.sleep(0.2)  # 0.5-second interval
            except:
                print("Error while reading data")
                return
    return Response(generate_data(), mimetype='text/html')

if __name__ == '__main__':
    # get port to use obd protocol
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(host='0.0.0.0')
