import re
#average local temperature anomaly
i = open("init/ncdc-merged-sfc-mntp.dat").readlines()
o = open("gtemp.csv", "w")
o.truncate()
l = 0
months = 0
avgsum = 0
while(l < len(i)):
	count = 0
	total = 0
	for offset in range(1, 36):
		for val in i[l+offset].split(" "):
			if(len(val) > 0 and val != "-9999"):
				total = total + float(val)/100
				count = count + 1
	m = re.search('^\W*(\d+).+([\d]{4})$', i[l])
	mavg = total/count
	o.write(m.group(2)+"-"+m.group(1)+","+str(mavg)+"\n")	
	months = months + 1
	avgsum = avgsum + mavg
	l = l + 37
avg = avgsum/months
o.flush()
#find global temperature anomaly, count hurricanes
i = open("gtemp.csv").readlines()
o = open("gtemp.csv", "w")
h = open("storms.csv").readlines()
o.truncate()
stormcount = 0
for line in i:
	date = line.split(",")[0]
	hcount = 0
	for storm in h:
		stormcount = stormcount + 1
		if(storm.split(",")[1] == date):
			hcount = hcount + 1
	if(hcount > 0):
		o.write(date+","+str(float(line.split(",")[1])-avg)+","+str(hcount)+"\n")
o.flush()
#1873/1424 = pos/neg