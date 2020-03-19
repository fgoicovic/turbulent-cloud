from __future__ import print_function

from numpy import pi
from numpy import floor, array, mgrid, concatenate, where
from numpy import linalg

class Sphere:
    """ Class for creating a uniform distribution of particles in a close-packed
        sphere.

        Arguments:
            n: total number of desired points to represent the sphere
            center: coordinates of the sphere's center (with units)
            radius: sphere's radius (with units)
    """
    def __init__(self, n=10000, center=[0.,0.,0.], radius=1.):

        # first we create a cube with uniform distribution, hence we need to sample
        # more particles than the desired N
        side   = 2*radius
        ncube  = 6/pi * n # 6/pi is the ratio between sphere and cube volume
        nside  = int(floor((ncube/4.)**(1./3)))
        naux   = nside**3

        h      = side / nside
        center = array(center)
        start  = center-radius

        z3     = mgrid[0:nside, 0:nside, 0:nside].T.reshape(naux, 3)
        grid   = (concatenate((z3, z3+[0.5, 0.5, 0], z3+[0, 0.5, 0.5],
                  z3+[0.5, 0, 0.5])) + 0.25)/nside * side

        pos    = start + grid
        r      = linalg.norm(pos, axis=1)

        ig     = where(r <= radius)[0]
        pos    = pos[ig]
        npart  = len(ig)
        print("We placed {:d} gas cells in a close-packed sphere.".format(npart))

        self.npart  = npart
        self.dx     = h
        self.pos    = pos
        self.r      = radius
        self.center = center




