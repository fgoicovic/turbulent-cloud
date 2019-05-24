from __future__ import print_function

from sys import exc_info, exit
import numpy as np
from logging import warning
from struct import pack

def save_particles(ids, pos, vel, mass, u, outfile, format):

    N = len(pos)

    if format == 0:
        # Openning file
        try:
            ofile = open(outfile,'w')
        except IOError as e:
            msg = "IO Error({0}): {1}".format(e.errno, e.strerror)
            warning(msg)
        except:
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise

        id_space = len("{}".format(N))

        # Preparing every line to print to the file
        for i in range(N):
            # Formatting particle attributes
            ie = '% d' % ids[i]
            me = '% 3.8e' % mass[i]
            rx = '% 3.8e' % pos[i][0]
            ry = '% 3.8e' % pos[i][1]
            rz = '% 3.8e' % pos[i][2]
            vx = '% 3.8e' % vel[i][0]
            vy = '% 3.8e' % vel[i][1]
            vz = '% 3.8e' % vel[i][2]
            ue = '% 3.8e' % u[i]

            # Right-align the strings
            outstring = "{0} {1} {2} {3} {4} {5} {6} {7} {8}\n".\
                         format( ie.rjust(id_space),\
                                 me.rjust(12),\
                                 rx.rjust(12),\
                                 ry.rjust(12),\
                                 rz.rjust(12),\
                                 vx.rjust(12),\
                                 vy.rjust(12),\
                                 vz.rjust(12),\
                                 ue.rjust(12))
            # Write to file
            ofile.write(outstring)

        # Closing the file
        ofile.close()

    elif format == 1:
        Ngas = len(mass)
        Npart = np.array([Ngas, 0, 0, 0, 0, 0])
        Nmass = np.array([mass[0], 0, 0, 0, 0, 0])
        # Linearizing the 3D-array of the position and velocity
        pos = pos.ravel()
        vel = vel.ravel()

        dummy = np.zeros(Npart[0])
        time = 0.
        redshift = 0.0  # double
        flag_sfr = 0  # long
        flag_feedback = 0  # long
        bytesleft = 256 - 6*4 - 6*8 - 8 - 8 - 2*4 - 6*4
        fill = np.zeros(int(bytesleft/4.0), dtype=np.int)  # int

        with open(outfile, 'wb') as f:
            nbytes = 256
            # Header
            f.write(pack('i', nbytes))
            f.write(pack('i' * len(Npart), *Npart))
            f.write(pack('d' * len(Nmass), *Nmass))
            f.write(pack('d', time))
            f.write(pack('d', redshift))
            f.write(pack('i', flag_sfr))
            f.write(pack('i', flag_feedback))
            f.write(pack('i' * len(Npart), *Npart))
            f.write(pack('i' * len(fill), *fill))
            f.write(pack('i', nbytes))

            # Positions
            nbytes = int(len(pos) * 4)
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(pos), *pos))
            f.write(pack('i', nbytes))

            # Velocities
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(vel), *vel))
            f.write(pack('i', nbytes))

            # Ids
            nbytes = int(len(ids) * 4)
            f.write(pack('i', nbytes))
            f.write(pack('i' * len(ids), *ids))
            f.write(pack('i', nbytes))

            # Masses
            nbytes = len(mass) * 4
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(mass), *mass))
            f.write(pack('i', nbytes))

            # Energy
            nbytes = len(u) * 4
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(u), *u))
            f.write(pack('i', nbytes))

    elif format == 2:
        Ngas = len(mass)
        Npart = np.array([Ngas, 0, 0, 0, 0, 0])
        Nmass = np.array([mass[0], 0, 0, 0, 0, 0])
        # Linearizing the 3D-array of the position and velocity
        pos = pos.ravel()
        vel = vel.ravel()

        dummy = np.zeros(Npart[0])
        time = 0.
        redshift = 0.0  # double
        flag_sfr = 0  # long
        flag_feedback = 0  # long
        bytesleft = 256 - 6*4 - 6*8 - 8 - 8 - 2*4 - 6*4
        fill = np.zeros(int(bytesleft/4.0), dtype=np.int)  # int


        with open(outfile, 'wb') as f:
            
            nbytes  = 256
            nbytes4 = 8
            
            f.write(pack('i', nbytes4))
            f.write(b'HEAD')
            f.write(pack('i', nbytes + 8))
            f.write(pack('i', nbytes4))
            # Header
            
            f.write(pack('i', nbytes))
            f.write(pack('i' * len(Npart), *Npart))
            f.write(pack('d' * len(Nmass), *Nmass))
            f.write(pack('d', time))
            f.write(pack('d', redshift))
            f.write(pack('i', flag_sfr))
            f.write(pack('i', flag_feedback))
            f.write(pack('i' * len(Npart), *Npart))
            f.write(pack('i' * len(fill), *fill))
            f.write(pack('i', nbytes))

            # Positions
            nbytes = int(len(pos) * 4)
            f.write(pack('i', nbytes4))
            f.write(b'POS ')
            f.write(pack('i', nbytes + 8))
            f.write(pack('i', nbytes4))
            
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(pos), *pos))
            f.write(pack('i', nbytes))

           # Velocities
            f.write(pack('i', nbytes4))
            f.write(b'VEL ')
            f.write(pack('i', nbytes + 8))
            f.write(pack('i', nbytes4))
            
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(vel), *vel))
            f.write(pack('i', nbytes))

            # Ids
            nbytes = int(len(ids) * 4)
            f.write(pack('i', nbytes4))
            f.write(b'ID  ')
            f.write(pack('i', nbytes + 8))
            f.write(pack('i', nbytes4))

            f.write(pack('i', nbytes))
            f.write(pack('i' * len(ids), *ids))
            f.write(pack('i', nbytes))

            # Masses
            nbytes = int(len(mass) * 4)
            f.write(pack('i', nbytes4))
            f.write(b'MASS')
            f.write(pack('i', nbytes+8))
            f.write(pack('i', nbytes4))
            
            f.write(pack('i', nbytes))
            f.write(pack('f' * len(mass), *mass))
            f.write(pack('i', nbytes))

            # Energy
            nbytes = int(len(u) * 4)
            f.write(pack('i', nbytes4))
            f.write(b'U   ')
            f.write(pack('i', nbytes + 8))
            f.write(pack('i', nbytes4))

            f.write(pack('i', nbytes))
            f.write(pack('f' * len(u), *u))
            f.write(pack('i', nbytes))

    else:
        print("Format {} unknown or not implemented. Exiting.".format(format))
        exit()
