
import sys
import os
import time
import psutil
print("started program at"+str(time.time()/60))
while 1 == 1:
    cpu = psutil.cpu_percent(interval=None, percpu=False)
    net = psutil.net_io_counters(pernic=False, nowrap=True)
    mem = psutil.virtual_memory()
    print("Free memory = " + str(mem.free) + " Used memory = " + str(mem.used) + " Cpu = " + str(cpu) + " network recieved = " + str(net.bytes_recv) + " network sent = " + str(net.bytes_sent) + "/")
    time.sleep(.5)