from time import sleep

import serial

dev = serial.Serial('COM7')
sleep(0.5)
voltages = [i for i in range(4096) if i%10==0]
currents = []

for voltage in voltages:
    command = f'OUT:CH0:{voltage}\n'
    # command_2 = 'OUT:CH0:{}\n'.format(voltage) <- Another possibility to format strings
    dev.write(command.encode('ascii'))
    sleep(0.05)
    dev.write(b'IN:CH0\n')
    current = dev.readline()
    current = current.decode('ascii')
    current = int(current)
    currents.append(current)
    print(current)

print(currents)
