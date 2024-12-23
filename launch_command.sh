#!/bin/bash

sudo qemu-system-x86_64 \
  -kernel ../linux-5.16.9/arch/x86_64/boot/bzImage \
  -nographic \
  -drive file=qemu-sda-image.img,media=disk,format=raw \
  -append "console=ttyS0 nokaslr root=/dev/sda rw" \
  -m 32G \
  --enable-kvm \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 \
  -serial mon:stdio \
  -device virtio-net-pci,netdev=net0
