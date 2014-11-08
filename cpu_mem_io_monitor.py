import re
import sys
import psutil
import time
from datetime import datetime

def parse_line(date, output_value):
    line = date.strftime("%d-%m-%y %H:%M:%S") + ";" + str(output_value)
    return line


def _write(f, line):
    f.write(line+"\n")


def main(args):
    run_forever = str(args[0])
    cpu_out_file = str(args[1])
    mem_out_file = str(args[2])
    io_out_file = str(args[3])
    cpu_out = open(cpu_out_file, 'w')
    _write(cpu_out,"timestamp;cpu_idle")
    mem_out = open(mem_out_file, 'w')
    _write(mem_out,"timestamp;mem_free")
    io_out = open(io_out_file, 'w')
    _write(io_out,"timestamp;read_count;write_count;read_bytes;write_bytes")
    if run_forever == 'TRUE':
        while(True):
            get_cpu_idle_percentage(cpu_out, interval=1, rounds=5)
            get_free_mem(mem_out, interval=1,rounds=5)
            get_io_usage(io_out, interval=1, rounds=5)

            time.sleep(10)


def get_cpu_idle_percentage(out, interval=1, rounds=5):
    measurements = []
    for x in range(rounds):
        measure = psutil.cpu_times_percent(interval=1, percpu=False)
        idletime = measure.idle + measure.iowait
        measurements.append(idletime)

    time_now = datetime.now()
    to_write = parse_line(time_now, _calculate_average(measurements))
    _write(out, to_write)


def get_free_mem(out, interval=1, rounds=5):
    measurements = []
    for x in range(rounds):
        measure = psutil.virtual_memory()
        free_mem = 100 - measure.percent
        measurements.append(free_mem)

    time_now = datetime.now()
    to_write = parse_line(time_now, _calculate_average(measurements))
    _write(out, to_write)


def get_io_usage(out, interval=1, rounds=5):
    read_count_list = []
    write_count_list = []
    read_bytes_list = []
    write_bytes_list = []
    for x in range(rounds):
        measure = psutil.disk_io_counters(perdisk=False)
        read_count = measure.read_count
        write_count = measure.write_count
        read_bytes = measure.read_bytes
        write_bytes = measure.write_bytes

        read_count_list.append(read_count)
        write_count_list.append(write_count)
        read_bytes_list.append(read_bytes)
        write_bytes_list.append(write_bytes)

    read_count_averages = _calculate_average(read_count_list)
    write_count_averages = _calculate_average(write_count_list)
    read_bytes_averages = _calculate_average(read_bytes_list)
    write_bytes_averages = _calculate_average(write_bytes_list)

    value = (str(read_count_averages) + ";" + str(write_count_averages) + ";" +
             str(read_bytes_averages) + ";" + str(write_bytes_averages))

    time_now = datetime.now()
    to_write = parse_line(time_now, value)
    _write(out, to_write)


def _calculate_average(values):
    return (sum(values)/ len(values))


if __name__ == "__main__":
    main(sys.argv[1:])
