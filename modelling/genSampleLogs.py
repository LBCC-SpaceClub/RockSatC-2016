import random

det_log_name = "sample_detector_log.txt"
imu_log_name = "sample_imu_log.txt"

with open(det_log_name, 'w') as log:
	for time in range(1000,20000):
		line = str(time)+','
		for d in random.sample(xrange(20,50),12):
			line += str(d)+','
		log.write(line+'\n')

with open(imu_log_name, 'w') as log:
	for time in range(1000,20000,20):
		line = str(time)+','
		for d in [random.uniform(0.2,0.5) for i in range(3)]:
			line += str(d/100.0)+','
		log.write(line+'\n')