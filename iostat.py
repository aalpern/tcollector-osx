#!/usr/bin/python
# This file is and add-on to tcollector for OS X. 

import os
import subprocess
import sys
import time

COLLECTION_INTERVAL = 10  # seconds

#adamalpern@Bliterator: 6:22PM ? iostat  
#          disk0       cpu     load average
#    KB/t tps  MB/s  us sy id   1m   5m   15m
#   30.32  13  0.38   3  1 96  1.67 1.68 1.55

def main():
    while True:
        ts = int(time.time())

        proc = subprocess.Popen(["iostat"], stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()

        cpu_user_index = -1
        cpu_sys_index  = -1
        cpu_idle_index = -1
        load_1m_index  = -1
        load_5m_index  = -1
        load_15m_index = -1

        if proc.returncode == 0:
            lines = stdout.split("\n")
            headers = lines[1].split()
            for i in range(0, len(headers)):
                h = headers[i]
                if h == "us":
                    cpu_user_index = i
                elif h == "sy":
                    cpu_sys_index = i
                elif h == "id":
                    cpu_idle_index = i
                elif h == "1m":
                    load_1m_index = i
                elif h == "5m":
                    load_5m_index = i
                elif h == "15m":
                    load_15m_index = i

            for line in lines:
                if not line:
                    continue
                fields = line.split()
                if not fields[1].isdigit():
                    continue
                print ("cpu.usage.user %d %s" % (ts, fields[cpu_user_index])) 
                print ("cpu.usage.system %d %s" % (ts, fields[cpu_sys_index]))
                print ("cpu.usage.idle %d %s" % (ts, fields[cpu_idle_index]))                       
                print ("load.average.1m %d %s" % (ts, fields[load_1m_index]))
                print ("load.average.5m %d %s" % (ts, fields[load_5m_index])) 
                print ("load.average.15m %d %s" % (ts, fields[load_15m_index]))

        else:
            print >> sys.stderr, "vm_stat returned %r" % proc.returncode

        sys.stdout.flush()
        time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
    main()
