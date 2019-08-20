# sysinf
python system tool for linux. Displays information about the system.

```
python sysinf.py
```

or create an alias in your .bashrc

```
sysinf () {
  /usr/bin/python3.7 $scripts/sysinf.py
}

get-sysinf () {
  ssh $@ 'python' < $scripts/sysinf.py
}

# after reloading bash with . .bashrc
$ sysinf
$ get-sysinf remote_machine  # works best if you trade keys :)
```

to get the model of the machine:
```
python sysinf.py -v
```
you'll need **root** access or modified user
permissions to use this feature

# example output

```
--------------------------------------surx--------------------------------------

[system]
Distribution    Linux-5.0.10-200.fc29.x86_64-x86_64-with-fedora-29-Twenty_Nine
Runtime         17:37:34

[cpu]
CPU Model       Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz
Sockets         1
Real Cores      4
Total Cores     4

[memory]
Total Memory    16363660 (15.61gb)

[network]
Gateway         192.168.1.254 (via eno1)
eno1            192.168.1.68
virbr0          192.168.122.1
docker0         172.17.0.1

[partitions]
name            total   used    %
/               48.97   22.95   46.87
/home           170.09  64.06   37.66
/storage        116.87  69.79   59.72
/Bstor          916.89  503.06  54.87
/Mstor          1832.77 509.85  27.82                                    1832.77 472.06  25.76
```
