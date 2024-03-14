import requests
from pypsrp.client import Client

def psrp_connection(hostname, username, password):
    # Disable SSL verification (not recommended for production)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Create a PyPSRP client with SSL verification disabled
    psrp_client = Client(server=hostname, username=username, password=password, ssl=False)
    return psrp_client

def execute_psrp_script(psrp_client, script):
    return psrp_client.execute_ps(script)

def main():
    psrp_host = "192.168.1.5"
    psrp_username = ''
    psrp_password = ''

    try:
        psrp_client = psrp_connection(psrp_host, psrp_username, psrp_password)

        psrp_result = execute_psrp_script(psrp_client, 'hostname')
        print("\nPyPSRP Output:")
        print(psrp_result)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close connections
        try:
            psrp_client.close()
        except:
            pass

if __name__ == "__main__":
    main()
