import re
import subprocess
import time
import os
import os.path


class SSH:
    def __init__(self):
        self.logfile_name = ""
        self.command = ""
        self.remote_port = ""
        self.local_port = ""
        self.pattern = ""
        self.name = ""
    
    def getURL(self,localhost=False):
        try:
            if localhost:
                return None
            while  True:
                if not self.logfile_exists():
                    continue
                with open(self.logfile_name) as f:
                    data = f.read()
                    f.close()
                output = data
                if output:
                    url_pattern = re.compile(self.pattern)
                    match = url_pattern.search(output)
                    if match:
                        #quick fix will improve later or you can be the contributor here if you solve the logic
                        if self.name == "Serveo":
                            return match.group(1)
                        else:
                            return match.group(0)
                else:
                    continue
        except Exception as e:
            print(f"An error occurred while fetching the Serveo URL: {e}")
        
        return None

    def start_service(self,command):
        try:
            # Construct the SSH command for Serveo
            # command = f'ssh -T -R {self.remote_port}:localhost:{self.local_port} serveo.net > ssh_tunnel.log 2>&1'
            process = subprocess.Popen(command,shell=True,stdout=subprocess.DEVNULL)
            return process
        except Exception as e:
            print(f"An error occurred while starting the Serveo tunnel: {e}")
            return None
    
    def logfile_exists(self):
        if os.path.exists(self.logfile_name):
            return True
        else:
            return False
    
    def delete_logfile(self):
        if os.path.exists(self.logfile_name):
            os.remove(self.logfile_name)
            return True
        return True
    

class HOSTING(SSH):

    def __init__(self):
        super().__init__()
        


    def start_serveo(self,local_port):
        self.logfile_name = "automation/logfile_serveo.log"
        self.local_port = local_port
        self.command = f'ssh -T -R 80:localhost:{self.local_port} serveo.net > {self.logfile_name} 2>&1'
        self.pattern = r"Forwarding HTTP traffic from (https?://\S+)"
        self.name = "Serveo"
        self.delete_logfile()
        process = self.start_service(self.command)
        print("Tunnel Started")
        return process
    
    def start_localhost(self,local_port):
        self.logfile_name = "automation/logfile_localhost.log"
        self.local_port = local_port
        self.command = f'ssh -T -R 80:localhost:{self.local_port} nokey@localhost.run > {self.logfile_name} 2>&1'
        self.pattern = r"https:\/\/[a-zA-Z0-9.-]+\.lhr\.life"
        self.name = "Localhost.run"
        self.delete_logfile()
        process = self.start_service(self.command)
        return process
    
        
    
    

        

    
    
            
if __name__ == "__main__":
    s = HOSTING()
    process = s.start_localhost(8000)
    url = s.getURL()
    print(f"Url is {url}")
    while process.poll() is None:
        try:
            print("Process is Running")
            time.sleep(5)
        except KeyboardInterrupt:
            process.kill()
            print("\nClosing Serveo..")
    
    

