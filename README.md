# hysplitModelFileCreation
Work here is largely devoted to creating input files for NOAA Air Resource Model (ARL) HYSPLIT trajectory and
dispersion model. The core program logic is contained in the data2grid package.
example.py illustrates expected use of module.

dat2grid.interpolate2grid ingests climate data from MS SQL database, interpolates to grid based on spatial
extent of met stations, and exports multi-dimensional arrays for each parameter, for example
temperature.

dat2grid.grid2netcdf ingests arrays and converts them to netCDF4 file format.

inserfromnoaa.py creates dimensions, variables and attributes directly from a netDCF avaiable from NOAA. This was used
test the netCDF structure and ensure we were writing these correctly from our own data.

interpolateMet reads directly from met data stored in MS SQL and creates the 3 dimensional numpy arrays

For obvious reasons, the credentials_db.py file is not stored here. This must be obtained
separately and used in your local environment to work. Otherwise, the interpolation will not run. This file
also has credential access to S3 bucket on AWS. It is advisable to work directly with S3 objects to ensure that
all collaborators are working with the same data.

It is important to note, that the logic used involves aggregating arrays in a loop, which is based on the desired
number of time steps, and that during this process arrays are loaded into memory. Python 64bit can utilize your machine
memory, but none the less may be an upper bound constraint. Insufficient memory would cause the program to fail, and
is not accounted for in  catch statement thus far.
