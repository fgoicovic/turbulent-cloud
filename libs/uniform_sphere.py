from __future__ import print_function

import numpy as np

class Sphere:
    """ Class for creating a uniform distribution of particles in a close-packed
        sphere.

        Arguments:
            N: total number of desired points to represent the sphere
            center: coordinates of the sphere's center (with units)
            radius: sphere's radius (with units)
    """
    def __init__(self, N=10000, center=[0.,0.,0.], radius=1.):

        # first we create a cube with uniform distribution, hence we need to sample
        # more particles than the desired N
        side = 2*radius
        Ncube = 6/np.pi * N # 6/pi is the ratio between sphere and cube volume
        Nside = int(np.floor((Ncube/4.)**(1./3)))
        Naux = Nside**3

        h = side / Nside
        center = np.array(center)
        start = center-radius

        z3 = np.mgrid[0:Nside, 0:Nside, 0:Nside].T.reshape(Naux, 3)
        grid = (np.concatenate((z3, z3+[0.5, 0.5, 0], z3+[0, 0.5, 0.5],
                z3+[0.5, 0, 0.5])) + 0.25)/Nside * side

        pos = start + grid
        r = np.linalg.norm(pos, axis=1)

        ig = np.where(r <= radius)[0]
        pos = pos[ig]
        Npart = len(ig)
        print("We placed {:d} gas cells in a close-packed sphere.".format(Npart))

        self.Npart  = Npart
        self.dx     = h
        self.pos    = pos
        self.r      = radius
        self.center = center




