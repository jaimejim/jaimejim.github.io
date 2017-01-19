---
title: "Using Resilio on Raspberri Pi 3"
layout: post
date: 2017-01-20 08:00
tag:
- Resilio
- Raspberry Pi
- Back Up
- File Synchronization
- Hard Drive
- NAS
blog: true
star: true
---

As a pet project of mine, I have been using a spare Raspberry Pi 3 as a back up system for my files. I want to reduce my dependency on *cloud* services like Google Drive, Dropbox, etc and I want to have control over what I share.

After some research I rediscovered [Resilio](https://www.resilio.com) which I remembered as Bittorrent Sync. It basically is a P2P-based file storage software that runs on pretty much any OS. It allows you to back up the files of your computer on any other device you own. You can also back up your phone pictures on your computer automatically or share a large folder among friends or colleagues.

First step is getting a [Raspberry 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) (I had a spare one at the office) and perhaps an external hard drive, although an SD card might be sufficient for you. Mine came with 16GB and would have been enough.

![Sexy insides of the Raspberry 3](/assets/images/resilio_raspberry.jpg)

### Installing Raspbian on Raspberry 3

Raspberry 3 comes with a handy [New Out Of the Box Software (NOOBS)](https://www.raspberrypi.org/downloads/noobs/) which is used during boot time to install any OS.  

For our purposes I chose [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) as it is the main distro.


### Installing Resilio on Raspbian


Once we have Rasbian ready, we can install Resilio. There is a [good tutorial](add link) that I have followed except for few changes.

We need to create a folder for Resilio.
```
sudo mkdir -p /opt/resilio/bin
sudo mkdir /opt/resilio/app_files
cd /opt/resilio/bin
```
Download the latest version and unpack.
```
sudo wget  https://download-cdn.resilio.com/stable/linux-arm/resilio-sync_arm.tar.gz
sudo tar -xvf resilio-sync_arm.tar.gz
sudo rm -f resilio-sync_arm.tar.gz
```

Then we need to create a service
```
sudo nano /etc/init.d/resilio
```

You can copy the following, note that we change rslsync.conf for resilio.conf:

```
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

Set appropriate permissions for the new file and set defaults for service.

```
sudo chmod 755 /etc/init.d/resilio
sudo update-rc.d resilio defaults
```

Now we need to create the configuration file with its basic information.

```
sudo vi /opt/resilio/bin/resilio.conf
```
Yuo can find the file at http://www.klaverstyn.com.au/david/wiki/index.php?title=Installing_Resilio_Sync_(rslSync)_on_the_Raspberry_Pi#Create_Folder_for_Resilio_Sync

4. network

###On nomadiclab wifi
http://10.0.2.243:8888/

###On another wifi
ssh inside
// add passwords (same twice)
http://localhost:38888/gui/
ssh pi

5. adding external hd
https://miqu.me/blog/2015/01/14/tip-exfat-hdd-with-raspberry-pi/

sudo apt-get install exfat-fuse

apparently it used to be unstable.
try rebooting just in case

180  cd ..
181  ls
182  cd mnt/
183  ls
184  cd ..
185  cat /etc/fstab
186  sudo mount -a
187  cat /etc/fstab
188  cat dev/disk/by-id/
189  ls
190  ls dev/disk/by-id/
191  ls dev/disk/by-label/
192  fdisk -l
193  sudo fdisk -l
194  ls dev/sda
195  ls dev/sda1
196  ls dev/sda2
197  cd dev/sda2
198  ls dev/sda2
199  sudo fdisk -l
200  ls dev/disk/by-label/
201  mount
202  ls mnt/
203  sudo raspi-config
204  mount
205  dmesg
206  mount /dev/sda2 /mnt
207  sudo mount /dev/sda2 /mnt
208  sudo apt-get install exfat-fuse
209  reboot now
210  sudo reboot now
211  history


https://miqu.me/blog/2015/01/14/tip-exfat-hdd-with-raspberry-pi/

Shell
```
sudo fdisk -l
```

```
Device         Boot   Start      End  Sectors  Size Id Type
/dev/mmcblk0p1         8192  2474609  2466418  1.2G  e W95 FAT16 (LBA)
/dev/mmcblk0p2      2474610 30318591 27843982 13.3G  5 Extended
/dev/mmcblk0p5      2482176  2547709    65534   32M 83 Linux
/dev/mmcblk0p6      2547712  2682879   135168   66M  c W95 FAT32 (LBA)
/dev/mmcblk0p7      2686976 30318591 27631616 13.2G 83 Linux

Disk /dev/sda: 931.5 GiB, 1000170586112 bytes, 1953458176 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 9F4936FE-C906-43A7-AE5E-D4A5BEF6F496

Device      Start        End    Sectors   Size Type
/dev/sda1      40     409639     409600   200M EFI System
/dev/sda2  411648 1953456127 1953044480 931.3G Microsoft basic data

```

pi@raspberrypi:/ $ sudo mkdir /mnt/PIHDD
pi@raspberrypi:/ $ mnt /dev/sda1 /mnt/PIHDD
-bash: mnt: command not found
pi@raspberrypi:/ $ mount /dev/sda1 /mnt/PIHDD
mount: only root can do that
pi@raspberrypi:/ $ sudo mount /dev/sda1 /mnt/PIHDD
pi@raspberrypi:/ $ ls mnt/PIHDD/
pi@raspberrypi:/ $ ls -las mnt/PIHDD/
total 5
1 drwxr-xr-x 2 root root  512 Jan  1  1970 .
4 drwxr-xr-x 3 root root 4096 Jan 19 17:09 ..


UUID="5880-C9F4"

3. explain about temperature issues.

GUI = around 10 degrees
Syncing = 5 - 9 degrees
Tue 17 Jan 14:20:21 UTC 2017
temp=55.8'C
Tue 17 Jan 14:20:31 UTC 2017
temp=55.8'C
Tue 17 Jan 14:20:41 UTC 2017
temp=55.8'C
Tue 17 Jan 16:20:51 EET 2017
temp=58.5'C
Tue Jan 17 16:35:24 EET 2017
temp=46.2'C
Tue Jan 17 16:35:34 EET 2017
temp=46.2'C

vcgencmd measure_temp

installation of a heat dissipator


![Final setup with Bad Piggy watching](/assets/images/raspberry_setup.jpg)
