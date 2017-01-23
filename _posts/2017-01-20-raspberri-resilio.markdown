---
title: "Running Resilio on a Raspberry Pi 3"
layout: post
date: 2017-01-20 08:00
tag:
- Resilio
- Raspberry Pi
- File Synchronization
- P2P
- NAS
blog: true
star: true
---

As a pet project of mine, I have been using a spare Raspberry Pi 3 as a back up system for my files. I want to reduce my dependency on *cloud* services like Google Drive, Dropbox, etc and I want to have control over what I share.

After some research I rediscovered [Resilio](https://www.resilio.com) which I remembered as Bittorrent Sync. It basically is a P2P-based file storage software that runs on pretty much any OS. It allows you to back up the files of your computer on any other device you own. You can also [back up your phone pictures](https://itunes.apple.com/us/app/resilio-sync-file-transfer/id1126282325?mt=8) on your computer automatically or share a large folder among friends or colleagues. If you have a NAS, you can also back it up there and sync the files between your computer and NAS. Finally, it also has the option of encrypting the folders that you are sharing, which is handy in the corporate environment.

![Sexy insides of the Raspberry 3](/assets/images/resilio_raspberry.jpg)

### Installing Raspbian on Raspberry 3

First step is getting a [Raspberry 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) (I had a spare one at the office) and perhaps an external hard drive, although an SD card might be sufficient for you. Mine came with 16GB and would have been enough.

Raspberry 3 comes with a handy New Out Of the Box Software [NOOBS](https://www.raspberrypi.org/downloads/noobs/) which, despite the name, even more experience users use to install Raspberry's OS.

This time I chose [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) as it is the default distro and possibly has more support.


### Installing Resilio on Raspbian


Once we have Raspbian ready, we can install Resilio. There is a good tutorial at [Klavo Wiki](https://goo.gl/ft8GzF) that you can follow to the letter except for a few nits, for that reason, I add the full installation below as well.

We need to create a folder for Resilio.

```sh
raspi:~$  sudo mkdir -p /opt/resilio/bin
raspi:~$  sudo mkdir /opt/resilio/app_files
raspi:~$  cd /opt/resilio/bin
```

Then we can download the official latest version and unpack it.

```sh
raspi:~$  sudo wget  https://download-cdn.resilio.com/stable/linux-arm/resilio-sync_arm.tar.gz
raspi:~$  sudo tar -xvf resilio-sync_arm.tar.gz
raspi:~$  sudo rm -f resilio-sync_arm.tar.gz
```

Then we need to create a service for it.

```sh
raspi:~$  sudo nano /etc/init.d/resilio
```

You can copy the following config file, note that we change rslsync.conf for resilio.conf:

```sh
#! /bin/sh
# /etc/init.d/resilio
#

# Carry out specific functions when asked to by the system
case "$1" in
start)
    /opt/resilio/bin/resilio --config /opt/resilio/bin/resilio.conf
    ;;
stop)
    killall resilio
    ;;
*)
    echo "Usage: /etc/init.d/resilio {start|stop}"
    exit 1
    ;;
esac

exit 0

```

We can then set the appropriate permissions for the new file and set defaults for service.

```sh
raspi:~$  sudo chmod 755 /etc/init.d/resilio
raspi:~$  sudo update-rc.d resilio defaults
```

Now we need to create the configuration file with its basic information.

```sh
raspi:~$  sudo nano /opt/resilio/bin/resilio.conf
```
You can find the config file at the [aforementioned wiki](https://goo.gl/ft8GzF).

After this you can reboot the Raspberry with `sudo reboot now`. After reboot you should be able to access Resilio's GUI at `0.0.0.0:8888` and it'd look like below.

![Resilio Web Gui](/assets/images/resilio_gui.png)

Now is it a good time to verify that you have networking, NATing and firewalls properly configured in your network.

```sh
raspi:~$  netstat -na | grep 8888
tcp        0      0 0.0.0.0:8888            0.0.0.0:*               LISTEN    
```

You can also enable SSH to the Raspberry for remote access.

```sh
raspi:~$  sudo raspi-config
```

### Mounting an External USB Hard Drive for Resilio Storage

This point is optional, since now we already have Resilio properly running on our board. It is only needed if you are planning to back up music or other larger files.

First you'd need to format the drive into the ExFAT format. I chose ExFAT because I have Windows, Linux, Android and MacOS and ExFAT seems to me like the only native option on all of them (apart from the outdated FAT32).  

Then we will need to install the drivers for the filesystem

```sh
raspi:~$  sudo apt-get install exfat-fuse
```

We can then reboot and check which are the available drives:

```sh
raspi:~$  sudo fdisk -l
```

You will most likely find the drive in the `/dev/sda2` partition, being `/dev/sda1` used for the partition table as below:

```
Disk /dev/sda: 931.5 GiB, 1000170586112 bytes, 1953458176 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 9F4936FE-C906-DISK-DISK-D4A5BEF6F496

Device      Start        End    Sectors   Size Type
/dev/sda1      40     409639     409600   200M EFI System
/dev/sda2  411648 1953456127 1953044480 931.3G Microsoft basic data
```


You could test if it mounts with `mount /dev/sda2 /mnt` and `dmesg` to see the mounting process.

Assuming everything works OK and you can mount your device you probably want to mount it automatically every time it boots. I found a good reference at [miqu blog](https://miqu.me/blog/2015/01/14/tip-exfat-hdd-with-raspberry-pi/) for exactly that purpose. I copy it below for the sake of brevity.

First run sudo `blkid` , it will return a list of devices and their UUIDs. Note the one for your partition:

Now you can use `sudo nano /ect/fstab` to add your partition to automount. Assuming you are mounting *MYUUID* on *MYHD* I used the same defaults as the article suggests:

```
UUID=MYUUID /mnt/MYHD exfat defaults,auto,umask=000,users,rw 0 0
```

Now every time the Pi starts it knows how to mount your drive.

### Possible Heating Issues.

The Raspberry will tend to overheat during syncing, and that's normal. However it shouldn't excess 75°C or performance will suffer. I believe at 85°C the Raspberry will shutdown to prevent damage.

It is then important to have good ventilation on your board and it wouldn't hurt to stick a heat dissipator on top, like the one I show on the first picture.

Another thing you can do is disable the GUI with `sudo raspi-config`. With that the temperature should drop already by 10 degrees pretty fast.

To be sure of the current temperature run

```sh
raspi:~$  vcgencmd measure_temp
temp=54.8C
```

Once all is ready and running, you have yourself an excellent back up and file sharing system.  Here is the final Set Up with Bad Piggy included.

![Final setup with Bad Piggy watching](/assets/images/raspberry_setup.jpg)

###**Update (23-01-2017):** Connectivity Issues

I have been noticing intermittent connectivity problems over wifi. I have not managed to debug whether it is a problem with the Raspberry, the router or something else.

Using the Ethernet port simultaneously, thus having two different IP addresses on two interfaces, seems to palliate the problem. Resilio will be accessible through the Ethernet interface. There is a relatively larger percentage of dropped packets over wifi. Still have to figure out why.

```
eth0      Link encap:Ethernet  HWaddr <XXX>  
          inet addr:<XXX>.221  Bcast:10.0.3.255  Mask:255.255.252.0
          RX packets:693059 errors:0 dropped:2 overruns:0 frame:0
          TX packets:349176 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:978393262 (933.0 MiB)  TX bytes:31174959 (29.7 MiB)

wlan0     Link encap:Ethernet  HWaddr b8:27:eb:65:20:61  
          inet addr:<XXX>.222  Bcast:<XXX>.255  Mask:255.255.252.0
          RX packets:207383 errors:0 dropped:3062 overruns:0 frame:0
          TX packets:62074 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:253370999 (241.6 MiB)  TX bytes:8083493 (7.7 MiB)
```
