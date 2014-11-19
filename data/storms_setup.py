import re
#trim uneeded vars
i = open("init/Allstorms.ibtracs_wmo.v03r06.csv").readlines()[3:]
o = open("storms.csv", "w")
o.truncate()
for line in i:
	ll = line.split(",")
	o.write(ll[0]+","+ll[5]+","+ll[6].split("-")[0]+"-"+re.sub('^0', '', ll[6].split("-")[1])+","+ll[8].strip()+","+ll[9].strip()+","+ll[10].strip()+","+ll[11].strip()+"\n")
o.flush()
#max wind speed for each storm
i = open("storms.csv").readlines()
o = open("storms.csv", "w")
o.truncate()
serial = ""
wmax = 0
sdat = ""
for line in i:
	ll = line.split(",")
	if(serial != ll[0]):
		if(wmax > 0):
			o.write(sdat+str(wmax)+"\n")
		sdat = ll[1]+","+ll[2]+","+ll[3]+","+ll[4]+","
		wmax = 0
		serial = ll[0]
	elif(float(ll[5]) > wmax):
		wmax = float(ll[5])
o.flush()
#calculate windspeed anomaly
i = open("storms.csv").readlines()
o = open("storms.csv", "w")
o.truncate()
s = 0
l = 0
for line in i:
	s = s + float(line.split(",")[-1])
	l = l + 1
avg = s/l
#print avg
for line in i:
	ll = line.split(",")
	ll[-1] = str(float(ll[-1])-avg)
	o.write(",".join(ll)+"\n")
o.flush()
# #find corresponding surface temp anomaly
i = open("storms.csv").readlines()
t = open("init/ncdc-merged-sfc-mntp.dat").readlines()
o = open("storms.csv", "w")
o.truncate()
s = 0
n = 0
for line in i:
	lat = float(line.split(",")[2])
	latoffset = int(((-1*lat)+90)/5) + 1
	lon = float(line.split(",")[3])
	lonoffset = int((lon+180)/5)*6
	year = line.split(",")[1].split("-")[0]
	month = re.sub('^0', '', line.split(",")[1].split("-")[1])
	l = 0
	while(l < len(t)):
		m = re.search('^\W*(\d+).+([\d]{4})$', t[l])
		if(m):
			if(year == m.group(2) and month == m.group(1)):
				break
		l = l + 37	
	if(l+37 < len(t)):
 		l = l + latoffset
 		val = t[l][lonoffset:lonoffset+6]
 		if(len(val) > 3 and val != " -9999"):
 			v = float(val)/100
 			o.write(line.strip()+","+str(v)+"\n")
 			s = s + v*100
 			n = n + 1
print n
print s/n
