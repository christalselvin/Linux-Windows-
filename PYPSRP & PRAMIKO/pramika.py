import paramiko

hostname = '172.24.193.135'
port = 22
user = 'amrith'
passwd = 'amrith'
 
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port=port, username=user, password= passwd)
try:
        cmd = "whoami"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
except Exception as err:
        print(str(err)) 

