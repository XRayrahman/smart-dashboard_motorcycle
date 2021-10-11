#!/usr/bin/python3
import subprocess
import _thread
import time

# Define a function for the thread
def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        result = subprocess.run("%s" %(threadName), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout = result.stdout
        print(stdout)
        #print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("python3 rfcomm_server.py", 4, ) )
   _thread.start_new_thread( print_time, ("python3 main.py", 4, ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass