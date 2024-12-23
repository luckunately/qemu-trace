# qemu-trace

This is the steps of collecting qemu trace. It will catch the `pc/ip` of the instruction that caused the page to be swapped and the address of the page being swapped. It can also print the content of the page being swapped.

## Table of Contents

- [Introduction](#qemu-trace)
- [Get a Linux Kernel](#get-a-linux-kernel)
    - [Download the Kernel](#download-the-kernel)
    - [Configure the Kernel](#configure-the-kernel)
    - [Install the Required Tools](#install-the-required-tools)
- [Adjust the Kernel Source Code](#adjust-the-kernel-source-code)
    - [`memory.c`](#memoryc)
    - [`internal.h`](#internalh)
- [Compile the Kernel](#compile-the-kernel)
    - [Possible Errors 1](#possible-errors-1)
    - [Possible Errors 2](#possible-errors-2)
- [Setup QEMU](#setup-qemu)
    - [Install `cgroup`](#install-cgroup)
    - [Launch QEMU](#launch-qemu)
        - [First Time of Launching](#first-time-of-launching)
        - [Running `cgroup` Commands](#running-cgroup-commands)
- [Collecting the Trace](#collecting-the-trace)
    - [Getting Executables](#getting-executables)
        - [Example and Sanity Check](#example-and-sanity-check)
    - [Processing the Trace](#processing-the-trace)

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

### install `cgroup`
For some reason, `cgroup` cannot be installed onto the image the easy way with `chroot` then `apt install`. We need to manually download the package and install it. 

`sudo apt download xxx` will download the package. We shall see the `*.deb` file.

We will need:
1. cgroup-tools
2. libcgroup1
3. Possibly `libc6` if it warns about it.

Suggestion: almost all operations require `sudo` so it is better to be in `root` mode. But with **great power comes great responsibility**.

1. Mount the image into the default folder with `mount -o loop qemu-sda-image.img qemu-hd` and copy the debian pakcage into it.
2. `chroot qemu-hd` and install the packages with `dpkg -i xxx.deb`
3. Check if `cgexec` works. If not, try to install `libc6` package.
4. Exit the `chroot` and unmount the image with `umount qemu-hd`. **WARNING**: Do not forget to unmount the image, otherwise, the data will be corrupted if you try to launch the virtual machine.

The above steps can be used to solve other package installation issues (hopefully).

### launch qemu
Check out `launch_qemu.sh` script in this repository. This script launches the qemu virtual machine with the kernel that was compiled. Change the size of ram and the path to the kernel as needed.

For each launch, just need to type in the password for the `root` user.

#### First time of launching

We need to set up the **swap space**. The script `commands_to_set_up_swap.sh` contains the commands to set up the swap space. Run the commands manually in the virtual machine.

### Running `cgroup` commands

For each launch, we need to create a cgroup with `cgcreate` and then execute the command with `cgexec`. 

An example could be:
```bash
sudo cgcreate -g memory:rpe
echo 56M > /sys/fs/cgroup/rpe/memory.high
```
The above commands create a cgroup named `rpe` and set the memory limit to 56MB.

To run an executable in the cgroup, use the following command:
```bash
cgexec -g memory:rpe ./the_executable
```

This shall run the executable in the cgroup `rpe` and the kernel will report the page swapping information.

### Collecting the trace

Since we are using the console to synchronize the info, we need to keep all the console printout. Thus when we launch the qemu, we need to redirect the output to a file. 

```bash
./launch_qemu.sh > output.log
```

The `output.log` file will contain all the console printout. Then do the usual login and `cgroup` setup in the same terminal that the qemu is running.

#### Getting executables

You can either compile the executables in the virtual machine or copy the executables from the host machine to the virtual machine.

##### Example and sanity check
Check out `rand_then_rand.c` and `shuffle.h` from this repository. Try it out and count the number of page faults. It should only get page faults upon swap. **YES, COLD MISSES** are not collected.

#### Processing the trace

`filter_page_faults.py` will filter out the page faults from the `output.log` file. To use it:
```bash
python3 filter_page_fault.py <input_file> <output_file>
```

This intermediate output will be a `.csv` file with headers `ip,addr`. The `ip` is the `pc/ip` of the instruction that caused the page to be swapped. The `addr` is the memory address of the page being swapped (The page fault address masked by page offset).

`mem_to_delta.py` will convert the memory address to the delta of the memory address. To use it:
```bash
python3 filter_page_fault.py <input_file> <output_file>
```

The final output will be a `.csv` file with headers `ip,delta_in,delta_out`. The `delta_in` is the delta of the memory address of the page being swapped. The `delta_out` is the delta of the `pc/ip` of the instruction that caused the page to be swapped. Both address is shifted by the page offset thus 1 means off by 1 page (4KB).

TODO: ADD support for page content printing.




