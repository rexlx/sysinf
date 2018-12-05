from __future__ import print_function
import multiprocessing as mp
import os, platform, sys, socket

def get_args():
    """
    gets arguments
    """
    # if user adds -v arg
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v':
            # they want the model. needs root priv
            verbose = True
        return verbose 
    else:
        verbose = False
        return verbose

def get_dist():
    # this will not work on windows, assume linux
    dist = platform.platform()
    #x = ' '.join(e for e in dist)
    print("Distribution".ljust(14) + dist)

def get_model():
    """
    this gets the model of the machine, requires superuser
    permissions. it is not on by default, and is invoked
    with the the -v option
    """
    try:
        # this leverages dmidecode command
        mdl = os.popen('dmidecode | grep "Product Name"')
        model = mdl.readline().split(': ')
        product = model[1]
        #return product
        print('Model'.ljust(14) + product, end='')
    # exception should be premission denied, it is
    # possible perhaps ddmidecode command isnt
    # installed as well.
    except Exception as e:
        print("couldn't get_model(), you need higher permissions\n")

def seconds_to_readable(seconds):
    """
    this function converts seconds to human readable times
    im sure theres a better way, but it works.
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
        # if the value
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
    return converted_time

def get_uptime():
    """
    this function opens the uptime file and, using the
    seconds_to_readable() function, converts it to
    something more readable
    """
    with open('/proc/uptime', 'r') as f:
        for i in f:
            line = str(i).split()
            uptime = line[0]
    # converted here
    runtime = seconds_to_readable(uptime)
    print('Runtime'.ljust(14) + runtime)

def get_cpu():
    """
    this function opens the cpuinfo file and gets some
    info about the cpu :)
    """
    with open('/proc/cpuinfo') as f:
        # count the cpu cores with multiprocessing module
        # includes hyperthreaded cores
        total_cores = mp.cpu_count()
        # make some empty lists for later
        sock_count = []
        core_count = []
        for line in f:
            # matches physical id
            if 'cal id' in line:
                sock_count.append(line)
            # this will get the cpu name
            if 'model name' in line:
                mod = line.split()
                model = mod[3:]
                cpu_model = ' '.join(str(e) for e in model)
            # only counts real cores, not hyper threaded ones
            if 'cpu cores' in line:
                cores = line.split()
                core_count.append(cores[3])
    # convert to set to remove duplicates
    sockets = set(sock_count)
    # the amount of total real cores is the real core count
    # multiplied by the amount of sockets (cpus) on board
    real_cores = int(core_count[-1]) * int(len(sockets))
    print('CPU Model'.ljust(14) + cpu_model)
    print('Sockets'.ljust(14) + str(len(sockets)))
    print('Real Cores'.ljust(14) + str(real_cores))
    print('Total Cores'.ljust(14) + str(total_cores))

def get_mem():
    """
    opens meminfo, gets meminfo
    """
    with open('/proc/meminfo') as f:
        for line in f:
            # gets total memory
            if 'MemTotal' in line:
                total = line.split()
                mem_in_kb = total[1]
                # convert to GiB
                kb_to_gb = int(mem_in_kb) / (1024 ** 2.0)
                # we dont need many decimals, two will do
                mem_in_gb = "{0:.2f}".format(kb_to_gb)
    print('Total Memory'.ljust(14) + mem_in_kb + ' (' + str(mem_in_gb) \
          + 'gb)')

def get_net():
    """
    get details about network state
    """
    # get the hostname via socket module
    hostname = socket.gethostname()
    # ip command can be in different places, test for this
    if os.path.isfile('/usr/sbin/ip'):
        # run ip route, gives us good data
        f = os.popen('/usr/sbin/ip route')
        is_linux_with_ip = True
    elif os.path.isfile('/sbin/ip'):
        f = os.popen('/sbin/ip route')
        is_linux_with_ip = True
    else:
        # if no ip, its time to update your server
        print("Missing 'ip' package")
        is_linux_with_ip = False
    if is_linux_with_ip:
        for line in f:
            if 'default' in line:
                data = line.split()
                # get default gateway and interface
                gateway, dev = data[2], data[4]
    # get ip as socket sees it
    ip = socket.gethostbyname(hostname)
    print('IP'.ljust(14) + ip)
    print('Gateway'.ljust(14) + gateway)
    print('Interface'.ljust(14) + dev)
    print('Hostname'.ljust(14) + hostname)

# deprecated since platform deprecated the distro feature
# will keep for now
def get_kernel():
    """
    get the kernel via uname cmd
    """
    f = os.popen('uname -r')
    kernel = f.readline()
    print('Kernel'.ljust(14) + kernel)

def main():
    """
    this is it, what we've all been waiting for
    """
    print('\n')
    # determine verbisity level from get_args
    verbose = get_args()
    if verbose:
        get_model()
    # leaving this commented in case someone
    # wants it on by defualt
    #get_model()
    get_dist()
    get_uptime()
    get_cpu()
    get_mem()
    get_net()
    #get_kernel()

if __name__ == '__main__':
    main()
