import sys
import os
import time
from datetime import datetime
import psutil
import subprocess
import commands

def _remove_last_char(line):
    return(line[:-1])

def parse_line(date, output_value):
    line = date.strftime("%d-%m-%y %H:%M:%S") + ";" + str(output_value)
    return line

def _write(f, line):
   f.write(line+"\n") 


def main(args):
    bench_type  = str(args[0])
    out_file = str(args[1])
    output = open(out_file, 'w')
    _write(output, "timestamp;process_time")

    while(True):
        cmd = "sysbench --test=%s run | grep 'total time:' | awk '{print $3}'" % (bench_type)
        process_time = _remove_last_char(commands.getstatusoutput(cmd)[1])
        time_now = datetime.now()
	_write(output, parse_line(time_now, process_time))
 
        time.sleep(300)
        
         

if __name__ == "__main__":
  main(sys.argv[1:])                                                             

