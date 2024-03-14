from pypsrp.client import Client
from pypsrp.powershell import PowerShell

hostname = 'AmrithSubramaniyan'
username = 'amrit'
password = 'Amrith2000'

# Create a PSRP client
client = Client(hostname, username, password)

# Run a simple PowerShell command
ps = PowerShell(client, 'Get-Process')
ps.start()
ps.join()

# Print the results
for result in ps.output:
    print(result)
