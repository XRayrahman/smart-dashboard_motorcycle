from subprocess import Popen, PIPE, STDOUT, check_output
import subprocess
from threading import Timer
#
#kill = lambda process: process.kill()
#cmd = ['python3 rfcomm_server.py']
#ping = subprocess.Popen(
#    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#my_timer = Timer(5, kill, [ping])
#try:
#    my_timer.start()
#    stdout, stderr = ping.communicate()
#finally:
#    my_timer.cancel()

command = "python3 rfcomm_server.py"
with open("rfcomm_server.log","wb") as out, open("rfcomm_serverr.log","wb") as err:
    p = subprocess.Popen(['python3', 'rfcomm_server.py'], stdout=out, stderr=err)
#with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
#    output = process.communicate()[0].decode("utf-8")
#    print(output)

#blu = check_output("python3 rfcomm_server.py", shell=True);
#try:
#    stdout = blu.stdout.read()
#except:
#    pass
#print(stdout)

display = Popen("python3 main.py", shell=True);

while True:
    stdout = p.stdout
    print(stdout)
    if not stdout:
            break