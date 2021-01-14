from netCDF4 import Dataset
import sys

#example
#python hongfei.py 'C:/files/repos/au-31/hysplit/input_output/wrfout_d01_2019-12-31_23_00_00-subset.nc' 'outCDF2.nc'

#-----------------
# read netCDF file
#-----------------

##exanmple

# open a netCDF file to read
argvs = sys.argv
inputfilename = argvs[1]
outputfilename = argvs[2]

ncin = Dataset(inputfilename, 'r')

# check netCDF file format
#print(ncin.file_format)
print(ncin)

# get dimensions
_timedimension = ncin.dimensions['Time']
_datestringlendimension = ncin.dimensions['DateStrLen']
_westeastdimension = ncin.dimensions['west_east']
_southnorthdimension = ncin.dimensions['south_north']
_bottomtopdimension = ncin.dimensions['bottom_top']
_bottomtopstagdimension = ncin.dimensions['bottom_top_stag']
_soillayersstagdimension = ncin.dimensions['soil_layers_stag']
_westeaststagdimension = ncin.dimensions['west_east_stag']
_southnorthstagdimension = ncin.dimensions['south_north_stag']

# get length of each dimension
ndatestringlendimension = len(_datestringlendimension)
nwesteastdimension = len(_westeastdimension)
nsouthnorthdimension = len(_southnorthdimension)
nbottomtopdimension = len(_bottomtopdimension)
nbottomtopstagdimension = len(_bottomtopstagdimension)
nsoillayersstagdimension = len(_soillayersstagdimension)
nwesteaststagdimension = len(_westeaststagdimension)
nsouthnorthstagdimension = len(_southnorthstagdimension)

# get variables
_p = ncin.variables['P']
_T = ncin.variables['T']
_U = ncin.variables['U']
_V = ncin.variables['V']
_W = ncin.variables['W']
_QVAPOR = ncin.variables['QVAPOR']
_TKE_PBL = ncin.variables['TKE_PBL']
_HGT = ncin.variables['HGT']
_PSFC = ncin.variables['PSFC']
_RAIN = ncin.variables['RAINNC']
_PBLH = ncin.variables['PBLH']
_UST = ncin.variables['UST']
_SWDOWN = ncin.variables['SWDOWN']
_HFX = ncin.variables['HFX']
_LH = ncin.variables['LH']
_T2 = ncin.variables['T2']
_U10 = ncin.variables['U10']
_V10 = ncin.variables['V10']
_RAINNC = ncin.variables['RAINNC']
_RAINC = ncin.variables['RAINC']
_RAINSH = ncin.variables['RAINSH']
_PB = ncin.variables['PB']
_Times = ncin.variables['Times']
_XTIME = ncin.variables['XTIME']
_ZNU = ncin.variables['ZNU']
_ZNW = ncin.variables['ZNW']

#------------------
# write netCDF file
#------------------

# open a netCDF file to write
ncfile = Dataset(outputfilename, 'w', format='NETCDF3_CLASSIC')

# create dimension
ncfile.createDimension('Time', None)  # unlimited
ncfile.createDimension('DateStrLen', ndatestringlendimension)
ncfile.createDimension('west_east', nwesteastdimension)
ncfile.createDimension('south_north', nsouthnorthdimension)
ncfile.createDimension('bottom_top', nbottomtopdimension)
ncfile.createDimension('bottom_top_stag', nbottomtopstagdimension)
ncfile.createDimension('soil_layers_stag', nsoillayersstagdimension)
ncfile.createDimension('west_east_stag', nwesteaststagdimension)
ncfile.createDimension('south_north_stag', nsouthnorthstagdimension)

