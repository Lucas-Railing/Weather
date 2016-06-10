import csv
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import curve_fit
import numpy as np
import math

month = input('What month is it?')
day   = input('What day is it?')
dt = datetime.datetime(2015, month, day, 0, 0)
tt = dt.timetuple()
DAY = tt.tm_yday

f = open('700576.csv')
wreader = csv.reader(f)
date = []
Tmax = []
Tmin = []
Parc = []
for x in wreader:
    date.append((x[5]))
    Tmax.append((x[41]))
    Tmin.append((x[46]))
    Parc.append((x[26]))
    
date2 = []
Tmax2 = []
Tmin2 = []
Parc2 = []
i = 1
while i < len(date):
    if abs(float(Tmax[i])) < 1000 and abs(float(Tmin[i])) < 1000 and abs(float(Parc[i])) < 1000:
        date2.append((date[i]))
        Tmax2.append((9.0/5)*(float(Tmax[i])/10.0) + 32.0)
        Tmin2.append((9.0/5)*(float(Tmin[i])/10.0) + 32.0)
        Parc2.append(float(Parc[i]))
    i = i + 1



aday = []
year = []
for x in date2:
    year.append(int(x[0:4]))
    dt = datetime.datetime(int(x[0:4]), int(x[4:6]), int(x[6:8]), 0, 0)
    tt = dt.timetuple()
    aday.append(tt.tm_yday)

nyear = []
for x in year:
    nyear.append(int(x))



#Generate a list of 366 blank lists:
x = 1
Dlist = []
dlist = []
while x < 367:
    Dlist.append([])
    dlist.append([])
    x = x + 1

x = min(nyear)
Ylist = []
ylist = []
Plist = []
while x < max(nyear) + 1:
    Ylist.append([])
    ylist.append([])
    Plist.append([])
    x = x + 1


#Append each of those lists with temperatures according to which day of the year they fall on: 
i = 0 
while i < len(Tmax2):
    k = aday[i]
    Dlist[k-1].append(Tmax2[i])
    dlist[k-1].append(Tmin2[i])
    i = i + 1

i = 0 
while i < len(Tmax2):
    k = nyear[i]
    Ylist[k-1-int(min(nyear))].append(Tmax2[i])
    ylist[k-1-int(min(nyear))].append(Tmin2[i])
    Plist[k-1-int(min(nyear))].append(Parc2[i])
    i = i + 1
i = 0 
while i < len(Tmax2):
    k = nyear[i]
    Ylist[k-1-int(min(nyear))].append(Tmax2[i])
    ylist[k-1-int(min(nyear))].append(Tmin2[i])
    i = i + 1


def avg(L):
    return sum(L)/len(L)

#Take an average of each list to find the average temperature for each day of the year:
High = []
SHigh =[]
for x in Dlist:
    H = avg(x)
    High.append(H)
    sq = avg([s*s for s in x])
    S = math.sqrt(sq - (avg(x))**2)
    SHigh.append(S)

Low = []
SLow =[]
for x in dlist:
    L = avg(x)
    sq = avg([s*s for s in x])
    S = math.sqrt(sq - (avg(x))**2)
    SLow.append(S)
    Low.append(L)

YHigh = []
SYHigh = []
for x in Ylist:
    H = avg(x)
    sq = avg([s*s for s in x])
    S = math.sqrt(sq - (avg(x))**2)
    YHigh.append(H)
    SYHigh.append(S)

YLow  = []
SYLow  = []
for x in ylist:
    L = avg(x)
    sq = avg([s*s for s in x])
    S = math.sqrt(sq - (avg(x))**2)
    SYLow.append(S)
    YLow.append(L)

AParc  = []
SAParc  = []
for x in Plist:
    L = avg(x)
    sq = avg([s*s for s in x])
    S = math.sqrt(sq - (avg(x))**2)
    SAParc.append(S)
    AParc.append(L)

#The set function gives the set of numbers in a list without repeating them. The list function converts it back to a list.
k = set(aday)
Day = list(k)
k = set(nyear)
Year = list(k)

#Begin Curve fit.
x = np.asarray(Day)
y = np.asarray(High)

def Lin(x, a, w, b, o):
    return a*np.sin(w*x + b) + o


popt, pcov = curve_fit(Lin, x, y, p0 = [35, 0.016, 30, 20])

a = popt[0]
b = popt[1]
c = popt[2]
d = popt[3]

H = a*math.sin(b*DAY + c) + d
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


x = np.asarray(Day)
y = np.asarray(Low)


popt, pcov = curve_fit(Lin, x, y, p0 = [35, 0.016, 30, 20])

a = popt[0]
b = popt[1]
c = popt[2]
d = popt[3]

L = a*math.sin(b*DAY + c) + d

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

open('Avg.txt', 'w').close()
F = open('Avg.txt', 'w')

i = 0
while i < 366:
    F.write(str(High[i]))
    F.write('  ')
    F.write(str(Low[i]))
    F.write('  ')
    F.write(str(HFit[i]))
    F.write('  ')
    F.write(str(LFit[i]))
    F.write('  ')
    F.write(str(SHigh[i]))
    F.write('  ')
    F.write(str(SLow[i]))
    F.write('  ')
    F.write('\n')
    i += 1
while i < 367:
    F.write(str(HList[0]))
    F.write('  ')
    F.write(str(HList[1]))
    F.write('  ')
    F.write(str(HList[2]))
    F.write('  ')  
    F.write(str(HList[3]))
    F.write('  ')
    F.write('\n')
    F.write(str(LList[0]))
    F.write('  ')
    F.write(str(LList[1]))
    F.write('  ')
    F.write(str(LList[2]))
    F.write('  ')  
    F.write(str(LList[3]))
    F.write('  ')
    F.write('\n')
    i += 1

F.close()

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
#fig2 = plt.figure(figsize = (15,8))
#fig2.canvas.set_window_title('Weather Washington, PA (2)')
#plt.ylabel("Temperature (degrees F)")
#plt.xlabel("Year")
#plt.title("Average Temperature vs. Year")
#L4 = plt.scatter(Year, YHigh, color = 'r', label = 'High')
#L5 = plt.scatter(Year, YLow , color = 'b', label = 'Low')
#L4 = plt.errorbar(Year, YHigh, yerr = SYHigh, color = 'r', label = 'High')
#L5 = plt.errorbar(Year, YLow , yerr = SYHigh, color = 'b', label = 'Low')
#plt.legend()
#plt.show()

#fig2 = plt.figure(figsize = (15,8))
#fig2.canvas.set_window_title('Precipitation Washington, PA (2)')
#plt.ylabel("Precipitation")
#plt.xlabel("Year")
#plt.title("Average Precipitation vs. Year")
#L4 = plt.scatter(Year, AParc, color = 'b', label = 'Precip')
#L4 = plt.errorbar(Year, SAParc, yerr = SAParc, color = 'b', label = 'Precip')
#plt.legend()
#plt.show()

