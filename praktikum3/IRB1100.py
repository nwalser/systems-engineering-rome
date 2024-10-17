#!/usr/bin/env python

import os
import numpy as np
import roboticstoolbox as rtb

class IRB1100(rtb.robot.Robot):
    
    """ Class that imports an ABB IRB 1100 URDF model """

    def __init__(self):

        links, name, urdf_string, urdf_filepath = self.URDF_read(os.getcwd()+"/IRB1100/irb1100.urdf", os.getcwd()+"/IRB1100")

        super().__init__(
            links,
            name = name,
            manufacturer = "ABB",
            urdf_string = urdf_string,
            urdf_filepath = urdf_filepath,
        )

        self.qr = np.array([0, 0, 0, 0, np.pi/4, 0])
        self.qz = np.zeros(6)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

if __name__ == "__main__":  # pragma nocover

    irb1100 = IRB1100()
    print(irb1100)
