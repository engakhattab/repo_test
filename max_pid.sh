#!/bin/bash

# Get the maximum value representable by a PID data type
max_pid=$(cat /proc/sys/kernel/pid_max)

echo "Maximum PID Value: $max_pid"
