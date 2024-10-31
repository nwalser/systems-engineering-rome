import socket

PORT = 8400  # the port used by the server

"""control an ABB robot with Python"""
class OmniCore:
    def __init__(self, ipAddress):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ipAddress, PORT))
        self.s.settimeout(60.0)

    def __del__(self):
        b = bytes("Close\r\n", 'utf-8')
        self.s.sendall(b)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def home(self):
        b = bytes("Home\r\n", 'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)

        return data

    def moveAbsJ(self, theta):
        b = bytes(f"MoveAbsJ {theta[0]:.3f} {theta[1]:.3f} {theta[2]:.3f} "
                  f"{theta[3]:.3f} {theta[4]:.3f} {theta[5]:.3f}\r\n", 'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)
        return data

    def moveL(self, position, orientation, configuration):
        b = bytes(f"MoveL {position[0]:.3f} {position[1]:.3f} {position[2]:.3f} "
                  f"{orientation[0]:.6f} {orientation[1]:.6f} {orientation[2]:.6f} {orientation[3]:.6f} "
                  f"{configuration[0]:.0f} {configuration[1]:.0f} {configuration[2]:.0f} {configuration[3]:.0f}\r\n", 
                  'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)
        return data
