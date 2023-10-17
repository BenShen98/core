"--privileged" runArgs allows usbip in the container to mount devices
To get usb device dynamically:
1. in windows: `usbipd bind -b 2-4`
2. in container: `sudo ./usbip attach -r 192.168.0.76 -b 2-4`