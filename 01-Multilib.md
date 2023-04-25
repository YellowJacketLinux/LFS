Multilib Plans
==============

My build of LFS is 64-bit but is not multilib, meaning it does not
support building or running 32-bit binaries.

My impression is that the biggest uses of a 32-bit compatible environment
within 64-bit GNU/Linux is WINE (an environment for running some 32-bit
Windows applications) and some games.

There also are some closed-source applications, like an AAC encoder
that used to be popular before FFmpeg caught up, that were (or are)
only available as 32-bit binaries.

Multilib is a low priority for me but when I do it, what I hope to do
is install the 32-bit environment within `/opt/compat-32` as the install
prefix rather than `/usr` which then forces the use of `/{,usr/}lib64`
for the 64-bit libraries.

Another possibility is to use `/{,usr/}lib32` for 32-bit libraries,
but I would rather just put the 32-bit environment within `/opt/compat-32`
and not have to use bit-specific library directories.

I have no plans to support a 32-bit bit build of YJL. 64-bit systems
have been the standard for about two decades now.
