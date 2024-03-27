import obd
import time

# manually specify the serial port
connection = obd.OBD("COM3")  # replace "COM3" with your port

# select an OBD command (sensor)
cmd = obd.commands.SPEED

# get the current time
last_time = time.time()

while True:
    # get the current time
    current_time = time.time()

    # check if 200ms have passed since the last query
    if current_time - last_time >= 0.2:
        # send the command, and parse the response
        response = connection.query(cmd)

        # user-friendly unit conversions
        print(response.value.to("mph"))

        # update the last query time
        last_time = current_time
