# IPython log file

format = '%Y-%m-%d %H:%M:%S'
dt = np.dtype([('id',np.str_,8), ('val',np.float),('time',np.str_,19)])
data = np.genfromtxt('data.lst', delimiter = '|', dtype=dt, converters={2:strpdate2num(format)})
get_ipython().system(u'ls -F --color ')
get_ipython().magic(u'cd python')
get_ipython().system(u'ls -F --color ')
data = np.genfromtxt('data.lst', delimiter = '|', dtype=dt, converters={2:strpdate2num(format)})
data[-1]
t1 = data[np.where(data['id']=='thermo1')]
t1_times = t1['time']
t1_vals = t1['val']
len(t1)
plt.plot(t1_times,t1_vals, '.')
t2 = data[np.where(data['id']=='thermo2')]
t2_vals = t2['val']
t2_times = t2['time']
plt.plot(t2_times,t2_vals, '.')
t3 = data[np.where(data['id']=='thermo3')]
t3_vals = t3['val']
t3_times = t3['time']
plt.plot(t3_times,t3_vals, '.')
lux = data[np.where(data['id']=='lux')]
lux_times = lux['time']
li = interp(lux_vals,[0,1023],[0,20])
lux_vals = lux['val']
li = interp(lux_vals,[0,1023],[0,20])
plt.plot(lux_times,li, '.')
len(data)
d
d = data[0]
d
date = d['time']
date
dateSecs = date
date = datetime.datetime(dateSecs)
dateSecs.strip()
dateSecs
dateSecs.strpdate2num(format)
gca()
ax
ax = gca()
ax.xaxis.get_major_formatter()
ax.xaxis.get_major_ticks()
ax.xaxis.get_major_locator()
ax.xaxis.units()
ax.xaxis.set_major_formatter(DateFormatter(%H))
ax.xaxis.set_major_formatter(DateFormatter('%H'))
draw()
get_ipython().magic(u'')
get_ipython().magic(u'h')
get_ipython().magic(u'help')
help
help()
get_ipython().system(u'ls -F --color ')
ipython help
get_ipython().magic(u'save')
get_ipython().magic(u'logstart')
get_ipython().system(u'ls -F --color ')
get_ipython().magic(u'hist')
exit()
