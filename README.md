# qemu-trace

This is the steps of collecting qemu trace.

## Get a linux kernel

Mainly follow the tutorial [here](https://www.cyberciti.biz/tips/compiling-linux-kernel-26.html#google_vignette)

### Download the kernel
Move to the directory where you want to download the kernel source code. 
```bash
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.9.tar.xz
tar xvf linux-5.16.9.tar.xz 
```

### Configure the kernel
I suggest that you copy existing config file using the cp command:
```bash
cd linux-5.16.9
cp -v /boot/config-$(uname -r) .config
```

### Install the required tools
```bash
sudo apt-get install build-essential libncurses-dev bison flex libssl-dev libelf-dev
```

## Adjust the kernel source code
Here is where the hacking is, the idea is to hack `do_swap_page` function in the kernel source code such that it prints the address of the page being swapped and the `pc/ip` of the instruction that caused the page to be swapped.

### `memory.c`
This is where the `do_swap_page` function is defined. The file is located at `mm/memory.c`. The function is defined as follows:

Replace it with the `memory.c` file in this repository.

Note: There is a macro `PRINT_PAGE_CONTENT` that is defined in the `memory.c` file. This macro is used to print the content of the page being swapped. You can define it to print the content of the page being swapped. The default is to **undef** it.

### `internal.h`
There are a few function definitions that I changed in the `internal.h` file. The file is located at `mm/internal.h`. Replace it with the `internal.h` file in this repository.

What I did was to pass the register struct to the `do_swap_page` function. This is because I want to print the `pc/ip` of the instruction that caused the page to be swapped.

## Compile the kernel
```bash
make menuconfig
# Nothing to do here, just save and exit
make -j $(nproc)
# This will take a while to build
```

### possible errors 1
It might be possible to see the error: `No rule to make target 'debian/canonical-certs.pem', needed by 'certs/x509_certificate_list'`

It is due to missing these files. My solution is to copy the files from the current running kernel. Note that the kernel running is `5.15.0-122-generic` while the kernel being built is `5.16.9`. Since not so far off, it worked for me. The solution is copied from [here](https://stackoverflow.com/questions/67670169/compiling-kernel-gives-error-no-rule-to-make-target-debian-certs-debian-uefi-ce)

Steps are below:
```bash
# check out the .config file
vim .config
# search for CONFIG_SYSTEM_TRUSTED_KEYS
```
You might see the following:
```
# Certificates for signature checking
#
CONFIG_MODULE_SIG_KEY="certs/signing_key.pem"
CONFIG_MODULE_SIG_KEY_TYPE_RSA=y
# CONFIG_MODULE_SIG_KEY_TYPE_ECDSA is not set
CONFIG_SYSTEM_TRUSTED_KEYRING=y
CONFIG_SYSTEM_TRUSTED_KEYS="debian/canonical-certs.pem"
CONFIG_SYSTEM_EXTRA_CERTIFICATE=y
CONFIG_SYSTEM_EXTRA_CERTIFICATE_SIZE=4096
CONFIG_SECONDARY_TRUSTED_KEYRING=y
CONFIG_SYSTEM_BLACKLIST_KEYRING=y
CONFIG_SYSTEM_BLACKLIST_HASH_LIST=""
CONFIG_SYSTEM_REVOCATION_LIST=y
CONFIG_SYSTEM_REVOCATION_KEYS="debian/canonical-revoked-certs.pem"
# end of Certificates for signature checking
```

Then copy the files from running kernel to the specified location in the kernel being built.
```bash
sudo apt install linux-source
sudo cp -v /usr/src/linux-source-*/debian/canonical-*.pem PATH/TO/YOUR/debian/
```

### possible errors 2
Another error I see: 
```
BTF: .tmp_vmlinux.btf: pahole (pahole) is not available
Failed to generate BTF for vmlinux
Try to disable CONFIG_DEBUG_INFO_BTF
make: *** [Makefile:1161: vmlinux] Error 1
```

Try to disable `CONFIG_DEBUG_INFO_BTF` in the `.config` file. And then move on with default options if prompted.

## setup qemu

Now that the kernel is compiled, we can use it to boot a virtual machine using qemu. Start with installing `sudo apt install debootstrap`

Check out `image_create_qemu.sh` script in this repository. This script creates a virtual machine image and installs the necessary packages to boot the virtual machine. Change the size of the image as needed and note how we can adjust the stuff inside the image in current running kernel.




