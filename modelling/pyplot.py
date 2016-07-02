from matplotlib import pyplot as plt
import numpy as np
#from matplotlib import style
#style.use('ggplot')

# log_file = "../logs/dlog_2016-06-17_19:50.txt"
log_file = "../logs/short_sensors_final.txt"
# colorList = list('rgbcmyk')+['#7FFF00','#D2691E','#FF8C00','#FF1493','#FF00FF']

''' Create a dictionary of time:sensors values from the log file. '''
print "Parsing log file..."
time, sensors = [], [ [] for x in range(12)]

with open(log_file) as log:
	for line in log:
		# Watch out for the end of the log
		if len(line) < 15:
			break;
		# normal lines formatted as:
		#time,sensor 1,2,3,4,5,6,7,8,9,10,11,12
		#Example: 32,680,970,0,884,138,946,1,2,4,1,1,2,
		line = [int(x) for x in line.split(',')[:13]]
		t, line = line[0], line[1:]
		time.append(t)
		for i in range(12):
			sensors[i].append(line[i])

# Combine opposite sensors to group data and highlight trends.
# Multiply by 5/1023 to convert from ADC reading back to voltage.
pair1_12 = [ ((sensors[0][i]+sensors[11][i])/2.0)*(5.0/1023) for i in range(len(time))]
pair2_11 = [ ((sensors[1][i]+sensors[10][i])/2.0)*(5.0/1023) for i in range(len(time))]
pair3_10 = [ ((sensors[2][i]+sensors[9][i])/2.0)*(5.0/1023) for i in range(len(time))]
pair4_9  = [ ((sensors[3][i]+sensors[8][i])/2.0)*(5.0/1023) for i in range(len(time))]
pair5_8  = [ ((sensors[4][i]+sensors[7][i])/2.0)*(5.0/1023) for i in range(len(time))]
pair6_7  = [ ((sensors[5][i]+sensors[6][i])/2.0)*(5.0/1023) for i in range(len(time))]
print "Parse complete."

plt.scatter(time, pair1_12, color='r', alpha=0.005 )
plt.scatter(time, pair2_11, color='k', alpha=0.005 )
plt.scatter(time, pair3_10, color='y', alpha=0.005 )
plt.scatter(time, pair4_9, color='g', alpha=0.005 )
plt.scatter(time, pair5_8, color='b', alpha=0.005 )
plt.scatter(time, pair6_7, color='c', alpha=0.005 )

plt.xlabel('Time (microseconds)')
plt.ylabel('Voltage (V)')
plt.show()