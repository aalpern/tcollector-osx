# tcollector-osx

Simple OpenTSDB collector scripts for OS X.

* ```dfstat.py```, adapted from the version included in [tcollector](https://github.com/stumbleupon/tcollector). It has the limitation that the ```fstype=``` tag is missing from the generated metrics, because OS X's version of ```df``` doesn't expose that information. 
* ```vmstat.py```, handles the system memory usage exposed by ```vm_stat```
* ```load.py``` creates metrics from the CPU usage and load averages produced by ```iostat```. Doesn't handle the disk I/O data yet (coming shortly).
