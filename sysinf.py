import multiprocessing as mp
import sys
import socket
import os

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
    # it into years, months, weeks, days,
    # hours, and seconds
    while True:
        if s < 0:
            print("thats less then zero...")
            error = 'true'
            break
        elif s >= 86400:
            s -= 86400
            day += 1
            continue
        elif s >= 3600:
            s -= 3600
            hour += 1
            continue
        elif s >= 60:
            s -= 60
            mins += 1
            continue
        elif s < 60:
            break
    converted_time = str(day) + 'd ' + str(hour) + 'h ' \
                   + str(mins) + 'm ' + str(s) + 's'
    #print(socket.gethostname().ljust(36) + ' ' + converted_time)
    return converted_time

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        for i in f:
            line = str(i).split()
            uptime = line[0]

    runtime = seconds_to_readable(uptime)
    print('Runtime'.ljust(14) + runtime)

def get_cpu():
    with open('/proc/cpuinfo') as f:
        total_cores = mp.cpu_count()
        sock_count = []
        core_count = []
        for line in f:
            if 'cal id' in line:
                sock_count.append(line)
            if 'model name' in line:
                mod = line.split()
                model = mod[3:]
                cpu_model = ' '.join(str(e) for e in model)
            if 'cpu cores' in line:
                cores = line.split()
                core_count.append(cores[3])
    sockets = set(sock_count)
    real_cores = int(core_count[-1]) * int(len(sockets))
    print('CPU Model'.ljust(14) + cpu_model)
    print('Sockets'.ljust(14) + str(len(sockets)))
    print('Real Cores'.ljust(14) + str(real_cores))
    print('Total Cores'.ljust(14) + str(total_cores))

def get_mem():
    with open('/proc/meminfo') as f:
        for line in f:
            if 'MemTotal' in line:
                total = line.split()
                mem_in_kb = total[1]
                kb_to_gb = int(mem_in_kb) / (1024 ** 2.0)
                mem_in_gb = "{0:.2f}".format(kb_to_gb)
    print('Total Memory'.ljust(14) + mem_in_kb + ' (' + str(mem_in_gb) \
          + 'gb)')

def get_net():
    hostname = socket.gethostname()
    if os.path.isfile('/usr/sbin/ip'):
        f = os.popen('/usr/sbin/ip route')
        is_linux_with_ip = True
    elif os.path.isfile('/sbin/ip'):
        f = os.popen('/sbin/ip route')
        is_linux_with_ip = True
    else:
        print("Missing 'ip' package")
        is_linux_with_ip = False
    if is_linux_with_ip:
        for line in f:
            if 'default' in line:
                data = line.split()
                gateway, dev = data[2], data[4]
    ip = socket.gethostbyname(hostname)
    print('IP'.ljust(14) + ip)
    print('Gateway'.ljust(14) + gateway)
    print('Interface'.ljust(14) + dev)
    print('Hostname'.ljust(14) + hostname)

def get_kernel():
    f = os.popen('uname -r')
    kernel = f.readline().strip()
    print('Kernel'.ljust(14) + kernel)


def get_os():
    if os.path.isfile('/etc/os-release'):
        f = open('/etc/os-release')
        for line in f:
            if "PRETTY_NAME" in line:
                osys = line.strip().split('"')
                distro = osys[1]
    print('OS'.ljust(14) + distro)

print('\n')
get_uptime()
get_cpu()
get_mem()
get_net()
get_kernel()
get_os()
