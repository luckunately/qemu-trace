#!/bin/bash

sudo cgcreate -g memory:rpe
echo 56M > /sys/fs/cgroup/rpe/memory.high
cgexec -g memory:rpe "$1"