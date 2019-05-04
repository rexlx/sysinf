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

[disks]
name                                    total   used    %
mapper/fedora_localhost--live-root      48.97   22.18   45.29
mapper/fedora_localhost--live-home      170.09  68.09   40.03
sda1                                    916.89  468.47  51.09
nvme0n1p1                               116.87  37.45   32.04
sdb                                     1832.77 472.06  25.76
```
