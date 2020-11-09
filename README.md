# turbulent-cloud
A spherical distribution of particles with turbulent velocity field.

The code first produces a sphere in a close-packed distribution. Then, it
assigns each particle a random velocity such that the cloud has a turbulent velocity
field with a given power spectrum. The default power index is npow=-4, which is
consistent with the observed velocity distribution of molecular clouds
(Larson 1981).

This code is **under development**.

# Author
Felipe G. Goicovic

# Usage

The basic usage is
```bash
python cloud.py -n NUM
```
where NUM is the total number of particles desired to represent the spherical cloud.
This will produce a binary file called 'ics_cloud.dat' that works as initial
conditions for GADGET (format 1).

For a complete description of parameters use
```bash
python cloud.py -h
```
