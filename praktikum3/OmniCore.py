class OmniCore:
    
    """control an ABB robot with Python"""

    def __init__(self, ipAddress):

        import socket
        PORT = 8400  # the port used by the server
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ipAddress, PORT))
        self.s.settimeout(10.0)

    def __del__(self):

        import socket
        
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
        
        b = bytes(f"MoveAbsJ {theta[0]:.3f} {theta[1]:.3f} {theta[2]:.3f} {theta[3]:.3f} {theta[4]:.3f} {theta[5]:.3f}\r\n", 'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)
        
        return data
