#!/usr/bin/python
# This file is and add-on to tcollector for OS X. 

import os
import subprocess
import sys
import time

# seconds. The actual interval will be 1 second longer, because iostat
# has a minimum one-second delay to get the current values, rather
# than the values averaged over system uptime.
COLLECTION_INTERVAL = 9  

#adamalpern@Bliterator: 8:18PM ? iostat -c 2 -w 1 
#          disk0           disk1       cpu     load average
#    KB/t tps  MB/s     KB/t tps  MB/s  us sy id   1m   5m   15m
#   28.51  11  0.31    34.61   0  0.00   2  2 96  1.78 1.86 1.54
#    0.00   0  0.00     0.00   0  0.00   3  2 94  1.78 1.86 1.54

def main():
    while True:
        ts = int(time.time())

        proc = subprocess.Popen(["iostat", "-c 2 -w 1"], stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()

        if proc.returncode == 0:
            lines      = stdout.split("\n")
            categories = lines[0].split()
            values     = lines[3].split()
            i          = 0
            for cat in categories:
                if cat.startswith('disk'):
                    print ("iostat.disk.KBt %d %s disk=%s" % (ts, values[i], cat))
                    i += 1
                    print ("iostat.disk.tps %d %s disk=%s" % (ts, values[i], cat))
                    i += 1
                    print ("iostat.disk.MBs %d %s disk=%s" % (ts, values[i], cat))
                    i += 1
                elif cat == "cpu":
                    print ("iostat.cpu.user %d %s" % (ts, values[i]))
                    i += 1
                    print ("iostat.cpu.sys %d %s" % (ts, values[i]))
                    i += 1
                    print ("iostat.cpu.idle %d %s" % (ts, values[i]))
                    i += 1
                elif cat == "load":
                    print ("iostat.loadaverage.1m %d %s" % (ts, values[i]))
                    i += 1
                    print ("iostat.loadaverage.5m %d %s" % (ts, values[i]))
                    i += 1
                    print ("iostat.loadaverage.15m %d %s" % (ts, values[i]))
                    i += 1
        else:
            print >> sys.stderr, "vm_stat returned %r" % proc.returncode

        sys.stdout.flush()
        time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
    main()
