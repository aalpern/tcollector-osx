#!/usr/bin/python
# This file is and add-on to tcollector for OS X. 
# It is derived from the original dfstats.py in tcollector. 
#
# Original Copyright:
# Copyright (C) 2010  StumbleUpon, Inc.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.
"""df disk space and inode counts for TSDB """
#
# dfstat.py
#
# df.1kblocks.total      total size of fs
# df.1kblocks.used       blocks used
# df.1kblocks.available  blocks available
# df.inodes.total        number of inodes
# df.inodes.used         number of inodes
# df.inodes.free         number of inodes

# All metrics are tagged with mount=

# Unfortunately, OS X does not report filesystem type in its
# implemented of df, so the type= tag is not added here.

import os
import subprocess
import sys
import time

COLLECTION_INTERVAL = 60  # seconds

# Differences from dfstats.py for Linux:
#   * The type= tag is not emitted, because OS X does not include fs
#     type information in df's output.
#   * Block and inode stats are obtained in one invocation of df
#
# In order to run tcollector, you must install pgrep. 
# If using brew,
#     brew install pgrep

def main():
    """dfstats main loop"""

    while True:
        ts = int(time.time())
        # 1kblocks
        df_proc = subprocess.Popen(["df", "-lki"], stdout=subprocess.PIPE)
        stdout, _ = df_proc.communicate()
        if df_proc.returncode == 0:
            for line in stdout.split("\n"): # pylint: disable=E1103
                fields = line.split()
                # skip header/blank lines
                if not line or not fields[2].isdigit():
                    continue

                mount = fields[8]
                if mount.startswith("/Volumes/Time Machine Backups"):
                    continue

                print ("df.1kblocks.total %d %s mount=%s"
                       % (ts, fields[1], mount))
                print ("df.1kblocks.used %d %s mount=%s"
                       % (ts, fields[2], mount))
                print ("df.1kblocks.free %d %s mount=%s"
                       % (ts, fields[3], mount))
                print ("df.inodes.total %d %d mount=%s"
                       % (ts, int(fields[5]) + int(fields[6]), mount))
                print ("df.inodes.used %d %s mount=%s"
                       % (ts, fields[5], mount))
                print ("df.inodes.free %d %s mount=%s"
                       % (ts, fields[6], mount))

        else:
            print >> sys.stderr, "df -lki returned %r" % df_proc.returncode

        sys.stdout.flush()
        time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
    main()
