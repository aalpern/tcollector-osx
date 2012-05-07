#!/usr/bin/python
# This file is and add-on to tcollector for OS X. 

import os
import subprocess
import sys
import time

COLLECTION_INTERVAL = 10  # seconds

# Mach Virtual Memory Statistics: (page size of 4096 bytes)
# Pages free:                         850318.
# Pages active:                       891845.
# Pages inactive:                     268414.
# Pages speculative:                  492338.
# Pages wired down:                   640591.
# "Translation faults":           1186269289.
# Pages copy-on-write:              43790753.
# Pages zero filled:               734503505.
# Pages reactivated:                   16570.
# Pageins:                           7818880.
# Pageouts:                              513.
# Object cache: 92 hits of 5104223 lookups (0% hit rate)

def main():
    while True:
        ts = int(time.time())

        proc = subprocess.Popen(["vm_stat"], stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
        if proc.returncode == 0:
            for line in stdout.split("\n"): # pylint: disable=E1103
                # skip blank lines
                if not line:
                    continue
                if line.startswith("Object cache"):
                    continue
                if line.startswith("Mach Virtual"):
                    continue

                fields = line.split(':')
                value = fields[1].strip().replace('.', '')
                if fields[0].startswith("Pages"):
                    name  = fields[0].strip().replace('Pages ', '').replace(' ', '')
                    print ("vm.4kpages.%s %d %s"
                           % (name, ts, value))
                elif fields[0] == 'Pageins':
                    print ("vm.pageins %d %s"
                           % (ts, value))
                elif fields[0] == 'Pageouts':
                    print ("vm.pageouts %d %s"
                           % (ts, value))

        else:
            print >> sys.stderr, "vm_stat returned %r" % proc.returncode

        sys.stdout.flush()
        time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
    main()
