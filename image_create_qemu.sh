#!/bin/bash

IMGSIZE=16g

IMGPATH=./qemu-sda-image.img
MOUNTPATH=./qemu-hd

rm -rf $IMGPATH

sudo mkdir -p $MOUNTPATH

qemu-img create $IMGPATH $IMGSIZE
fdisk -l $IMGPATH
mkfs.ext4 $IMGPATH

sudo mount -o loop,rw $IMGPATH $MOUNTPATH
# sudo debootstrap bionic $MOUNTPATH
# sudo debootstrap focal $MOUNTPATH
sudo debootstrap jammy $MOUNTPATH
sudo chroot $MOUNTPATH apt-get update
sudo chroot $MOUNTPATH apt-get install -y build-essential vim wget curl git gdb
# sudo chroot $MOUNTPATH apt-get install -y cgroup-tools # cgroupfs-mount cgroup-bin cgroup-lite cgroupfs-mount libcgroup1
echo "set root password"
sudo chroot $MOUNTPATH passwd root
sudo umount $MOUNTPATH``


protect
[ 2413.826604] "4. PF addr and ip", 7f1e44696000, 401a98
protect