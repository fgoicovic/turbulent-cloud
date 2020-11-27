from __future__ import print_function

from numpy import pi, sum, max, min, log, exp
from numpy import diff, where, unique, argsort
from numpy import array, full, linspace, mgrid
from numpy import transpose, append, digitize
from numpy import concatenate
from numpy.linalg import norm

class Sphere:
    """ Class for creating a distribution of particles in a close-packed
        sphere.

        Arguments:
            n     : total number of desired points to represent the sphere
            center: coordinates of the sphere's center (with units)
            radius: sphere's radius (with units)
            mass  : sphere's mass   (with units)
    """
    def __init__(self, n=10000, center=[0.,0.,0.], radius=1., mass=1.):

        # first we create a cube with uniform distribution, hence we need to sample
        # more particles than the desired N
        side   = 2*radius
        ncube  = 6/pi * n # 6/pi is the ratio between sphere and cube volume
        nside  = int((ncube/4.)**(1./3))
        naux   = nside**3

        h      = side / nside * 0.5 # min particle separation
        center = array(center)

        z3     = mgrid[0:nside, 0:nside, 0:nside].T.reshape(naux, 3)
        grid   = (concatenate((z3, z3+[0.5, 0.5, 0], z3+[0, 0.5, 0.5],
                  z3+[0.5, 0, 0.5])) + 0.25)/nside * side

        pos    = grid - radius
        r      = norm(pos, axis=1)

        ig     = where(r <= radius)[0]
        pos    = pos[ig] + center
        npart  = len(ig)
        masses = full(npart, mass / float(npart)) # uniform masses
        print("We placed {:d} gas cells in a close-packed sphere.".format(npart))

        self.npart  = npart
        self.dx     = h
        self.pos    = pos
        self.r      = radius
        self.center = center
        self.mass   = masses


    def add_profile(self, gamma=0, method=2):
        """ Function for setting a radial density profile to a uniform
            sphere of particles.

            Arguments:
                gamma : power index of radial density distribution
                method: method to be implemented
                        1: The profile is created by redistributing the
                           particles positions, considering they have equal
                           mass. In consecuence, a spherical gap may appear
                           at the center if gamma > 0.
                        2: The profile is created by redistributing the
                           particles masses, without modifying their positions.
                           In consecuence, final total mass may be slightly
                           smaller than preset if npart is small.
        """

        if gamma <= -3:   # impossible
            print("Gamma must be greater than -3. Exiting")
            exit()

        elif gamma != 0:
            print("Setting radial density profile with "+\
                        "RHO~r**{}".format(gamma))

            # we use centered transpose of pos
            pos  = transpose(self.pos - self.center)

            if method == 1:

                # redistribute particles uniformingly along radius
                pos *= sum(pos**2, axis=0)

                # redistribute particles according to gamma
                pos *= norm(pos, axis=0)**(1/float(3 + gamma) - 1)

                # normalize radii according to radius
                pos *= self.r / max(norm(pos, axis=0))

                # new min separation
                dx = min(diff(unique(pos[0])))

                self.pos  = transpose(pos) + self.center
                self.dx   = dx


            elif method == 2:

                # get radii and sort particles
                radii   = norm(pos, axis=0)
                order   = argsort(radii)
                pos     = pos[:,order]
                radii   = radii[order]

                # normalization cte
                cte     = (gamma + 3) * log(self.r) - log(sum(self.mass))

                # radial bins
                eps     = 1e-5
                nbins   = int( (radii[-1] - radii[0]) /
                                max(diff(unique(radii))) )
                bins    = linspace(min(radii) * (1 + eps),
                                 max(radii) * (1 + eps), nbins)

                # cumulative mass per bin
                CM_b    = bins ** (gamma + 3) * exp(-cte)

                # mass per bin
                M_b     = append(CM_b[0], diff(CM_b))

                # particles bin's index
                Pb_ind  = digitize(radii, bins)

                # particles per bin
                _, NP_b = unique(Pb_ind, return_counts=True)

                # particles's mass per bin
                PM_b    = M_b/NP_b

                # distribute mass
                masses  = PM_b[Pb_ind]

                self.pos  = transpose(pos) + self.center
                self.mass = masses
