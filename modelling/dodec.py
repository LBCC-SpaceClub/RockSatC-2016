from visual import *
from math import cos, sin, radians

display(width=600, height=600, title='RockSat-C 2016 Dodecahedron', range=5)
dodec = frame()
faces = []

det_log_file = "sample_detector_log.txt"
imu_log_file = "sample_imu_log.txt"

# top face
faces.append(cylinder(frame=dodec, pos=(0,0,1.11803398875), axis=(0,0,1),
	radius=0.5, length=0.1, color=color.red))

for i,j in zip(range(5), range(6)):
	for k in [-2, 2]:
		POS = vector(cos(2*pi*i/5), sin(2*pi*i/5), sin(pi/(k*3)))
		faces.append(cylinder(frame=dodec, pos=POS, axis=POS, radius=0.5,
			length=0.1))
		#print (i,j,k), POS, mag(POS)

# bottom face
faces.append(cylinder(frame=dodec, pos=(0,0,-1.11803398875), axis=(0,0,-1),
	radius=0.5, length=0.1, color=color.blue))

''' Read detector log into a dictionary of time:sensors '''
det_log = {}
with open(det_log_file) as log:
	for line in log:
		# each line should look like: 1000,35,40,33,42,46,44,28,29,24,25,22,21,
		line = line.replace(',', ' ')
		time, samples = line.split(' ',1)
		time = int(time)
		samples = [int(det) for det in samples.split()[:12]]
		det_log[time] = samples

''' Read imu log into a dictionary of time:dx,dy,dz '''
with open(imu_log_file) as log:
	for line in log:
		# each line should look like: 1000,0,1,2,
		line = line.replace(',', ' ')
		time, imu = line.split(' ',1)
		time = int(time)
		imu = [float(i) for i in imu.split()]
		det_log[time].append(imu)


''' Read through the log one line at a time.
	For each line, update the face colors and, when appropriate, the payload angle
'''
for time, value in det_log.iteritems():
	rate(1000) 			 # slow down the animation to real time.
	if len(value) == 13: # only update the angle if a new angle is available
		dodec.rotate(angle=value[12][0], axis=(1,0,0)) # update x angle
		dodec.rotate(angle=value[12][1], axis=(0,1,0)) # update y angle
		dodec.rotate(angle=value[12][2], axis=(0,0,1)) # update z angle
	for i in range(12):  # Update all 12 faces
		faces[i].color = color.gray(value[i]/30.0)
	#print time, value, len(value)	# debugging

print "All done!"

'''
while 1:
	rate(10)
	dodec.rotate(angle=.05)
	# rotate in a different direction by including an axis of rotation
	dodec.rotate(angle=.05, axis=(0,1,0))
'''