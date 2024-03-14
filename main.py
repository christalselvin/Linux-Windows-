from flask import Flask, render_template, request, redirect, url_for
from pypsrp.client import Client as PSRPClient
import paramiko

app = Flask(__name__)


common_username = ""
common_password = ""

windows_hostname = "localhost"
windows_port = 5985

linux_hostname = "dev.autointelli.com"
linux_port = 20222
linux_username = "root"
linux_password = "@ut0!ntell!@123"

def execute_powershell_commands():
    client = None  
    try:
        # Connect to Windows machine using pypsrp
        client = PSRPClient(
            server=windows_hostname,  
            port=windows_port,
            username=common_username,
            password=common_password,
            ssl=False,
            auth="ntlm",
            timeout=60,
        )

        

    except Exception as e:
        return {"error": {"message": str(e), "type": type(e).__name__}}

    finally:
        if client:
            client.close()

def execute_custom_powershell_command(command):
    client = None 
    try:
        
        client = PSRPClient(
            server=windows_hostname,  
            port=windows_port,
            username=common_username,
            password=common_password,
            ssl=False,
            auth="ntlm",
            timeout=60,
        )

        result = client.execute_ps(command)
        return {
            "Command Result": result[0].strip(),
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if client:
            client.close()



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


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            try:
                result = execute_custom_powershell_command(command)
                return render_template('search.html', results=result)
            except Exception as e:
                return render_template('search.html', error=str(e))

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
        result = execute_powershell_commands()
        return f":{result}"
    
    
def execute_bash_command(command):
    try:
        sshclient = paramiko.SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshclient.connect(
            linux_hostname,
            port=linux_port, 
            username=linux_username,  
            password=linux_password,  
            look_for_keys=False,
            allow_agent=False,
            timeout=60
        )

        result = sshclient.exec_command(command)
        return {
            "Command Result": result[1].read().decode("utf-8").strip()
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        sshclient.close()


@app.route('/linuxsearch', methods=['POST'])
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

@app.route('/uname_a', methods=['POST'])
def uname_a():
    if request.method == 'POST':
        command = "uname -a"
        result = execute_bash_command(command)
        return f":{result}"
    
@app.route('/c_d', methods=['POST'])
def c_d():
    if request.method == 'POST':
        command = "cal"
        result = execute_bash_command(command)
        return f":{result}"
    
@app.route('/p_w_d', methods=['POST'])
def p_w_d():
    if request.method == 'POST':
        command = "pwd"
        result = execute_bash_command(command)
        return f":{result}"

if __name__ == "__main__":
    app.run(port=5000)
