from __future__ import print_function
import multiprocessing as mp
import sys
import socket
import os

"""
EXAMPLE OUTPUT:

Model         K56CA
Runtime       0d 1h 5m 42s
CPU Model     Intel(R) Core(TM) i5-3317U CPU @ 1.70GHz
Sockets       1
Real Cores    2
Total Cores   4
Total Memory  8050780 (7.68gb)
IP            10.0.0.41
Gateway       10.0.0.1
Interface     wlp2s0
Hostname      rxlx
Kernel        4.15.9-200.fc26.x86_64
"""

def get_model():
    mdl = os.popen('sudo dmidecode | grep "Product Name"')
    model = mdl.readline().split(': ')
    product = model[1]
    #return product
    print('Model'.ljust(14) + product, end='')

def seconds_to_readable(seconds):
    """
    A python program that converts seconds to
    human readable times
    """
    #Copies the number
    s = int(float(seconds))

    #Sets default values
    day = 0
    hour = 0
    mins = 0

    # this loop tests the input and breaks
    # it into days, hours, and seconds
    while s >= 0:
        # if the value is negative
        if s < 0:
            # inform user of error
            print("thats less then zero...")
            error = 'true'
            break
        # if the value is greater or equal to a day in seconds
        elif s >= 86400:
            # subtract a day from the value and increase the day count by one
            s -= 86400
            day += 1
            # repeat from the top
            continue
        # if the value is greater or equal to an hour in seconds
        elif s >= 3600:
            # subtract an hour from the value and increase the hour count by one
            s -= 3600
            hour += 1
            continue
        # subtracts minutes and increases the minute counter
        elif s >= 60:
            s -= 60
            mins += 1
            continue
        # otherwise, the value had been reduced to its final form
        elif s < 60:
            #stop evaluating the value now
            break
    # join the the counters from above and return them
    converted_time = str(day) + 'd ' + str(hour) + 'h ' \
                   + str(mins) + 'm ' + str(s) + 's'
    return converted_time

def get_uptime():
    # open (and close) the uptime file
    with open('/proc/uptime', 'r') as f:
        for i in f:
            # splits the line for just the runtime
            line = str(i).split()
            uptime = line[0]
    # converts that data into human readable times
    runtime = seconds_to_readable(uptime)
    print('Runtime'.ljust(14) + runtime)

def get_cpu():
    # open and close the cpu file
    with open('/proc/cpuinfo') as f:
        #using the multiprocessing module, count cores
        total_cores = mp.cpu_count()
        # empty lists to append later
        sock_count = []
        core_count = []
        # for each line in the cpu file
        for line in f:
            # if (physical id) is in the line
            if 'cal id' in line:
                # append the socket list
                sock_count.append(line)
            if 'model name' in line:
                # split the line for the stuff we need
                mod = line.split()
                model = mod[3:]
                # join into a single string
                cpu_model = ' '.join(str(e) for e in model)
            if 'cpu cores' in line:
                cores = line.split()
                core_count.append(cores[3])
    # convert this list into a set to leave only unique values
    sockets = set(sock_count)
    # use the last value in the list and multiply it
    # by the amount of sockets giving you the total real cpus
    real_cores = int(core_count[-1]) * int(len(sockets))
    print('CPU Model'.ljust(14) + cpu_model)
    print('Sockets'.ljust(14) + str(len(sockets)))
    print('Real Cores'.ljust(14) + str(real_cores))
    print('Total Cores'.ljust(14) + str(total_cores))

def get_mem():
    # open and close meminfo (meminfo values print as kB but are KB
    # aka KiB
    with open('/proc/meminfo') as f:
        for line in f:
            if 'MemTotal' in line:
                total = line.split()
                mem_in_kb = total[1]
                # convert KB to GB
                kb_to_gb = int(mem_in_kb) / (1024 ** 2.0)
                # get rid of some zeroes
                mem_in_gb = "{0:.2f}".format(kb_to_gb)
    # dazzle
    print('Total Memory'.ljust(14) + mem_in_kb + ' (' + str(mem_in_gb) \
          + 'gb)')

def get_net():
    # get hostname
    hostname = socket.gethostname()
    # this tests where ip is, since CentOS versions cant agree :)
    if os.path.isfile('/usr/sbin/ip'):
        f = os.popen('/usr/sbin/ip route')
        is_linux_with_ip = True
    elif os.path.isfile('/sbin/ip'):
        f = os.popen('/sbin/ip route')
        is_linux_with_ip = True
    else:
        # otherwise the ip command is not installed
        print("Missing 'ip' package")
        is_linux_with_ip = False
    if is_linux_with_ip:
        for line in f:
            #get basic net info
            if 'default' in line:
                data = line.split()
                gateway, dev = data[2], data[4]
    # get ip address
    ip = socket.gethostbyname(hostname)
    print('IP'.ljust(14) + ip)
    print('Gateway'.ljust(14) + gateway)
    print('Interface'.ljust(14) + dev)
    print('Hostname'.ljust(14) + hostname)

def get_kernel():
    f = os.popen('uname -r')
    kernel = f.readline()
    print('Kernel'.ljust(14) + kernel)

print('\n')
get_model()
get_uptime()
get_cpu()
get_mem()
get_net()
get_kernel()
