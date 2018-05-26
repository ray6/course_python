#-*- utf-8 -*-
import re
import codecs
import unicodedata
import os
from math import sqrt

RAWFILE = "2015taiwan.txt"
PMFILE = "data.txt"

data = {}  #{location:[data list each day]}
locations = []

def get_PM25():
	pattern = r"PM2.5"
	raw_data = open(RAWFILE, "r")
	PM = open(PMFILE, "w")

	f = raw_data.readlines()
	for i in range(len(f)):
		get = re.findall(pattern, f[i])
		if get:
			PM.write(f[i])
	raw_data.close()
	PM.close()

def IsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def GetDataFromFile():
	#read PM file
	loss = ['','','','','','','','','','','','','','','','','','','','','','','','']
	cnt = 0
	with codecs.open(PMFILE, "r", encoding="utf-8") as PM:
		for line in PM:
			rawlist = line.split(',')
			local = rawlist.pop(1)
			if not data.has_key(local):
				data.update({local:[]})
				locations.append(local)
				cnt = 1

			date = rawlist.pop(0)
			for i in range(countDate(date)-cnt):
				data[local].append((DaytoDate(cnt),loss))
				cnt += 1
			rawlist.pop(0)
			data[local].append((date, rawlist))
			cnt +=1
	PM.close()
	os.remove(PMFILE)

def ListToString(a):
	s = ""
	for i in a:
		s += ","+str(i)
	return s

def GeneratePM25File():
	g = codecs.open("PM25.txt", "wb", encoding="utf-8")
	for local in locations:
		for i in range(len(data[local])):
			s = ListToString(data[local][i][1])
			g.write(data[local][i][0]+","+local+",PM2.5"+s+"\n")
	g.close()

def countDate(s):
	s = s.split("/")
	mon = int(s[1])
	date = int(s[2])
	year = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151,
			7:181, 8:212, 9:243, 10:273, 11:304, 12:334}
	day = year[mon]+date
	return day
def DaytoDate(a):
	year = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151,
			7:181, 8:212, 9:243, 10:273, 11:304, 12:334}
	for key, value in year.items():
		if key != 12:
			if value < a <= year[key+1]:
				date = "2015/"+str(key)+"/"+str(a-value)
				break
		else:
			date = "2015/"+str(key)+"/"+str(a-value)
			break
	return date


def Dist(x, y):
	dist = 0.0
	for i in range(24):
		dist += (x[i]-y[i])*(x[i]-y[i])
	dist = sqrt(dist)
	return dist

def Sim(x,y):
	tmp = 0.0
	tmpx = 0.0
	tmpy = 0.0
	for i in range(24):
		tmp += x[i]*y[i]
		tmpx += x[i]*x[i]
		tmpy += y[i]*y[i]
	try:
		tmp = tmp/(sqrt(tmpx)*sqrt(tmpy))
	except:
		return 1.0
	return tmp

def FoundNeighbor(local, day, k):
	dist = []
	sim = []
	for i in range(k):
		dist.append((1000,'',1))
		sim.append((0.0,0,1))
	day -= 1
	for lo in locations:
		if local != lo:
			for a in range(len(data[local])):
				d = Dist(data[local][a][1], data[lo][a][1])
				s = Sim(data[local][a][1], data[lo][a][1])
				if dist[k-1][0] > d:
					dist.pop()
					dist.append((d, a, lo))
					dist.sort()
				if sim[k-1][0] > s:
					sim.pop()
					sim.append((s, a, lo))
					sim.sort()

	print('distance:')
	for i in range(k):
		da = DaytoDate(int(dist[i][1]))
		lo = dist[i][2]
		print(da),
		print(lo)
	print('Similarity:')
	for i in range(k):
		da = DaytoDate(int(sim[i][1]))
		lo = sim[i][2]
		print(da),
		print(lo)



if __name__ == "__main__":

	get_PM25()
	GetDataFromFile()

	for local in locations:
		for i in range(24):
			cnt = 0
			tmp = 0.0
			avg = 0.0
			illegal = []
			for d in range(len(data[local])):
				if IsInt(data[local][d][1][i]):
					cnt += 1
					data[local][d][1][i] = int(data[local][d][1][i])
					tmp += data[local][d][1][i]
				else:
					illegal.append(d)

			avg = round(tmp/cnt, 2)
			for a in illegal:
				data[local][a][1][i] = avg

	GeneratePM25File()
	print("Finish generate PM2.5 File.")

	while True:
		locate = raw_input('locate(type 0 to exit):')
		if locate == '0':
			break
		date = raw_input('year/month/day:')
		k = raw_input('Find ? neighbor:')
		locate = locate.decode('utf-8')
		day = countDate(date)

		FoundNeighbor(locate, day, int(k))

