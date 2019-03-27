from __future__ import print_function

import numpy as np
from libs.turbulence import VelocityGrid
from libs.uniform_sphere import Sphere
from libs.const import G, msol, parsec
from libs.utils import save_particles
from libs.options_parser import OptionsParser


if __name__ == "__main__":

    op = OptionsParser()
    args = op.get_args()

    Mcloud = args.mass * msol
    Rcloud = args.radius * parsec
    N = args.num
    print("We want {:d} gas cells to represent the cloud".format(N))

    # where we want to place the cloud's center of mass
    r_com = np.array([0.,0.,0.])

    # first, determine position of particles given total number of
    # desired cells
    cloud = Sphere(N=N, center=r_com, radius=Rcloud)
    dx = cloud.dx

    pos = cloud.pos
    Ngas = cloud.Npart
    mpart = Mcloud / Ngas
    mass = np.full(Ngas, mpart)
    ids = np.arange(1, Ngas+1)
    u = np.zeros(Ngas)
    vel = np.zeros((Ngas, 3))

    # produce the velocity grid for turbulent ICs
    vg = VelocityGrid(xmax=2*Rcloud, dx=dx, npow=args.npow, ngrid=args.ngrid)
    vg.coordinate_grid(xstart=r_com[0]-Rcloud, xend=r_com[0]+Rcloud)
    print("Adding turbulent velocity to particles.")
    vel = vg.add_turbulence(pos=pos, vel=vel)

    # now we need to normalize the velocity values
    # we do it such that the cloud is marginally bound
    v2 = np.linalg.norm(vel, axis=1)**2
    Ekin = np.sum(0.5*mpart*v2)
    Epot = 3./5. * G * Mcloud**2 / Rcloud
    Avel = np.sqrt(Epot/(2*Ekin))
    vel *= Avel

    print("Writing output file {}...".format(args.outfile))
    save_particles(ids, pos, vel, mass, u, args.outfile, args.format)

    print("done...bye!")






