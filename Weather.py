from csv import reader
import datetime
from scipy.optimize import curve_fit
from numpy import asarray, sin, sqrt
from collections import defaultdict
from matplotlib import pyplot as plt


Today = str(datetime.date.today()).split('-')
month = int(Today[1])
day   = int(Today[2])
dt = datetime.datetime(2015, month, day, 0, 0)
tt = dt.timetuple()
DAY = tt.tm_yday

print 'Today is',Today[1],'/', Today[2],'/', Today[0], '.'

File = open('707039.csv')
wreader = reader(File)
Header = next(wreader)
i = 0
for x in Header:
    if x == 'DATE':
        D = i
    if x == 'TMAX':
        M = i
    if x == 'TMIN':
        m = i
    i += 1


date = []
Tmax = []
Tmin = []
for x in wreader:
    date.append((x[D]))
    Tmax.append((x[M]))
    Tmin.append((x[m]))


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
    dt = datetime.datetime(int(x[0:4]), int(x[4:6]), int(x[6:8]), 0, 0)
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

Low = []
SLow =[]
for x in dlist.values():
    L = avg(x)
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
print "The average high for today is", int(round(H)), 'degrees Fahrenheit.'
print "The average low for today is", int(round(L)), 'degrees Fahrenheit.'


fig = plt.figure(figsize = (11,8))
#####ADJUST THE TITLE OF THE WINDOW HERE.
fig.canvas.set_window_title('Weather Washington, PA')
L1 = plt.scatter(Day, High, color = 'g', label = 'High')
L2 = plt.scatter(Day, HFit, color = 'r', label = 'HFit')
L3 = plt.scatter(Day, Low,  color = 'y', label = 'Low')
L4 = plt.scatter(Day, LFit, color = 'b', label = 'LFit')
L5 = plt.plot([DAY, DAY], [0,100], color = 'r')
plt.legend()
plt.ylabel("Average Temperature (degrees F)")
plt.xlabel("Day of Year")
plt.title("Temperature vs. Date")
plt.show()
