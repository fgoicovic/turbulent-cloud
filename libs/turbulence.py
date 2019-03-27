from __future__ import print_function

from sys import exit
import numpy as np
from time import time
from scipy.interpolate import RegularGridInterpolator

class VelocityGrid:
    """ Class for creating a 3-D grid with turbulent velocity field.
        The velocities are produced from a Gaussian random distribution
        with a given power spectrum.
        Each velocity component is sampled in Fourier space, and then
        transformed back to real space.
        Based on Dubinski et al. (1995).

        Arguments:
           npow: power index of spectrum.
           N: number of grid points per dimension (must be even).
           xmax: outer scale of turbulence.
           dx: physical separation between neighboring points.
           seed: number that determines the random realization.
    """

    def __init__(self, npow=4., ngrid=256, xmax=1., dx=0.01, seed=27021987):

        start = time()
        print("Creating 3-D velocity grid with power spectrum P_k~k**{0}".\
              format(npow))

        if ngrid % 2 != 0:
            print("Grid points must be an even number. Exiting.")
            exit()
        Nc = int(ngrid/2) + 1

        kmax = 2*np.pi/dx
        kmin = 2*np.pi/xmax

        kx = np.fft.fftfreq(ngrid, d=1/(2*kmax))
        ky = kx
        kz = np.fft.rfftfreq(ngrid, d=1/(2*kmax))

        # we produce a 3-D grid of the Fourier coordinates
        kxx, kyy, kzz = np.meshgrid(kx, ky, kz, indexing='ij', sparse=True)
        kk = kxx*kxx + kyy*kyy + kzz*kzz + kmin**2

        np.random.seed(seed)

        # we sample the components of a vector potential, as we want
        # an incompresible velocity field
        xi1 = np.random.random(size=kk.shape)
        xi2 = np.random.random(size=kk.shape)
        C = kk**(-(npow+2.)/4.)*np.sqrt(-np.log(1-xi1))
        phi = 2*np.pi*xi2
        Akx = C*np.exp(1j*phi)
        xi1 = np.random.random(size=kk.shape)
        xi2 = np.random.random(size=kk.shape)
        C = kk**(-(npow+2.)/4.)*np.sqrt(-np.log(1-xi1))
        phi = 2*np.pi*xi2
        Aky = C*np.exp(1j*phi)
        xi1 = np.random.random(size=kk.shape)
        xi2 = np.random.random(size=kk.shape)
        C = kk**(-(npow+2.)/4.)*np.sqrt(-np.log(1-xi1))
        phi = 2*np.pi*xi2
        Akz = C*np.exp(1j*phi)

        new_shape=Akx.shape+(3,)
        kv = np.zeros(new_shape, dtype=Akx.dtype)
        kv[:,:,:,0] = 1j*kxx
        kv[:,:,:,1] = 1j*kyy
        kv[:,:,:,2] = 1j*kzz
        Ak = np.zeros(new_shape, dtype=Akx.dtype)
        Ak[:,:,:,0] = Akx
        Ak[:,:,:,1] = Aky
        Ak[:,:,:,2] = Akz

        # the velocity vector in Fourier space is obtained by
        # taking the curl of A, which is ik x A
        vk = np.cross(kv, Ak)

        self.ngrid = ngrid
        self.vx = np.fft.irfftn(vk[:,:,:,0])
        self.vy = np.fft.irfftn(vk[:,:,:,1])
        self.vz = np.fft.irfftn(vk[:,:,:,2])

        print("\nInverse Fourier Transform took {:g}s.\n".format(time()-start))


    def coordinate_grid(self, xstart=0., xend=1.):
        self.x = np.linspace(xstart, xend, self.ngrid)


    def add_turbulence(self, pos, vel):

        pos = np.array(pos).reshape(-1,3)
        vel = np.array(pos).reshape(-1,3)

        if not hasattr(self, 'x'):
            self.coordinate_grid()
        x  = self.x
        vx = self.vx
        vy = self.vy
        vz = self.vz

        interp_func_x = RegularGridInterpolator((x,x,x), vx)
        interp_func_y = RegularGridInterpolator((x,x,x), vy)
        interp_func_z = RegularGridInterpolator((x,x,x), vz)
        vx = interp_func_x(pos)
        vy = interp_func_y(pos)
        vz = interp_func_z(pos)

        vel[:,0] += vx
        vel[:,1] += vy
        vel[:,2] += vz

        return vel







