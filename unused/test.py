from flask import Flask, render_template, request, redirect, url_for
from pypsrp.client import Client
import requests
import paramiko
import getpass


app = Flask(__name__)
# WINDOWS
def ssh_connection(host, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port=port, username=username, password=password)
    return ssh_client

def psrp_connection(hostname, username, password):
    
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

        psrp_result = execute_psrp_script(psrp_client, 'Get-ComputerInfo')
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


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if request.form['username'] == '1234' and request.form['password'] == 'abcd':
            return redirect(url_for('gridsystem'))
        else:
            return 'Login Failed. Please check your credentials.'
    return render_template('login.html')


@app.route('/gridsystem', methods=['GET','POST'])
def gridsystem():
    return render_template("gridsystem.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        command = request.form.get('command')  # Get the command from the form
        if command:
            try:
                result = main()
                # After executing the command, redirect to the 'system_info' page
                return render_template('search.html', results=result)
            except Exception as e:
                return render_template('search.html', error=str(e))

    # If no command was submitted or there was an error, show an empty result.
    return render_template('search.html', results={})


@app.route('/start_service', methods=['POST'])
def start_service():
    if request.method == 'POST':
        powershell_command = "Start-Service"
        result = execute_powershell_commands()
        return f":{result}"

@app.route('/get_service', methods=['POST'])
def get_service():
    if request.method == 'POST':
        powershell_command = "get-Service"
        result = execute_powershell_commands()
        return f":{result}"


@app.route('/hostname', methods=['POST'])
def get_hostname():
    if request.method == 'POST':
        powershell_command = "hostname"
        result = execute_powershell_commands()
        return f":{result}"


@app.route('/get_wmi_object', methods=['POST'])
def get_wmi_object():
    if request.method == 'POST':
        powershell_command = "Get-WmiObject -Class Win32_ComputerSystem"
        result = execute_powershell_commands()
        return f":{result}"


@app.route('/get_computer_info', methods=['POST'])
def get_computer_info():
    if request.method == 'POST':
        powershell_command = "Get-ComputerInfo"
        result = execute_psrp_script()
        return f":{result}"

@app.route('/linuxsearch', methods=['GET', 'POST'])
def linuxsearch():
        if request.method == 'POST':
            command = request.form.get('command')
            if command:
                try:
                    result = execute_bash_command(command)
                    return render_template('linuxsearch.html', results=result)
                except Exception as e:
                    return render_template('linuxsearch.html', error=str(e))

        return render_template('linuxsearch.html', results={}) 

hostname = "dev.autointelli.com"
port = 20222
username = "root"
password = "@ut0!ntell!@123"    



@app.route('/uname_a', methods=['POST'])
def uname_a():
        if request.method == 'POST':
            command = "uname -a"
            result = execute_bash_command(command)
            return f":{result}"

if __name__ == "__main__":
    app.run (port=5000)