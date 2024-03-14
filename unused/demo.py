import paramiko
from pypsrp.client import Client
import getpass
import requests

def ssh_connection(host, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port=port, username=username, password=password)
    return ssh_client

def psrp_connection(hostname, username, password):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    psrp_client = Client(server=hostname, username=username,password=password,ssl=False)
    return psrp_client

def execute_ssh_command(ssh_client, command):
    _, stdout, _ = ssh_client.exec_command(command)
    return stdout.read().decode()

def execute_psrp_script(psrp_client, script):
    return psrp_client.execute_ps(script)

def main():
    # Replace these values with your actual connection details
    ssh_host = "dev.autointelli.com"
    ssh_port = 20222
    ssh_username = "root"
    ssh_password = getpass.getpass(prompt="Enter SSH Password: ")

    psrp_host = "192.168.1.5"
    psrp_username = ''
    psrp_password = ''
    

    try:
        ssh_client = ssh_connection(ssh_host, ssh_port, ssh_username, ssh_password)
        psrp_client = psrp_connection(psrp_host, psrp_username, psrp_password)

        ssh_output = execute_ssh_command(ssh_client, 'ls -l')
        print("Paramiko Output:")
        print(ssh_output)

        psrp_result = execute_psrp_script(psrp_client, 'hostname')
        print("\nPyPSRP Output:")
        print(psrp_result)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close connections
        try:
            ssh_client.close()
        except:
            pass

        try:
            psrp_client.close()
        except:
            pass

if __name__ == "__main__":
    main()
