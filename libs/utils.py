from __future__ import print_function

from sys import exc_info
import numpy as np

def save_particles(pos, vel, mass, outfile):

    # Openning file
    try:
        ofile = open(outfile,'w')
    except IOError as e:
        msg = "IO Error({0}): {1}".format(e.errno, e.strerror)
        logging.warning(msg)
    except:
        print("Unexpected error: {}".format(exc_info()[0]))
        raise

    ofile.write("# {0} {1} {2} {3} {4} {5} {6}\n".format( 'm'.ljust(14),
                                                          'x'.ljust(15),
                                                          'y'.ljust(15),
                                                          'z'.ljust(15),
                                                          'vx'.ljust(15),
                                                          'vy'.ljust(15),
                                                          'vz') )

    # Preparing every line to print to the file
    for i in range(len(pos)):
        # Formatting particle attributes
        m  = '%+3.8e' % mass[i]
        rx = '%+3.8e' % pos[i][0]
        ry = '%+3.8e' % pos[i][1]
        rz = '%+3.8e' % pos[i][2]
        vx = '%+3.8e' % vel[i][0]
        vy = '%+3.8e' % vel[i][1]
        vz = '%+3.8e' % vel[i][2]

        # Right-align the strings
        outstring = "{0} {1} {2} {3} {4} {5} {6}\n".format( m.rjust(12),\
                                                            rx.rjust(12),\
                                                            ry.rjust(12),\
                                                            rz.rjust(12),\
                                                            vx.rjust(12),\
                                                            vy.rjust(12),\
                                                            vz.rjust(12)
                                                           )
        # Write to file
        ofile.write(outstring)

    # Closing the file
    ofile.close()

