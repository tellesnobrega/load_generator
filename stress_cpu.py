import sys
import os
import time
import psutil

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
    cpu_file_path = str(args[0])
    mem_file_path = str(args[1])
    io_file_path = str(args[2])

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

        print(cpu_usage)
        print(mem_usage)
        print(io_line)
  
        cmd = "lookbusy -c %i -m %i -d %i" % (cpu_usage, mem_usage, io_usage)
        
        os.system(cmd)
        
        time.sleep(60)
        
         

if __name__ == "__main__":
  main(sys.argv[1:])                                                             

