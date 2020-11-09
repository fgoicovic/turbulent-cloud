from __future__ import print_function

from numpy import sum, mean, sqrt, cross
from numpy import array, isnan, newaxis
from numpy.linalg import norm
import warnings
warnings.filterwarnings('ignore')

class Rotation:
    """ Class for setting rotational energy to a set of particles.
        Some modes/noise may appear when setting a LARGE beta value.
        This method efficiency scales as ~ alpha/(alpha+beta), so we
        rescale beta if necessary.

        Arguments:
           beta : ratio of rotational energy to the magnitude of
                  gravitational energy.
           alpha: ratio of turbulent energy to the magnitude of
                  gravitational energy.
           epot : magnitude of gravitational energy.
    """
    def __init__(self, beta=-1, alpha=0.5, epot=1):

        if beta >= alpha: # impossible
            print("Beta must be lower than alpha. Exiting")
            exit()

        elif beta == -1:  # nothing to do here
            self.erot = None

        else:           # we rescale beta for this method
            print("Adding rotational energy with beta~{}".\
                   format(beta))
            if beta/alpha < 0.1: # linear range
                self.erot = epot*beta
            else:                # scaling range
                self.erot = epot*alpha*beta/float(alpha-beta)

    def add_rotation(self, pos, vel, mass):

        if self.erot is None: return vel #nothing to do here

        # we set rotational energy according to beta
        # first we calculate the desired angular velocity
        Iz      = sum(mass * (pos[:,0]**2 + pos[:,1]**2))
        omega_d = sqrt(2*self.erot/Iz)

        # now we measure the existing mean angular velocity
        v2      = sum(vel**2, axis=1)
        radii2  = sum(pos**2, axis=1)
        sec2    = mean(sum(cross(array([0,0,1]),
                                    pos/radii2[:,newaxis])**2, axis=1))

        omega_e = mean(cross(pos, vel) / radii2[:,newaxis], axis=0)*sec2

        # we add the new and subtract the old angular velocity
        vel += cross(array([0,0,omega_d]) - omega_e, pos)

        # we re-normalize the velocities to preserve alpha relation
        # to do so, we measure the ratio ekin_old/ekin_new and
        # distribute it over all particles
        vel2  = sum(vel**2, axis=1)
        ratio = sum(v2)/sum(vel2)

        # in order not to affect omega, re-escale only vz if possible,
        # else the whole vector
        factor       = sqrt((ratio * vel2 - vel[:,0]**2 - vel[:,1]**2)\
                            / vel[:,2]**2)
        nan          = isnan(factor)
        vel[~nan,2] *= factor[~nan]       # possible
        vel[nan]    *= sqrt(ratio)        # not possible

        return vel
