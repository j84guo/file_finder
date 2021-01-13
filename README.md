# Description
This tool aims to make it easier to find files in a directory tree from the
terminal, without having to know their full paths ahead of time. 

File paths descending from the current directory which match a pattern 
(pattern is subsequence of path component) are displayed in a terminal 
menu (sorted by Levenshtein distance). Selecting one file causes its full 
path to be printed out by the tool, making it possible to chain this tool
with other programs, e.g. something like ```vim $(file_finder)```.

It's a super simple version of [fzf](https://github.com/junegunn/fzf).

![](demo.gif)

# Improvements
There are many improvements one could make. 

Notably, directory walking and file path matching occur in the UI's main 
event loop, which of course is a big no no as the UI noticeably hangs for 
large directories, e.g. from root. A more scalable design could have the
directory walking and pattern matching occur in a concurrent worker 
(std::thread, goroutine, multiprocessing.Process) which communicates with
the UI's main event loop via IPC. [urwid](http://urwid.org/), which powers
the UI, allows concurrent workers' output to be detected by its
(```select()```-based) event loop via pipe file descriptors for example.

I tried to implement this improvement today but found I lacked the time
right now. I hope this short (and sweet?) sample is helpful to you in
the meantime :) Thanks for visiting my Github!
