import csv
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
        'Throttle': commands.THROTTLE_POS,
        'MAF': commands.MAF,
        'Intake Pressure': commands.INTAKE_PRESSURE,
        'Barometric Pressure': commands.BAROMETRIC_PRESSURE,
        'Intake Temperature': commands.INTAKE_TEMP,
        'RPM': commands.RPM,
        'Speed': commands.SPEED,
        'Fuel Rate': commands.FUEL_RATE,
        'Load %': commands.ENGINE_LOAD,
    }
    try:

        # Connect to the OBD-II adapter
        connection = OBD(portstr=port, baudrate=9600, fast=False, timeout=1, protocol="6")
        if connection.status() == OBDStatus.NOT_CONNECTED:
            print("Failed to connect to the OBD-II adapter")
            exit()
        if connection.status() == OBDStatus.CAR_CONNECTED:
            print("The OBD-II adapter has established a connection with the vehicle!\nEntering execution mode...")
    except:
        print("Failed to connect to the OBD-II adapter")
        exit()

    # Function to calculate MAF
    def calculate_maf(rpm, map_kpa, iat_c):
        iat_k = iat_c + 273.15
        imap = rpm * map_kpa / iat_k
        maf = imap  * 0.0000394908187
        return maf

    def generate_data():
        def run_command(connection, command):
            if connection.supports(command):
                return connection.query(command).value
            return None

        fields = [
            'Time',
            'Run Time',
            'RPM',
            'Speed',
            'Throttle',
            'Load %',
            'MAF',
            'Intake Temperature',
            'Air Intake'
        ]

        while True:
            try:
                # Get the data from the OBD-II adapter
                fuel_type = run_command(connection, pid_mapping['Fuel Type'])
                run_time = run_command(connection, pid_mapping['Run Time'])
                run_time_object = None if run_time is None else {
                    "magnitude": run_time.magnitude,
                    "unit": str(run_time.units),
                    "string": str(run_time)
                }
                throttle = run_command(connection, pid_mapping['Throttle'])
                throttle_object = None if throttle is None else {
                    "magnitude": throttle.magnitude,
                    "unit": str(throttle.units),
                    "string": str(throttle)
                }
                rpm = run_command(connection, pid_mapping['RPM'])
                rpm_object = None if rpm is None else {
                    "magnitude": rpm.magnitude,
                    "unit": str(rpm.units),
                    "string": str(rpm)
                }
                intake_temperature = run_command(connection, pid_mapping['Intake Temperature'])
                intake_temperature_object = None if intake_temperature is None else {
                    "magnitude": intake_temperature.magnitude,
                    "unit": str(intake_temperature.units),
                    "string": str(intake_temperature)
                }
                speed = run_command(connection, pid_mapping['Speed'])
                speed_object = None if speed is None else {
                    "magnitude": speed.magnitude,
                    "unit": str(speed.units),
                    "string": str(speed)
                }
                air_intake = run_command(connection, pid_mapping['Intake Pressure'])
                air_intake_object = None if air_intake is None else {
                    "magnitude": air_intake.magnitude,
                    "unit": str(air_intake.units),
                    "string": str(air_intake)
                }

                maf = calculate_maf(
                    rpm.magnitude if rpm is not None else 0,
                    air_intake.magnitude if air_intake is not None else 0,
                    intake_temperature.magnitude if intake_temperature is not None else 0
                )
                maf_object = None if maf is None else {
                    "magnitude": maf,
                    "unit": "kg/s",
                    "string": str(maf)
                }
                load = run_command(connection, pid_mapping['Load %'])

                read = {
                    'time': time.strftime("%H:%M:%S", time.localtime()),
                    'data': {
                        'Fuel Type': str(fuel_type),
                        'Run Time': run_time_object,
                        'Throttle': throttle_object,
                        'Air Intake': air_intake_object,
                        'RPM': rpm_object,
                        'Speed': speed_object,
                        'Load %': load.magnitude if load else 'N/A',
                        'MAF': maf_object,
                        'Intake Temperature': intake_temperature_object,
                    }
                }

                row = {
                    "Time": time.strftime("%H:%M:%S", time.localtime()),
                    "Run Time": run_time.magnitude if run_time is not None else 0,
                    "Throttle": throttle.magnitude if throttle is not None else 0,
                    "Air Intake": air_intake.magnitude if air_intake is not None else 0,
                    "RPM": rpm.magnitude if rpm is not None else 0,
                    "Speed": speed.magnitude if speed is not None else 0,
                    "Load %": load.magnitude if load is not None else 0,
                    "MAF": maf,
                    "Intake Temperature": intake_temperature.magnitude if intake_temperature is not None else 0,
                }

                with open('data_log.csv', 'a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fields)

                    #Write the header only once, check if the file size is 0
                    if file.tell() == 0:
                        writer.writeheader()

                    # Write the data
                    writer.writerow(row)

                yield "<script> document.body.innerHTML = ''</script>"
                yield str(read)
                time.sleep(0.25)  # 0.5-second interval
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
