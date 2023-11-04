# Attach device to container dynamically
"--privileged" runArgs allows usbip in the container to mount devices
To get usb device dynamically:
1. in windows: `usbipd wsl bind -b 2-4`
2. in wsl: `sudo echo 'c 166:* rwm' > /sys/fs/cgroup/devices/docker/eb6ee91aaf*/devices.allow`
<!-- 3. in container: `sudo ./usbip attach -r 192.168.0.76 -b 2-4` -->

## refs
- https://www.kernel.org/doc/Documentation/cgroup-v1/devices.txt
-