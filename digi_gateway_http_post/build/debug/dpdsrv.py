#####################################################################
# Automatically generated file
# Don't edit this file
# Created on: 1 November 2024
#####################################################################

import threading
import time
import sys, os 

sys.path.insert(0, os.path.join(os.path.abspath('.'), 'dpdebug.zip'))

import pydevd
pydevd.settrace('192.168.1.47', stdoutToServer=False, stderrToServer=False, suspend=False, trace_only_current_thread=False)
threading.settrace(pydevd.GetGlobalDebugger().trace_dispatch)

print "Debugging Python application '%s' ...\r\n" %'http_get_post.py'

if not os.path.isdir('C:/Users/48888/OneDrive/Pulpit/Nowy folder (2)/http_get_post-3/src'):
    execfile(os.path.join(os.path.abspath('.'), 'http_get_post.py'))
else:
    execfile('C:/Users/48888/OneDrive/Pulpit/Nowy folder (2)/http_get_post-3/src/http_get_post.py')

while True:
    time.sleep(60)

