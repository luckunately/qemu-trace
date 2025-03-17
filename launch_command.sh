#!/bin/bash

sudo qemu-system-x86_64 \
  -kernel ../linux-qemu/arch/x86_64/boot/bzImage \
  -nographic \
  -drive file=qemu-sda-image.img,media=disk,format=raw \
  -append "console=ttyS0 nokaslr root=/dev/sda rw" \
  -m 32G \
  --enable-kvm \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 \
  -serial mon:stdio \
  -device e1000,netdev=net0 \
  2>&1 | tee qemu.log
