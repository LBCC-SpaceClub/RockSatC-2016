import serial
ser = serial.Serial('/dev/ttyUSB0', 2000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
while True:
  data_raw = ser.readline()
  print(data_raw)