import socket
import math

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
        b = bytes(f"MoveAbsJ {theta[0]:.3f} {theta[1]:.3f} {theta[2]:.3f} {theta[3]:.3f} {theta[4]:.3f} {theta[5]:.3f}\r\n", 'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)
        return data

    def moveJ(self, x, r, theta, velocity, zone):
        return self.__move("MoveJ", x, r, theta, velocity, zone)

    def moveL(self, x, r, theta, velocity, zone):
        return self.__move("MoveL", x, r, theta, velocity, zone)

    def egmMoveL(self, x, r, theta, velocity, zone):
        return self.__move("EGM", x, r, theta, velocity, zone)

    def __move(self, command, x, r, theta, velocity, zone):
        quaternion = [1.0, 0.0, 0.0, 0.0]
        add = 0
        if len(r) == 3:
            qs = math.sqrt(r[0][0]+r[1][1]+r[2][2]+1)/2.0
            kx = r[2][1]-r[1][2]
            ky = r[0][2]-r[2][0]
            kz = r[1][0]-r[0][1]
            if r[0][0] >= r[1][1] and r[0][0] >= r[2][2]:
                kx1 = r[0][0]-r[1][1]-r[2][2]+1
                ky1 = r[1][0]+r[0][1]
                kz1 = r[2][0]+r[0][2]
                if kx >= 0:
                    add = 1
            elif r[1][1] >= r[2][2]:
                kx1 = r[1][0]+r[0][1]
                ky1 = r[1][1]-r[0][0]-r[2][2]+1
                kz1 = r[2][1]+r[1][2]
                if ky >= 0:
                    add = 1
            else:
                kx1 = r[2][0]+r[0][2]
                ky1 = r[2][1]+r[1][2]
                kz1 = r[2][2]-r[0][0]-r[1][1]+1
                if kz >= 0:
                    add = 1
            if add > 0:
                kx = kx+kx1
                ky = ky+ky1
                kz = kz+kz1
            else:
                kx = kx-kx1
                ky = ky-ky1
                kz = kz-kz1
            norm = math.sqrt(kx*kx+ky*ky+kz*kz)
            if norm > 0:
                s = math.sqrt(1.0-qs*qs)/norm
                quaternion = [qs, s*kx, s*ky, s*kz]
        else:
            quaternion = r
        quadrant = [round((theta[0]-44)/90), round((theta[3]-44)/90), round((theta[5]-44)/90), 0]
        if theta[4] < 0.0:
            quadrant[3] = 1
        if velocity < 10:
            velocity = 10
        elif velocity > 2000:
            velocity = 2000
        if zone < 0:
            zone = 0
        elif zone > 100:
            zone = 100
        b = bytes(f"{command} {x[0]:.2f} {x[1]:.2f} {x[2]:.2f} {quaternion[0]:.5f} {quaternion[1]:.5f} {quaternion[2]:.5f} {quaternion[3]:.5f} {quadrant[0]:d} {quadrant[1]:d} {quadrant[2]:d} {quadrant[3]:d} {velocity:d} {zone:d}\r\n", 'utf-8')
        self.s.sendall(b)
        data = self.s.recv(1024)
        return data
