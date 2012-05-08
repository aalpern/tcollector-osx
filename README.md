# tcollector-osx

Simple OpenTSDB collector scripts for OS
X. [tcollector](https://github.com/stumbleupon/tcollector) itself runs
unmodified on OS X, once you install pgrep, which you can do with
[Homebrew](http://mxcl.github.com/homebrew/).

```
brew install pgrep
```

## Collectors

These have been tested on OS X 10.7 Lion only. Your mileage may vary
on older releases.

* ```dfstat.py```, adapted from the version included in
  [tcollector](https://github.com/stumbleupon/tcollector). It has the
  limitation that the ```fstype=``` tag is missing from the generated
  metrics, because OS X's version of ```df``` doesn't expose that
  information.

* ```vmstat.py```, handles the system memory usage exposed by ```vm_stat```

* ```iostat.py``` creates metrics from the CPU usage, disk, and load
  averages produced by ```iostat```.

## Other Stats

Apple seems to enjoy making the output of their stats utilities human
readable, but harder to machine parse. ```netstat -m```, ```netstat
-mm```, and ```netstat -s```, for example.
