import os
import sys
import socket
import time
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
savePath = ""
clear()
# Automatically install dependencies
os.system("pip install requests\n\n\n")
import requests




def get_ip(): # Get the local ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def manualOs():
    manualOs = input("Does your computer use .sh(linux/unix/mac) or .bat(windows) scripts?\n[.sh/.bat] ")
    if manualOs == ".sh":
        script = "bash"
    elif manualOs == ".bat":
        script = "windows"
    else:
        print("You will have to manually set up the server from here. Your os is not supported")


# BEGINNING OF CODE

# Ask the user for the version they want
verson = input("What minecraft version will the server be?\n")
response = requests.get("https://api.papermc.io/v2/projects/paper/versions/" + verson)

while True:
    # Find the latest build of the selected minecraft version
    if response.status_code == 200:
        data = response.json()
        latestBuild = data["builds"][-1]
        response = requests.get("https://api.papermc.io/v2/projects/paper/versions/" + verson)
        break
    else: # If the requested version does not exist then list the available versions
        response = requests.get("https://api.papermc.io/v2/projects/paper")
        data = response.json()
        availableVersions = data["versions"]
        print("List of available versions:\n" + str(availableVersions))

# Get the save path from the user
while True:
    selection = int(input("Where do you want to save the minecraft server?\n1) Desktop\n2) Current directory\n3) Somewhere else\n[1/2/3] "))
    if selection == 1:
        savePath = '~/Desktop'
    elif selection == 2:
        savePath = os.getcwd()
    elif selection == 3:
        savePath = input(
            "Where do you want to save your minecraft server? (your user will need write access to that path)\n")
    else:
        break
    break
savePath = os.path.expanduser(savePath)
if savePath == '':
    savePath = '.'

# Ask the user for server name
name = input("What do you want to name the server?\n")

# Download the minecraft version selected with the newest build of paper
while True:
    response = requests.get("https://api.papermc.io/v2/projects/paper/versions/" + verson + "/builds/" + str(latestBuild) + "/downloads/paper-" + verson + "-" + str(latestBuild) + ".jar")
    if response.status_code == 200:
        if os.path.exists(savePath + "/" + name):
            print("The server will be saved in " + savePath + "/" + name)
            os.chdir(savePath + "/" + name)
        else:
            if not os.path.exists(savePath):
                os.makedirs(savePath)
                os.chdir(savePath + "/" + name)
            os.makedirs(savePath + "/" + name)
            print("The directory was created successfully and the server will be saved in " + savePath + "/" + name)
            os.chdir(savePath + "/" + name)
        with open("server.jar", "wb") as f:
            f.write(response.content)
            print("Minecraft server files downloaded!")
            break
    else:
        print("ERROR: ", response.status_code)
        exit()
# Begin setup
print("Now we will start setting up the server!")
# Detect platform to chose from .sh or .bat files
if sys.platform.startswith('win'):
    script = "windows"
    if not input(
            "We detected you're running windows so we will make a batch script. Is this correct?\n[Y/N] ").lower() == "y":
        manualOs()
elif sys.platform.startswith('linux'):
    script = "bash"
    if not input(
            "We detected you're running linux so we will make a bash script. Is this correct?\n[Y/N] ").lower() == "y":
        manualOs()
elif sys.platform.startswith('darwin'):
    script = "bash"
    if not input(
            "We detected you're running OSX so we will make a bash script. Is this correct?\n[Y/N] ").lower() == "y":
        manualOs()
else: # If the user says they use a different os then ask them to manually set .sh or .bat
    manualOs()
while True: # Ask the user to accept the minecraft EULA and keep asking until they say yes or close the program
    if input("Do you accept the minecraft EULA (https://aka.ms/MinecraftEULA)?\n[Y/N] ").lower() == "y":
        with open("eula.txt", "w") as f:
            f.write(
                "#EULA accepted by user with MinecraftServerMaker.py\n#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\neula=true")
            break
    else:
        print("To continue you have to accept the EULA by pressing y")
# Ask the user how much ram they would like the server to use
ram = input("How much ram do you want to give to the server in Gigabytes? (ex. 2 = 2 Gigabytes)\n")
if script == "bash":
    with open("run.sh", "w") as f:
        f.write("#!/bin/bash\njava -Xmx" + ram + "G -Xms" + ram + "G -jar server.jar\necho \"Server off. Press enter to close\" \nread")
    os.chmod("run.sh", 0o755)
if script == "windows":
    with open("run.bat", "w") as f:
        f.write("java -Xmx" + ram + "G -Xms" + ram + "G -jar server.jar\npause")
    # Windows firewall instructions
    print("\nWhen the server opens for the first time you might see a windows firewall popup. If you do then allow it for both public and private networks.\n")

# General port forwarding instructions
print("\nPort forwarding:\nFor other people to join your minecraft server you need to forward port 25565 to " + get_ip() + ".")
print("To do this you can try these links to access your router\'s settings:\n10.0.0.1\n192.168.0.1\n192.168.2.1")

# Ask the user if they would like to test the server
if input("\n\nDo you want to test the server now?\n[Y/N] ").lower() == "y":
    # Instructions to test server
    print("\n\nIf the server successfuly starts up the console will say \"Done\" and you can type stop then press enter in the terminal to close")
    time.sleep(3)
    if script == "bash":
        os.system("./run.sh")
    if script == "windows":
        os.system("./run.bat")
    # Basic troubleshooting
    if input("Did the server start?\n[Y/N] ").lower() == "n":
        if input("Did it say something about java or JDK?\n[Y/N] ").lower() == "y":
            print("Download the latest version of java from https://www.oracle.com/ca-en/java/technologies/downloads/ then run run.bat or run.sh")

# OS specific instructions to run the server
if script == "bash":
    print("\nTo run your server go to " + os.getcwd() + " and open \"run.sh\"\n")
if script == "windows":
    print("\nTo run your server go to " + os.getcwd() + " and open \"run.bat\"\n")
