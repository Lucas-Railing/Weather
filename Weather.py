from csv import reader
from datetime import datetime
from scipy.optimize import curve_fit
from numpy import asarray, sin, sqrt
from collections import defaultdict
from matplotlib import pyplot as plt

month = input('What month is it?')
day   = input('What day is it?')
dt = datetime(2015, month, day, 0, 0)
tt = dt.timetuple()
DAY = tt.tm_yday

f = open('700576.csv')
wreader = reader(f)
date = []
Tmax = []
Tmin = []
for x in wreader:
    date.append((x[5]))
    Tmax.append((x[41]))
    Tmin.append((x[46]))


#Removes 'flagged' data and converts to fahrenheit:
date2 = []
Tmax2 = []
Tmin2 = []
i = 1
while i < len(date):
    if abs(float(Tmax[i])) < 1000 and abs(float(Tmin[i])) < 1000:
        date2.append((date[i]))
        Tmax2.append((9.0/5)*(float(Tmax[i])/10.0) + 32.0)
        Tmin2.append((9.0/5)*(float(Tmin[i])/10.0) + 32.0)
    i = i + 1





#Determines day of year as a number from 1-366:
aday = []
nyear = []
for x in date2:
    nyear.append(int(x[0:4]))
    dt = datetime(int(x[0:4]), int(x[4:6]), int(x[6:8]), 0, 0)
    tt = dt.timetuple()
    aday.append(tt.tm_yday)

#Create 366 Lists:
Dlist = defaultdict(list)
dlist = defaultdict(list)

#Append each list (High-Dlist and Low-dlist) with temperatures according to which day of the year they fall on: 
i = 0 
while i < len(Tmax2):
    k = aday[i]
    Dlist[k-1].append(Tmax2[i])
    dlist[k-1].append(Tmin2[i])
    i = i + 1


def avg(L):
    return sum(L)/len(L)

#Take an average of each list to find the average temperature for each day of the year:
High = []
SHigh =[]
for x in Dlist.values(): 
    H = avg(x)
    High.append(H)
    sq = avg([s*s for s in x])
    S = sqrt(sq - (avg(x))**2)
    SHigh.append(S)

Low = []
SLow =[]
for x in dlist.values():
    L = avg(x)
    sq = avg([s*s for s in x])
    S = sqrt(sq - (avg(x))**2)
    SLow.append(S)
    Low.append(L)


#The set function gives the set of numbers in a list without repeating them. The list function converts it back to a list.
k = set(aday)
Day = list(k)


#Begin Curve fit.
x = asarray(Day)
y = asarray(High)

def Lin(x, a, w, b, o):
    return a*sin(w*x + b) + o


popt, pcov = curve_fit(Lin, x, y, p0 = [35, 0.016, 30, 20])

a = popt[0]
b = popt[1]
c = popt[2]
d = popt[3]

H = Lin(DAY, a, b, c, d)
HList = [a,b,c,d]

#End Curve fit.


print 
print "The equation for high temerature, 'T,' as a funtion of time, 't' is"
print "T =", a, "Sin(", b, "t", "+", c, ")" , "+", d
print "where temperature is in degrees Fahrenheit, and time is in days."


HFit = []
t = 0
while t < len(Day):
    F = Lin(t, a, b, c, d)
    HFit.append(F)
    t = t + 1


x = asarray(Day)
y = asarray(Low)


popt, pcov = curve_fit(Lin, x, y, p0 = [35, 0.016, 30, 20])

a = popt[0]
b = popt[1]
c = popt[2]
d = popt[3]

L = Lin(DAY, a, b, c, d)
LList = [a,b,c,d]

LFit = []
t = 0
while t < len(Day):
    F = Lin(t, a, b, c, d)
    LFit.append(F)
    t = t + 1


print 
print "The equation for low temerature, 'T,' as a funtion of time, 't' is"
print "T =", a, "Sin(", b, "t", "+", c, ")" , "+", d
print "where temperature is in degrees Fahrenheit, and time is in days."

print
print "The average high for today is", H, '.'
print "The average low for today is", L, '.'

#open('Avg.txt', 'w').close()
#F = open('Avg.txt', 'w')

#i = 0
#while i < 366:
#    F.write(str(High[i]))
#    F.write('  ')
#    F.write(str(Low[i]))
#    F.write('  ')
#    F.write(str(HFit[i]))
#    F.write('  ')
#    F.write(str(LFit[i]))
#    F.write('  ')
#    F.write(str(SHigh[i]))
#    F.write('  ')
#    F.write(str(SLow[i]))
#    F.write('  ')
#    F.write('\n')
#    i += 1
#while i < 367:
#    F.write(str(HList[0]))
#    F.write('  ')
#    F.write(str(HList[1]))
#    F.write('  ')
#    F.write(str(HList[2]))
#    F.write('  ')  
#    F.write(str(HList[3]))
#    F.write('  ')
#    F.write('\n')
#    F.write(str(LList[0]))
#    F.write('  ')
#    F.write(str(LList[1]))
#    F.write('  ')
#    F.write(str(LList[2]))
#    F.write('  ')  
#    F.write(str(LList[3]))
#    F.write('  ')
#    F.write('\n')
#    i += 1

#F.close()

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
plt.ylabel("Temperature (degrees F)")
plt.xlabel("Day")
plt.title("Temperature vs. Date")
plt.show()
