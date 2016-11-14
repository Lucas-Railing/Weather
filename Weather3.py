import matplotlib.pyplot as plt
import math
import datetime


month = input('What month is it?')
day   = input('What day is it?')
dt = datetime.datetime(2015, month, day, 0, 0)
tt = dt.timetuple()
DAY = tt.tm_yday

f = open('Avg.txt')

i = 0
High = []
Low = []
HFit = []
LFit = []
SHigh = []
SLow = []
YHigh = []
YLow = []
while i < 366:
    rlist = f.readline().split()
    High.append(float(rlist[0]))
    Low.append(float(rlist[1]))
    HFit.append(float(rlist[2]))
    LFit.append(float(rlist[3]))
    SHigh.append(float(rlist[4]))
    SLow.append(float(rlist[5]))
    i += 1
while i < 367:
    rlist = f.readline().split()
    popt1 = [float(x) for x in rlist]
    i += 1
while i < 368:
    rlist = f.readline().split()
    popt2 = [float(x) for x in rlist]
    i += 1
f.close()

a = popt1[0]
b = popt1[1]
c = popt1[2]
d = popt1[3]

H = a*math.sin(b*DAY + c) + d

print 
print "The equation for high temerature, 'T,' as a funtion of time, 't' is"
print "T =", a, "Sin(", b, "t", "+", c, ")" , "+", d
print "where temperature is in degrees Fahrenheit, and time is in days."

a = popt2[0]
b = popt2[1]
c = popt2[2]
d = popt2[3]

L = a*math.sin(b*DAY + c) + d

print 
print "The equation for low temerature, 'T,' as a funtion of time, 't' is"
print "T =", a, "Sin(", b, "t", "+", c, ")" , "+", d
print "where temperature is in degrees Fahrenheit, and time is in days."

print 
print "The average high for today is", H, '.'
print "The average low for today is", L, '.'



Day = range(0,366)

fig = plt.figure(figsize = (15,8))
fig.canvas.set_window_title('Weather Washington, PA')
plt.subplot(1,2,1)
L1 = plt.scatter(Day, High, color = 'g', label = 'High')
L2 = plt.scatter(Day, HFit, color = 'r', label = 'HFit')
L3 = plt.scatter(Day, Low,  color = 'y', label = 'Low')
L4 = plt.scatter(Day, LFit, color = 'b', label = 'LFit')
plt.legend()
plt.ylabel("Average Temperature (degrees F)")
plt.xlabel("Day of Year")
plt.title("Temperature vs. Date")
plt.subplot(1,2,2)
L1 = plt.scatter(Day, HFit, color = 'r', label = 'HFit')
L2 = plt.errorbar(Day, High, yerr = SHigh, color = 'g', label = 'High')
L3 = plt.scatter(Day, LFit,  color = 'b', label = 'LFit')
L4 = plt.errorbar(Day, Low, yerr = SLow,  color = 'y', label = 'Low')
plt.legend()
plt.ylabel("Average Temperature (degrees F)")
plt.xlabel("Day of Year")
plt.title("Temperature vs. Date")
plt.show()

