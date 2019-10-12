# PykdKernelTools
A collection of python scripts to be used alongside pykd within WinDBG.


## bin.py
**aka Break In**

Allows you to break into a process without having to use the `.process` command. If there are multiple matches, this will just switch to the first process found to match.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/bin.gif)


## bol.py
**aka Break On Load**

Allows you to break into a process at the point that it loads a specific image.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/bol.gif)


## bop.py
**aka Break On Process**

Allows you to set a breakpoint that only gets triggered when the process matches the given process name.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/bop.gif)


## objdump.py
**aka Object Dump**

Prints all objects contained in the object table, along with the object statistics, including how many objects are currently in use across the machine.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/objdump.gif)


## regdump.py
**aka Register Dump**

Dumps all prominent register values in a readable format.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/regdump.png)


## syscall.py
**aka Display Syscall**

Gives you the resulting kernel function called to from a syscall.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/syscall.png)


## tokenatt.py
**aka Token Attributes**

Prints the token attributes that are currently missing from the `!token` command.

![alt text](https://github.com/TomCouser/PykdKernelTools/blob/master/images/tokenatt.png)

