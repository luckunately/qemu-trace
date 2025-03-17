#!/bin/bash

IMGSIZE=100g

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
sudo chroot $MOUNTPATH apt-get install -y build-essential vim wget curl git gdb time
# sudo chroot $MOUNTPATH apt-get install -y cgroup-tools # cgroupfs-mount cgroup-bin cgroup-lite cgroupfs-mount libcgroup1
echo "setup the server name to be qemu"
echo "qemu" | sudo tee $MOUNTPATH/etc/hostname
echo "set root password, you will login with root user"
sudo chroot $MOUNTPATH passwd root
sudo umount $MOUNTPATH``
