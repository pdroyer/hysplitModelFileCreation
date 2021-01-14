
from hysplit.dat2grid import interpolate2grid, grid2netcdf, grid2netcdf
import netCDF4 as nc4
import boto3
import credentials_db
from s3fs.core import S3FileSystem

#Connect to S3 bucket for retreiving and storing data in S3 bucket
id = credentials_db.aws_access_key_id
key = credentials_db.aws_secret_access_key
s3client = boto3.client('s3', region_name='us-west-2', aws_access_key_id=id, aws_secret_access_key=key)
s3resource = boto3.resource('s3', region_name='us-west-2', aws_access_key_id=id, aws_secret_access_key=key)
#s3client.list_buckets() ##list buckets

##show files in array bucket
##this is not necessary, it is only for user benefit to see stored files in sS3
myBucket = s3resource.Bucket('hysplit')
for file in myBucket.objects.filter(Prefix='arrays/'):
    print(file.key)
##download files from S3
def s32local(bucket_name, key, outf):
    try:
        s3resource.Bucket(bucket_name).download_file(key, outf)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
#example s32local('hyplit', 'arrays/temperature.npy','my_local_array.npy')

"""
function met2grid fetches near real time data from meteorological stations, interpolates data to grid, and write arrays
as numpy files
2 args:
output path file for writing numpy arrays
Last time step in hours, beginning at zero. The example below runs for the first 48 hours
Note, the module as it is currently written requires that arrays are written to memory while processing
Large arrays may supersede available memory and fail. This is still being tested 

interpolate2grid.metdat2grid(<'ouput director for arrays'>, <number of time steps in hours>)

"""
interpolate2grid.metdat2grid('C:/files/EED_ML_LDRD/climatedatarrays/HongFei', 1)
"""
function arguments for grid2netcdf
(input array, group name for net CDF, output net cdf)

"""

#grid2netcdf.grid2netcdf('C:/files/EED_ML_LDRD/climatedatarrays/windspeed.npy', 'windspeed_data', 'C:/files/EED_ML_LDRD/netcdf/windspeedCDF.nc')
grid2netcdfHongfei.grid2netcdf('C:/files/EED_ML_LDRD/climatedatarrays/HongFei/', 'C:/files/EED_ML_LDRD/netcdf/allVarsCDF.nc')


##run directly from S23 bucket
s3files = S3FileSystem(anon=False, key=id, secret=key)
fkey = 'arrays/temperature.npy'
bucket = 'hysplit'
s3pth = s3files.open('{}/{}'.format(bucket, fkey))
#df = np.load(s3files.open('{}/{}'.format(bucket, fkey))) ##used when loading array diretly into memory

#grid2netcdf.grid2netcdf(s3pth, 'windspeed_data', 'C:/files/EED_ML_LDRD/netcdf/windspeedCDF.nc')
grid2netcdfHongfei.grid2netcdf(s3pth, 'C:/files/EED_ML_LDRD/netcdf/windspeedCDF.nc')


"""
verify netCDFfile written correctly by opening and examining
"""
fname = 'C:/files/EED_ML_LDRD/netcdf/windspeedCDF.nc'
f = nc4.Dataset(fname,'r')
f.groups ##show groups
windspeedgrp = f.groups['windspeed_data']
windspeedgrp.variables ##Show variables
windspeedgrp.variables.keys() ##show keys
windspeedgrp.variables['Windspeed'] #show variable

##accessing variables
zlvls = windspeedgrp.variables['Levels'][:]
ws = windspeedgrp.variables['Windspeed'][:]

##example file from NOAA WRF archive at


fname = r'C:\files\AU-31\HYSPLIT\inputFiles\WRF\wrfout_d01_2020-01-01_01_00_00-subset'
fWrf = nc4.Dataset(fname,'r')
fWrf.groups #looks like there are not groups in WRF format
fWrf.variables
fWrf.variables.keys()

fpvardescription = r'C:\files\AU-31\HYSPLIT\inputFiles\WRF\WRF_ARF_VAR_DESCRIPTION.csv'
varDescriptions = pd.read_csv(fpvardescription)

#read in our file created to compare
fnameNative = r'C:\files\EED_ML_LDRD\netcdf\allVarsCDF.nc'
fWrfNative = nc4.Dataset(fnameNative,'r')
"""
KEYS
odict_keys(['Times', 'LU_INDEX', 'ZNU', 'ZNW', 
'ZS', 'DZS', 'U', 'V', 'W', 'PH', 'PHB', 'T', 
'HFX_FORCE', 'LH_FORCE', 'TSK_FORCE', 'HFX_FORCE_TEND', 
'LH_FORCE_TEND', 'TSK_FORCE_TEND', 'MU', 'MUB', 'MUU', 
'MUV', 'MUT', 'P', 'PB', 'FNM', 'FNP', 'RDNW', 'RDN', 'DNW', 
'DN', 'CFN', 'CFN1', 'Q2', 'T2', 'TH2', 'PSFC', 'U10', 'V10', 
'RDX', 'RDY', 'RESM', 'ZETATOP', 'CF1', 'CF2', 'CF3', 'ITIMESTEP', 
'XTIME', 'QVAPOR', 'QCLOUD', 'QRAIN', 'TSLB', 'SMOIS', 'SH2O', 
'SMCREL', 'SEAICE', 'XICEM', 'IVGTYP', 'ISLTYP', 'VEGFRA',
'GRDFLX', 'SNOW', 'SNOWH', 'CANWAT', 'SSTSK', 'LAI', 
'TKE_PBL', 'MAPFAC_M', 'MAPFAC_U', 'MAPFAC_V', 'MAPFAC_MX', 'MAPFAC_MY',
'MAPFAC_UX', 'MAPFAC_UY', 'MAPFAC_VX', 'MF_VX_INV', 'MAPFAC_VY',
'HGT', 'TSK', 'P_TOP', 'T00', 'P00', 'TLP', 'TISO', 'MAX_MSTFX', 
'MAX_MSTFY', 'RAINC', 'RAINSH', 'RAINNC', 'SNOWNC', 'GRAUPELNC', 'HAILNC',
'SWDOWN', 'GLW', 'OLR', 'ALBEDO', 'CLAT', 'ALBBCK', 'EMISS', 'XLAND', 
'ZNT', 'UST', 'PBLH', 'HFX', 'QFX', 'LH', 'SNOWC', 'SR', 'SAVE_TOPO_FROM_REAL', 
'AVGFLX_RUM', 'AVGFLX_RVM', 'AVGFLX_WWM', 'SEED1', 'SEED2', 'LANDMASK', 'SST'])
"""
ZNUdat = fWrf.variables['ZNU'][:]
ZNWdat = fWrf.variables['ZNW'][:]


#reading in netCDF from NOAA to better understand data and data structure
fname = 'C:/files/repos/au-31/hysplit/input_output/wrfout_d01_2019-12-31_23_00_00-subset.nc'
f = nc4.Dataset(fname, 'r')
f.dimensions
f.variables
f.variable['SST']

