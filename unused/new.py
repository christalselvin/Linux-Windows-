import getpass
import paramiko
import logging

logging.basicConfig(level=logging.INFO)

def ssh_connection(host, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(host, port=port, username=username, password=password)
        logging.info("SSH connection established successfully.")
        return ssh_client
    except Exception as e:
        logging.error(f"Error connecting to {host}: {e}")
        raise

def execute_ssh_command(ssh_client, command):
    try:
        _, stdout, _ = ssh_client.exec_command(command)
        result = stdout.read().decode()
        logging.info(f"Command '{command}' executed successfully.")
        return result
    except Exception as e:
        logging.error(f"Error executing command: {e}")
        raise

def par():
    # Replace these values with your actual connection details
    ssh_host = "dev.autointelli.com"
    ssh_port = 20222
    ssh_username = "root"
    ssh_password = getpass.getpass(prompt="Enter SSH Password: ")

    try:
        ssh_client = ssh_connection(ssh_host, ssh_port, ssh_username, ssh_password)
        ssh_output = execute_ssh_command(ssh_client, 'ls -l')
        print("Paramiko Output:")
        print(ssh_output)

    except KeyboardInterrupt:
        logging.warning("Script interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close connections
        try:
            ssh_client.close()
            logging.info("SSH connection closed.")
        except Exception as e:
            logging.error(f"Error closing SSH connection: {e}")

if __name__ == "__main__":
    par()
