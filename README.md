# tcollector-osx

Simple OpenTSDB collector scripts for OS
X. [tcollector](https://github.com/stumbleupon/tcollector) itself runs
unmodified on OS X, once you install pgrep, which you can do with
[Homebrew](http://mxcl.github.com/homebrew/).

```
brew install pgrep
```

* ```dfstat.py```, adapted from the version included in
  [tcollector](https://github.com/stumbleupon/tcollector). It has the
  limitation that the ```fstype=``` tag is missing from the generated
  metrics, because OS X's version of ```df``` doesn't expose that
  information.

* ```vmstat.py```, handles the system memory usage exposed by ```vm_stat```

* ```iostat.py``` creates metrics from the CPU usage, disk, and load
  averages produced by ```iostat```.
