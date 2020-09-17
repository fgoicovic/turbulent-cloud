from __future__ import print_function

import numpy as np
from libs.turbulence import VelocityGrid
from libs.uniform_sphere import Sphere
from libs.rotation import Rotation
from libs.const import G, msol, parsec
from libs.utils import save_particles
from libs.options_parser import OptionsParser


if __name__ == "__main__":

    op     = OptionsParser()
    args   = op.get_args()

    mcloud = args.mass * msol
    rcloud = args.radius * parsec
    n      = args.num
    print("We want {:d} gas cells to represent the cloud".format(n))

    # where we want to place the cloud's center of mass
    r_com = np.array([0.,0.,0.])

    # first, determine position of particles given total number of
    # desired cells
    cloud = Sphere(n=n, center=r_com, radius=rcloud)
    dx    = cloud.dx

    pos   = cloud.pos
    ngas  = cloud.npart
    mpart = mcloud / ngas
    mass  = np.full(ngas, mpart)
    ids   = np.arange(1, ngas+1)
    u     = np.zeros(ngas)
    vel   = np.zeros((ngas, 3))

    # produce the velocity grid for turbulent ICs
    vg = VelocityGrid(xmax=2*rcloud, dx=dx, npow=args.npow, ngrid=args.ngrid)
    vg.coordinate_grid(xstart=r_com[0]-rcloud, xend=r_com[0]+rcloud)
    print("Adding turbulent velocity to particles.")
    vel = vg.add_turbulence(pos=pos, vel=vel)

    # now we need to normalize the velocity values
    # we do it according to the alpha value
    vtur = vel - np.mean(vel, axis=0)
    vt2  = np.linalg.norm(vtur, axis=1)**2
    etur = np.sum(0.5*mpart*vt2)
    epot = 3./5. * G * mcloud**2 / rcloud
    kvel = np.sqrt(args.alpha*epot/etur)
    vel *= kvel

    # we manually add rotation if desired
    rot = Rotation(beta=args.beta, alpha=args.alpha, epot=epot)
    vel = rot.add_rotation(pos=pos, vel=vel, mass=mass)


    print("Writing output file {}...".format(args.outfile))
    save_particles(ids, pos, vel, mass, u, args.outfile, args.format, args.units)

    print("done...bye!")
