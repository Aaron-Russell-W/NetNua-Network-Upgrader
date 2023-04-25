import paramiko


def update_device_version(device):
    dnsname = device.dnsName
    username = device.loginUser
    password = device.loginPwd
    manufacturer = device.manufacturer

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if manufacturer == 'Cisco':
        try:
            ssh.connect(dnsname, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command("show version")
            output = stdout.readlines()
            output = output[0].split(",")
            version = output[2].replace('Version', '').strip()
            print(version)
            device.currentVersion = version
            device.save()
            return "success"
        except Exception as e:
            return str(e)
    elif manufacturer == 'Arista':
        try:
        # Automatically add SSH keys from servers
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the server
            ssh.connect(dnsname, username=username, password=password)
        # Run the command to get the version from the Cisco device
            stdin, stdout, stderr = ssh.exec_command("show version")
        # Get the output from the executed command
            output = stdout.readlines()
            version = output[5].replace('Software image version:', '').strip()
            device.currentVersion = version
            device.save()
            return "success"
        except Exception as e:
            return str(e)