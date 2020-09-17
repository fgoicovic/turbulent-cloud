from __future__ import print_function

from numpy import mean, sqrt, cross, array, isnan, newaxis
from numpy.linalg import norm 
  
class Rotation:
    """ Class for setting rotational energy to a 3-D set of particles.
        This method efficiency scales as ~ alpha/(alpha+beta).
        Some modes/noise may appear when setting a large beta value.
        Arguments:
           beta : Ratio of rotational energy to the magnitude of
                  gravitational energy.
           alpha: Ratio of turbulent energy to the magnitude of
                  gravitational energy.
           epot : Magnitude of gravitational energy.
    """
    def __init__(self, beta=0, alpha=0.5, epot=1):

        if beta>=alpha: # impossible
            print("WARNING: Can't apply new rotational energy\n" +\
                    "          beta must be lower than alpha.")
            self.erot  = None

        elif beta==-1: # nothing to do here
            self.erot = None

        else: # we re-escale beta for this method
            self.erot  = epot*alpha*beta/float(alpha-beta)

    def add_rotation(self, pos, vel, mass, erot):

        if erot is None: return vel #nothing to do here

        print("Adding rotational energy to particles.")
        # we set rotational energy according to beta
        # first we calculate the desired angular velocity
        Iz      = np.sum(mass * (pos[:,0]**2 + pos[:,1]**2))
        omega_d = sqrt(2*erot/Iz)

        # now we measure the existing mean angular velocity
        v2      = norm(vel, axis=1)**2
        radii2  = norm(pos, axis=1)**2
        sec2    = mean(norm(cross(array([0,0,1]),
                                    pos/radii2[:,newaxis]), axis=1)**2)
        omega_e = mean(cross(pos, vel) / radii2[:,newaxis], axis=0)*sec2

        # we add the new and subtract the old angular velocity
        vel += cross(array([0,0,omega_d]) - omega_e, pos)

        # we re-normalize the velocities to preserve alpha relation
        # to do so, we measure the ratio ekin_old/ekin_new and
        # distribute it over all particles
        ratio = np.sum(v2)/np.sum(vel**2)

        # in order not to affect omega, re-escale only vz if possible,
        # else the whole vector
        factor       = sqrt((ratio * np.sum(vel**2, axis=1) \
                            - vel[:,0]**2 - vel[:,1]**2) / vel[:,2]**2)
        nan          = isnan(factor)
        vel[~nan,2] *= factor[~nan]       # possible
        vel[nan]    *= sqrt(ratio)        # not possible

        return vel
