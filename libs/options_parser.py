import argparse
import textwrap

class OptionsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=
                'Generate a sphere of particles with a turbulent velocity field.',
                formatter_class=argparse.RawTextHelpFormatter)

        self.parser.add_argument("-N", "-n",
                            dest     = "num",
                            type     = int,
                            help     = "Number of particles (required)",
                            required = True)

        self.parser.add_argument("-o",
                            metavar = "outfile",
                            dest    = "outfile",
                            help    = "Name of output file",
                            default = "ics_cloud.dat")

        self.parser.add_argument("-format",
                            dest    = "format",
                            type    = int,
                            help    = "Format of output file.\n0 = ASCII,\n"+\
                                       "1 = Gadget binary format 1,\n"+\
                                       "2 = Gadget binary format 2",
                            default = 1)

        self.parser.add_argument("-m", "-mass",
                            dest     = "mass",
                            type     = float,
                            help     = "Total gas mass (in solar masses)",
                            default  = 1.)

        self.parser.add_argument("-npow",
                            dest     = "npow",
                            type     = float,
                            help     = "Power index of the power spectrum",
                            default  = 4.)

        self.parser.add_argument("-ngrid",
                            dest     = "ngrid",
                            type     = int,
                            help     = "Number of grid points per dimension for\n"+\
                                        "the turbulent velocity field",
                            default  = 256)

        self.parser.add_argument("-r", "-radius",
                            dest     = "radius",
                            type     = float,
                            help     = "Radius of the sphere (in parsecs)",
                            default  = 1.)

        self.parser.add_argument("--units",
                            dest     = "units",
                            help     = "Change units to Msol/Parsec/km s^{-1} ",
                            action   = "store_true")

    def get_args(self):
        return self.parser.parse_args()

