import base64
import paramiko
import pandas as pd
import re 
from time import sleep

# DON'T change these settings!
TESTS = ["create_threads",
        "create_processes",
        "launch_programs",
        "mem_alloc"
        ]
ITERATIONS = 30

# DO change this part!
# the key is tricky just run the program 
# and copy the correct one from the error
OSB_PATH = "/path/to/osbench/out/"
IP_NAME = '192.168.0.102' # or whatever
OUT_FILE_NAME = "baseline_run_3-19" # you may want to date this file
ROOTUSER = 'root'
ROOTPASS = 'root_pass'
# the key is tricky just run the program and copy the correct one from the error
KEY = paramiko.RSAKey(data=base64.b64decode(b'AAAA....PYFqM= root@host_name'))


# this generates the commands
nicety = "nice -n -20 "
test_commands = [ OSB_PATH + c for c in TESTS for i in range(ITERATIONS)]
test_commands =  test_commands + [ nicety + OSB_PATH + c for c in TESTS for i in range(ITERATIONS)]

# Connects to the pi
client = paramiko.SSHClient()
client.get_host_keys().add(IP_NAME, 'ssh-rsa', KEY)
client.connect(IP_NAME, username=ROOTUSER, password=ROOTPASS)

# get the results, this may take some time
metric = []
measure = []
units = []
heat = []
volt = []

# Set the baseline temp that must be matched
stdin, stdout, stderr = client.exec_command('/opt/vc/bin/vcgencmd measure_temp')
for line in stdout:
    h = re.findall(r'[\d+.]+', line)[0]

base_line_temp = h

for i, command in enumerate(test_commands):
    # check the temp every test and make it cool off
    if not ((i+1) % (ITERATIONS)):
        stdin, stdout, stderr = client.exec_command('/opt/vc/bin/vcgencmd measure_temp')
        for line in stdout:
            h = re.findall(r'[\d+.]+', line)[0]
        while base_line_temp < h:
            print(h)
            sleep(1)
    stdin, stdout, stderr = client.exec_command(command)
    results = []
    for line in stdout:
        results.append(line.strip('\n'))
    stdin, stdout, stderr = client.exec_command('/opt/vc/bin/vcgencmd measure_temp')
    for line in stdout:
        h = re.findall(r'[\d+.]+', line)[0]
    heat.append(h)
    stdin, stdout, stderr = client.exec_command('/opt/vc/bin/vcgencmd measure_volts')
    for line in stdout:
        v = re.findall(r'[\d+.]+', line)[0]
    volt.append(v)
    bad, good = results[0].split(' ', 1)
    good, bad = good.split('.', 1)
    metric.append(good)
    m, u = results[1].split(' ', 1)
    measure.append(m)
    units.append(u)

# make a data frame
data = pd.DataFrame()
data['metric'] = metric
data['measure'] = pd.to_numeric(measure)
data['units'] = units
data['heat'] = heat
data['volt'] = volt
nice_flag = ['so nice' for c in TESTS for i in range(ITERATIONS)]
nice_flag = nice_flag + ['not nice' for c in TESTS for i in range(ITERATIONS)]
data['nice'] = nice_flag
sdat = data[['metric', 'nice', 'units', 'measure']]

# Aggregate statistics
data_av = data.groupby(['metric', 'units', 'nice']).mean()
data_sd = data.groupby(['metric', 'units', 'nice']).std()
data_av.columns = ['mean']
data_sd.columns = ['standard deviation']
data_stats = data_av.join(data_sd)

data.to_feather(OUT_FILE_NAME + ".ftr")
data.to_csv(OUT_FILE_NAME + ".csv")
data_stats.to_csv(OUT_FILE_NAME + "_stats" + ".csv")


