import sys
import os
import time
import psutil
import subprocess
import signal

def _split_line(line):
    return(line.strip().split(";"))

def get_cpu_usage(line):
    return 100 - float(_split_line(line)[1])

def get_mem_usage(total_mem, line):
    percentage = 1 - ((float(_split_line(line)[1]))/100)
    print(percentage)
    return (total_mem * percentage)

def get_io_usage(line):
    return(int(_split_line(line)[4]))
    
def main(args):
    testing = str(args[0])
    if testing == "all":
        cpu_file_path = str(args[1])
        mem_file_path = str(args[2])
        io_file_path = str(args[3])
        
        cpu_file = open(cpu_file_path, 'r') 
        mem_file = open(mem_file_path, 'r') 
        io_file = open(io_file_path, 'r') 
        total_mem = psutil.phymem_usage().total
        
        cpu_lines = cpu_file.readlines()
        mem_lines = mem_file.readlines()
        io_lines = io_file.readlines()
        
        for i in range(1,len(cpu_lines)):
            cpu_line = cpu_lines[i]
            mem_line = mem_lines[i]
            io_line = io_lines[i]
    
            cpu_usage = get_cpu_usage(cpu_line)
            mem_usage = get_mem_usage(total_mem, mem_line)
            io_usage = get_io_usage(io_line)
    
            #All together  
            cmd = "lookbusy -c %i -m %i -d %i" % (cpu_usage, mem_usage, io_usage)
            
            
            os.system(cmd)
            
            time.sleep(60)
            
    elif testing == "cpu":
        cpu_file_path = str(args[1])
        cpu_file = open(cpu_file_path, 'r') 
        cpu_lines = cpu_file.readlines()
        
        for i in range(1,len(cpu_lines)):
            cpu_line = cpu_lines[i]
           
            cpu_usage = get_cpu_usage(cpu_line)
            
            cmd = "exec lookbusy -c %i" % (cpu_usage)
            
            p = subprocess.Popen(cmd,
                    stdout=subprocess.PIPE,
                    shell=True,
                    preexec_fn=os.setsid)
            
            time.sleep(60)
            os.killpg(p.pid, signal.SIGTERM)
            time.sleep(5)
    elif testing == "mem":
        mem_file_path = str(args[1])
        mem_file = open(mem_file_path, 'r') 
        total_mem = psutil.phymem_usage().total
        mem_lines = mem_file.readlines()

        for i in range(1,len(cpu_lines)):
            mem_line = mem_lines[i]
            mem_usage = get_mem_usage(total_mem, mem_line)
            
            cmd = "lookbusy -m %i" % (mem_usage)
                
            os.system(cmd)
            
            time.sleep(60)
            
    else:
        io_file_path = str(args[1])
        io_file = open(io_file_path, 'r') 
        io_lines = io_file.readlines()
        for i in range(1,len(io_lines)):
            io_line = io_lines[i]
    
            io_usage = get_io_usage(io_line)
    
            cmd = "lookbusy -d %i" % (io_usage)
            
            os.system(cmd)
            
            time.sleep(60)

if __name__ == "__main__":
  main(sys.argv[1:])                                                             

