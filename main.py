import requests
import os
import sys
import socket

verson = input("What minecraft version will the server be?\n")

response = requests.get("https://api.papermc.io/v2/projects/paper/versions/" + verson)

#Download the selected minecraft version

def manualOs():
    manualOs = input("Does your computer use .sh(linux/unix/mac) or .bat(windows) scripts?\n[.sh/.bat] ")
    if manualOs == ".sh":
        script = "bash"
    elif manualOs == ".bat":
        script = "windows"
    else:
        print("You will have to manually set up the server from here. Your os is not supported")
def download():
    # Get the save path from the user
   savePath = input("Where do you want to save your minecraft folder? \nPress enter to save into the current directory or type desktop to save it to your desktop\n")
   if savePath == "desktop":
       savePath = "~/Desktop"
   savePath = os.path.expanduser(savePath)
   if savePath == '':
       savePath = '.'

   response = requests.get("https://api.papermc.io/v2/projects/paper/versions/" + verson + "/builds/" + str(latestBuild) + "/downloads/paper-" + verson + "-" + str(latestBuild) + ".jar")
   if response.status_code == 200:
       if os.path.exists(savePath + "/Server"):
           print("The server will be saved in " + savePath + "/Server")
       else:
           if not os.path.exists(savePath):
            os.makedirs(savePath)
           os.makedirs(savePath + "/Server")
           print("The directory was created successfully and the server will be saved in " + savePath + "/Server")
           os.chdir(savePath + "/Server/")
       with open("server.jar", "wb") as f:
        f.write(response.content)
        print("Minecraft server files downloaded!")
        setup()
   else:
       print("ERROR: ", response.status_code)

def setup():
    print("Now we will start setting up the server!")
    if sys.platform.startswith('win'):
        script = "windows"
        if not input("We detected you're running windows so we will make a batch script. Is this correct?\n[y/n] ") == "y":
            manualOs()
    elif sys.platform.startswith('linux'):
        script = "bash"
        if not input("We detected you're running linux so we will make a bash script. Is this correct?\n[y/n] ") == "y":
            manualOs()
    elif sys.platform.startswith('darwin'):
        script = "bash"
        if not input("We detected you're running OSX so we will make a bash script. Is this correct?\n[y/n] ") == "y":
            manualOs()
    else:
        manualOs()
    while True:
        if input("Do you accept the minecraft EULA (https://aka.ms/MinecraftEULA)?\n[Y/N] ").lower() == "y":
            with open("eula.txt", "w") as f:
                f.write("#EULA accepted by user with MinecraftServerMaker.py\n#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\neula=true")
                break
        else:
            print("To continue you have to accept the EULA by pressing y")

    ram = input("How much ram do you want to give to the server? (ex. 2G = 2 Gigabytes and 2M = 2 Megabytes\n")
    if script == "bash":
        with open("run.sh", "w") as f:
            f.write("#!/bin/bash\njava -Xmx" + ram + " -Xms" + ram + " -jar server.jar\necho \"Server off. Press enter to close\" \nread")
        os.chmod("run.sh", 0o755)
    if script == "windows":
        with open("run.bat", "w") as f:
            f.write("java -Xmx" + ram + " -Xms" + ram + " -jar server.jar\npause")


#Find the latest build of the selected minecraft version
if response.status_code == 200:
    data = response.json()
    latestBuild = data["builds"][-1]
    download()
    response = requests.get("https://api.papermc.io/v2/projects/paper/versions/" + verson)
else: print("ERROR " + response.status_code + "\nThat version of minecraft was probably either entered wrong, doesn't exist, or is not available yet")