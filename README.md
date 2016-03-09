# XRootD on Travis CI [![Build Status](https://travis-ci.org/alexpearce/XRootD-Travis.svg?branch=master)](https://travis-ci.org/alexpearce/XRootD-Travis)

Trying to compile [XRootD][1] on [Travis CI][2].

Files on EOS are not publicly readable by default. This can be changed with 
something like:

```bash
$ eos chmod -r 775 /eos/path/to/folder
```