# create variables
P = ncfile.createVariable('P','f',('Time','bottom_top','south_north','west_east'))
P.units = 'Pa'
P.description = 'Total pressure'
P.time_op = 'average'
T = ncfile.createVariable('T','f',('Time','bottom_top','south_north','west_east'))
T.units = 'K'
T.description = 'Temperature'
T.time_op = 'average'
U = ncfile.createVariable('U','f',('Time','bottom_top','south_north','west_east_stag'))
U.units = 'm s-1'
U.description = 'U component of wind'
U.time_op = 'average'
V = ncfile.createVariable('V','f',('Time','bottom_top','south_north_stag','west_east'))
V.units = 'm s-1'
V.description = 'V component of wind'
V.time_op = 'average'
W = ncfile.createVariable('W','f',('Time','bottom_top_stag','south_north','west_east'))
W.units = 'Pa s-1'
W.description = 'time-averaged mass coupled eta-dot'
W.time_op = 'average'
QVAPOR = ncfile.createVariable('QVAPOR','f',('Time','bottom_top','south_north','west_east'))
QVAPOR.units = 'kg kg-1'
QVAPOR.description = 'water vapor mixing ratio'
QVAPOR.time_op = 'average'
TKE_PBL = ncfile.createVariable('TKE_PBL','f',('Time','bottom_top_stag','south_north','west_east'))
TKE_PBL.units = 'm2 s-2'
TKE_PBL.description = 'turbulent Kinetic Energy (TKE) from PBL schemes'
TKE_PBL.time_op = 'average'
HGT = ncfile.createVariable('HGT','f',('Time','south_north','west_east'))
HGT.units = 'm'
HGT.description = 'Terrain elevation'
HGT.time_op = 'average'
PSFC = ncfile.createVariable('PSFC','f',('Time','south_north','west_east'))
PSFC.units = 'Pa'
PSFC.description = 'surface pressure'
PSFC.time_op = 'average'
RAIN = ncfile.createVariable('RAIN','f',('Time','south_north','west_east'))
RAIN.units = 'mm'
RAIN.description = 'total precipitation'
RAIN.time_op = 'average'
RAINNC = ncfile.createVariable('RAINNC','f',('Time','south_north','west_east'))
RAINNC.units = 'mm'
RAINNC.description = 'Accumulated total grid scale precipitation'
RAINNC.time_op = 'average'
RAINC = ncfile.createVariable('RAINC','f',('Time','south_north','west_east'))
RAINC.units = 'mm'
RAINC.description = 'Accumulated total cumulus precipitation'
RAINC.time_op = 'average'
RAINSH = ncfile.createVariable('RAINSH','f',('Time','south_north','west_east'))
RAINSH.units = 'mm'
RAINSH.description = 'Accumulated shallow cumulus precipitation'
RAINSH.time_op = 'average'
PBLH = ncfile.createVariable('PBLH','f',('Time','south_north','west_east'))
PBLH.units = 'm'
PBLH.description = 'boundary layer height'
PBLH.time_op = 'average'
UST = ncfile.createVariable('UST','f',('Time','south_north','west_east'))
UST.units = 'm s-1'
UST.description = 'friction velocity'
UST.time_op = 'average'
SWDOWN = ncfile.createVariable('SWDOWN','f',('Time','south_north','west_east'))
SWDOWN.units = 'W m-2'
SWDOWN.description = 'Downward shortwave flux'
SWDOWN.time_op = 'average'
HFX = ncfile.createVariable('HFX','f',('Time','south_north','west_east'))
HFX.units = 'W m-2'
HFX.description = 'sensible heat flux'
HFX.time_op = 'average'
LH = ncfile.createVariable('LH','f',('Time','south_north','west_east'))
LH.units = 'W m-2'
LH.description = 'latent heat flux'
LH.time_op = 'average'
T2 = ncfile.createVariable('T2', 'f', ('Time','south_north','west_east'))
T2.units = 'K'
T2.description = 'Temperature at 2m'
T2.time_op = 'average'    
U10 = ncfile.createVariable('U10','f',('Time','south_north','west_east'))
U10.units = 'm s-1'
U10.description = 'U component of wind at 10m'
U10.time_op = 'average'
V10 = ncfile.createVariable('V10','f',('Time','south_north','west_east'))
V10.units = 'm s-1'
V10.description = 'V component of wind at 10m'
V10.time_op = 'average'
PB = ncfile.createVariable('PB','f',('Time','bottom_top','south_north','west_east'))
PB.units = 'Pa'
PB.description = 'Base state pressure'

Times = ncfile.createVariable('Times','b',('Time','DateStrLen'))
Times.description = 'Times'
XTIME = ncfile.createVariable('XTIME','f',('Time'))
XTIME.description = 'Minutes since simulation start'
ZNU = ncfile.createVariable('ZNU','f',('Time','bottom_top'))
ZNU.description = 'eta values on half(mass) levels'
ZNW = ncfile.createVariable('ZNW','f',('Time','bottom_top_stag'))
ZNW.description = 'eta values on full(w) levels'

## see https://www.ncl.ucar.edu/Applications/wrflc.shtml for map information

#Assign values to attributes
ncfile.TITLE = 'Output from hongfei.py'
ncfile.START_DATE = '2019-12-30_06:00:00'
ncfile.SIMULATION_START_DATE = '2019-12-30_06:00:00'
ncfile.MAP_PROJ = 1
"""
MAP_PROJ = 0 --> "CylindricalEquidistant"
MAP_PROJ = 1 --> "LambertConformal"
MAP_PROJ = 2 --> "Stereographic"
MAP_PROJ = 3 --> "Mercator"
MAP_PROJ = 6 --> "Lat/Lon"
"""
ncfile.CEN_LAT = 37.000008
ncfile.CEN_LON = -98
ncfile.STAND_LON = -98
ncfile.DX = 27000.0
ncfile.DY = 27000.0
ncfile.TRUELAT1 = 25
ncfile.TRUELAT2 = 50

"""
The following would be used for our dataset 
#Assign values to attributes
ncfile.TITLE = 'Output from hongfei.py'
ncfile.START_DATE = '2019-12-30_06:00:00'
ncfile.SIMULATION_START_DATE = '2019-12-30_06:00:00'
ncfile.MAP_PROJ = 1
ncfile.CEN_LAT = 101758
ncfile.CEN_LON = 564407
ncfile.STAND_LON = 564407
ncfile.DX = 100.00
ncfile.DY = 100.00
ncfile.TRUELAT1 = 45642
ncfile.TRUELAT2 = 157875

"""


# Assign values to variables
P[:] = _p[:]
T[:] = _T[:]
U[:] = _U[:]
V[:] = _V[:]
W[:] = _W[:]
QVAPOR[:] = _QVAPOR[:]
TKE_PBL[:] = _TKE_PBL[:]
HGT[:] = _HGT[:]
PSFC[:] = _PSFC[:]
RAIN[:] = _RAIN[:]
PBLH[:] = _PBLH[:]
UST[:] = _UST[:]
SWDOWN[:] = _SWDOWN[:]
HFX[:] = _HFX[:]
LH[:] = _LH[:]
T2[:] = _T2[:]
U10[:] = _U10[:]
V10[:] = _V10[:]

#TODO:HONGFEI How to assign the data: [[b'2' b'0' b'1' b'9' b'-' b'1' b'2' b'-' b'3' b'1' b'_' b'2' b'3' b':' b'0' b'0' b':' b'0' b'0']]
#Times[:] = _Times[:]
XTIME[:] = _XTIME[:]
ZNU[:] = _ZNU[:]
ZNW[:] = _ZNW[:]
RAINC[:] = _RAINC[:]
RAINNC[:] = _RAINNC[:]
RAINSH[:] = _RAINSH[:]

print('         Succefully created the netcdf file!')

# close files
ncin.close()
ncfile.close()
