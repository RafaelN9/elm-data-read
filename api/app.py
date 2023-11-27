from flask import Flask, Response
import obd
from obd import OBD, OBDStatus, Unit, commands
import time, sys

obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

app = Flask(__name__)
port = "/dev/pts/1"

# Stream the data using Flask
@app.route('/stream')
def stream_data():

    pid_mapping = {
        'Run Time': commands.RUN_TIME,
        'Fuel Type': commands.FUEL_TYPE,
        'Fuel Pressure': commands.FUEL_PRESSURE,
        'Throttle': commands.THROTTLE_POS,
        'MAF': commands.MAF,
        'RPM': commands.RPM,
        'Speed': commands.SPEED,
        'Ethanol %': commands.ETHANOL_PERCENT,
        'Fuel Rate': commands.FUEL_RATE,
        'Load %': commands.ENGINE_LOAD,
        'Intake Pressure': commands.INTAKE_PRESSURE,
        'Fuel Trim': [
            commands.SHORT_FUEL_TRIM_1,
            commands.SHORT_FUEL_TRIM_2,
            commands.SHORT_O2_TRIM_B1,
            commands.SHORT_O2_TRIM_B2,
        ]
    }
    try:

        # Connect to the OBD-II adapter
        connection = OBD(portstr=port, baudrate=9600, fast=False, timeout=1)
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
                fuel_pressure = run_command(connection, pid_mapping['Fuel Pressure'])

                fuel_efficiency = speed.magnitude * 1.040 / fuel_pressure.magnitude
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
            except Exception as e:
                print(e)
                print("Error while reading data")
                return
    return Response(generate_data(), mimetype='text/html')

if __name__ == '__main__':
    # get port to use obd protocol
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(host='0.0.0.0')
