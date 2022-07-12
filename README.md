# SWDET 
## Description:  
Simple Website Directory Enumeration Tool is a small programm written in Python, that tries to automate the process of searching for website's files and directories.

## Usage:  
SWDET takes arguments, some of what you have to specify before executing.
> -h, --help : show the help message and exit.  
> -u, --uri : save uri to begin the bruteforcing process.  
> -w, --wordlist : point SWDET to a wordlist.   
> -m, --head : use HEAD method instead of GET.  
> -r, --redirects : allow redirects. **(only for swdet.py)**  
> -t, --threads : a number of threads to be used. **(only for swdet-mt.py)**  
  
SWDET does not automatically filter output. You can do it yourself by piping it into awk or grep:  
`python3 src/swdet.py -u https://<website>/ -w src/wl.txt | grep 200`  
OR something like  
`python3 src/swdet.py -u https://<website>/ -w src/wl.txt | grep -v 404`  

## How it works:
When executed - SWDET starts sending requests forming targets using given wordlist,  
it then writes the received data to stdout. You can redirect it into a file.  
It is expected that you, as the end user, will make your assumptions based on the status code.  
SWDET does not recurse into directories.  
SWDET is better suited for scripts.

## What's new:
It is now possible to send requests using HEAD method instead of GET.  
I also added a version that uses threading and queue instead of asyncio and aiohttp.  
I was highly inspired by [this](https://stackoverflow.com/questions/35747235/python-requests-threads-processes-vs-io) question in my tool selection.   
This boosted the speed to the incredible 576 rps (on a 5G wifi).  
I am planning to make a uri normalization algorithm to make the program more human-usable.  
-
Implemented very basic exception handling. One step closer to normal logging.


## License:
SWDET - Simple Website Directory Enumeration Tool; SWDET-MT - Simple Website Directory Enumeration Tool - Multi Threaded  
Copyright (C) 2022  Jaraslau

These programs are free software: you can redistribute them and/or modify
them under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

These programs are distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
