from flask import Flask, render_template, request, redirect, url_for
import requests
from pypsrp.client import Client

app = Flask(__name__)

hostname = "localhost"
port = 5985
username = ""
password = ""

def execute_powershell_commands():
    try:
        client = Client(
            hostname,
            username=username,
            password=password,
            port=port,
            ssl=False,
            auth="ntlm",
            timeout=60,
        )

        system_info_command = "Get-ComputerInfo"
        system_info_result = client.execute_ps(system_info_command)
        system_info_str = system_info_result[0].strip()

        hardware_info_command = "Get-WmiObject -Class Win32_ComputerSystem"
        hardware_info_result = client.execute_ps(hardware_info_command)
        hardware_info_str = hardware_info_result[0].strip()

        uptime_info_command = "Get-CimInstance -ClassName Win32_OperatingSystem"
        uptime_info_result = client.execute_ps(uptime_info_command)
        uptime_info_str = uptime_info_result[0].strip()

        date_command = "Get-Date"
        date_info_result = client.execute_ps(date_command)
        date_str = date_info_result[0].strip()

        get_child_command = "Get-ChildItem "
        get_child_result = client.execute_ps(get_child_command)
        get_str = get_child_result[0].strip()

        get_host_command = "  Get-Host "
        get_host_result = client.execute_ps(get_host_command)
        host_str = get_host_result[0].strip()


        return {
            "System Information": system_info_str,
            "Hardware Information": hardware_info_str,
            "System Uptime and Last Boot Time": uptime_info_str,
            "Date Info": date_str,
            "Get ChildItem": get_str,
            "Get Host": host_str
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        client.close()

def send_request(action):
    api_endpoint = 'https://your-api.com'
    url = f'{api_endpoint}/{action}'

    try:
        # Make a POST request to the API endpoint
        response = requests.post(url)

        # Check if the request was successful (status code 2xx)
        if response.ok:
            print(f'{action} successful! Response: {response.json()}')
        else:
            # Print the error message if the request was not successful
            print(f'Error during {action}: {response.status_code} - {response.text}')

    except requests.RequestException as e:
        # Handle any exceptions that might occur during the request
        print(f'Request failed: {e}')


# Example usage
    send_request('start')
    send_request('stop')
    send_request('restart')
    send_request('reboot')


@app.route('/system_info', methods=['GET', 'POST'])
def system_info():
    if request.method == 'POST':
        command = request.form['command']
        if command:
            try:
                result = execute_custom_powershell_command(command)
                return render_template('system_info.html', results=result)
            except Exception as e:
                return render_template('system_info.html', error=str(e))


    results = execute_powershell_commands()
    return render_template('system_info.html', results=results)

def execute_custom_powershell_command(command):
    try:
        client = Client(
            hostname,
            username=username,
            password=password,
            port=port,
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
        client.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if request.form['username'] == '1234' and request.form['password'] == 'abcd':
            return redirect(url_for('search'))  # Redirect to the search page on successful login
        else:
            return 'Login Failed. Please check your credentials.'
    return render_template('login.html')


@app.route('/search', methods=['GET', 'POST'])
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



# def execute_powershell_command(command):
#     try:
#         # Create a PSRP client
#         with Client('localhost') as client:
#             # Execute the PowerShell command
#             result = client.execute_ps(command)
            
#             # Read the output
#             output = result[0].stream
#             error = result[1].stream
            
#             if result[1].status_code == 0:
#                 return f"Command executed successfully: {output}"
#             else:
#                 return f"Error executing PowerShell command: {error}"

#     except Exception as e:
#         return f"Error: {e}"



if __name__ == '__main__':
    app.run(debug=True)