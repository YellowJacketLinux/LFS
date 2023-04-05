SystemD verses System V Init
============================

My current LFS build is the System V Init build of LFS 11.3.

By the time I finish this current RPM bootstrap, I suspect that a new
LFS version will be available. My plan is at that point in time to
build the SystemD version of LFS and then port my RPM spec files to
use SystemD (really only an issue for daemons).

Initially my plan was to retain a System V Init system but I have since
decided there are enough benefits to SystemD that it is worth it.

So...that is why some RPM spec files currently install System V Init
scripts. That is changing.

Note that the current `%post` and `%preun` scriptlets do not handle
setting up the run levels. It is not worth coming up with the infrastructure
for that (e.g. `chkconfig`) when I will be changing to SystemD anyway. 
