import numpy as np
import netCDF4 as nc4
from datetime import datetime
import os

### TODO Hongfei: Please check the following code
def grid2netcdf(inDir, outCdf):
    print('loading arrays')
    windpressureArr = np.load(os.path.join(inDir, 'windpressure.npy'))
    windspeedArr = np.load(os.path.join(inDir, 'windspeed.npy'))
    temperatureArr = np.load(os.path.join(inDir, 'temperature.npy'))
    winddirArr = np.load(os.path.join(inDir, 'winddir.npy'))
    zwindcomponentArr = np.load(os.path.join(inDir, 'zwindcomponent.npy'))
    watervaporArr = np.load(os.path.join(inDir, 'watervapor.npy'))
    turbulentkineticenergyArr = np.load(os.path.join(inDir, 'turbulentkineticenergy.npy'))
    terrainelevationArr = np.load(os.path.join(inDir, 'terrainelevation.npy'))
    surfacepressureArr = np.load(os.path.join(inDir, 'surfacepressure.npy'))
    totalprecipitationArr = np.load(os.path.join(inDir, 'totalprecipitation.npy'))
    boundarylayerheightArr = np.load(os.path.join(inDir, 'boundarylayerheight.npy'))
    frictionvelocityArr = np.load(os.path.join(inDir, 'frictionvelocity.npy'))
    downwardshortwavefluxArr = np.load(os.path.join(inDir, 'downwardshortwaveflux.npy'))
    sensibleheatfluxArr = np.load(os.path.join(inDir, 'sensibleheatflux.npy'))
    latentpressureArr = np.load(os.path.join(inDir, 'latentpressure.npy'))
    temperatureat2mArr = np.load(os.path.join(inDir, 'temperatureat2m.npy'))
    uwindcomponentat10mArr = np.load(os.path.join(inDir, 'uwindcomponentat10m.npy'))
    vwindcomponentat10mArr = np.load(os.path.join(inDir, 'vwindcomponentat10m.npy'))
    #arr = np.load(inArr)
    print('arrays loaded')
    ###TODO Hongfei:The passed-in file needs to contain data for all the variables
    height = windspeedArr.shape[1]
    width = windspeedArr.shape[2]
    zeroDim = windspeedArr.shape[0]
    lon1 = np.arange(0, windspeedArr.shape[1])
    lat1 = np.arange(0, windspeedArr.shape[2])
    x = windspeedArr
    z = np.arange(0, windspeedArr.shape[0])
    print('creating netCDF files')
    ncfile = nc4.Dataset(outCdf, 'w', format='NETCDF4')
    ncfile.title='Output of Met raw data'
    ncfile.subtitle='From database'

    print('creating dimemsions')
    time_dim = ncfile.createDimension('time', None) 
    lev_dim = ncfile.createDimension('lev', zeroDim) 
    lat_dim = ncfile.createDimension('lat', width) 
    lon_dim = ncfile.createDimension('lon', height)

    ilev_dim = ncfile.createDimension('ilev', zeroDim)

    #List of WRF-ARW variables converted to the use of HYSPLIT.
    #Variable in WRF-ARW 	Variable in HYSPLIT 	Note 
    #P (i.e P+PB) 	            PRES 	        Total pressure 
    #T (i.e T+300.0) 	        TEMP 	        Converting potential temperature (WRF) to ambient temperature 
    #U 	                        UWND 	        U component of wind 
    #(or AVGFLX_RUM) 		                    (or time-averaged mass coupled u-wind) 
    #V 	                        VWND 	        V component of wind 
    #(or AVGFLX_RVM) 		                    (or time-averaged mass coupled v-wind) 
    #W 	                        WWND 	        Converting vertical velocity (m/s) to omega (hPa/s) 
    #(or AVGFLX_WWM) 		                    (or time-averaged mass coupled eta-dot, unit Pa/s, no conversion) 
    #X 	                        DIFW 	        Writing difference field for greater precision for vertical velocities 
    #QVAPOR 	                SPHU 	        Water vapor mixing ratio 
    #TKE_PBL 	                TKEN 	        Turbulent Kinetic Energy (TKE) from PBL schemes 
    #X 	                        DIFT 	        Writing difference field for greater precision for TKE 
    #HGT 	                    SHGT 	        Terrain elevation 
    #PSFC 	                    PRSS 	        Surface pressure 
    #RAIN 	                    TPP1 	        Total precipitation 
    #(i.e RAINC+RAINNC) 		
    #X 	                        DIFR 	        Writing difference field for greater precision for precipitation 
    #PBLH 	                    PBLH 	        Boundary layer height 
    #UST 	                    USTR 	        Friction velocity 
    #SWDOWN 	                DSWF 	        Downward shortwave flux 
    #HFX 	                    SHTF 	        Sensible heat flux 
    #LH 	                    LHTF 	        Latent heat flux 
    #T2 	                    T02M 	        Temperature at 2 m 
    #U10 	                    U10M 	        U component of wind at 10 m 
    #V10 	                    V10M 	        V component of wind at 10 m 
    #NOTE: ’X’ is not a variable in WRF but a placeholder used in the WRFDATA.CFG to process the difference field for greater precision.

    print('creating variables')
    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = 'days since 0000-09-01 00:00:00'

    time.description = 'time'
    print('time variable added')
    lev = ncfile.createVariable('lev', np.float32, ('lev',))
    lev.units = 'hybrid_sigma_pressure'
    #lev.description = 'hybrid level at layer midpoints (1000*(A+B))'
    lev.positive = "down"
    lev.description = "atmosphere_hybrid_sigma_pressure_coordinate"
    lev.formula_terms = "a: hyam b: hybm p0: P0 ps: PS"
    print('lev variable added')
    lon = ncfile.createVariable('lon', np.float32, ('lon',))
    lon.units = 'degrees_east'
    lon.description = 'longitude'
    print('lon variable added')
    lat = ncfile.createVariable('lat', np.float32, ('lat',))
    lat.units = 'degrees_north'
    lat.description = 'latitude'
    print('lat variable added')
    ilev = ncfile.createVariable('ilev', np.float32, ('ilev',))
    ilev.units = 'hybrid_sigma_pressure'
    ilev.description = 'hybrid level at layer interfaces (1000*(A+B))'
    ilev.positive = "down"
    ilev.formula_terms = "a: hyai b: hybi p0: P0 ps: PS"
    print('ilev variable added')
    hybm = ncfile.createVariable('hybm', np.float32, ('lev',))
    hybm.description = 'hybrid B coefficient at layer midpoints'
    hyam = ncfile.createVariable('hyam', np.float32, ('lev',))
    hyam.description = 'hybrid A coefficient at layer midpoints'
    print('hyam variable added')
    hybi = ncfile.createVariable('hybi', np.float32, ('ilev',))
    hybi.description = 'hybrid B coefficient at layer interfaces'
    hyai = ncfile.createVariable('hyai', np.float32, ('ilev',))
    hyai.description = 'hybrid A coefficient at layer interfaces'
    print('hyai variable added')
    P = ncfile.createVariable('P',np.float32,('time','lev','lat','lon'))
    P.units = 'Pa'
    P.description = 'Total pressure'
    P.time_op = 'average'
    print('P variable added')
    T = ncfile.createVariable('T',np.float32,('time','lev','lat','lon'))
    T.units = 'K'
    T.description = 'Temperature'
    T.time_op = 'average'
    print('T variable added')
    U = ncfile.createVariable('U',np.float32,('time','lev','lat','lon'))
    U.units = 'm s-1'
    U.description = 'U component of wind'
    U.time_op = 'average'
    V = ncfile.createVariable('V',np.float32,('time','lev','lat','lon'))
    V.units = 'm s-1'
    V.description = 'V component of wind'
    V.time_op = 'average'
    print('V variable added')
    W = ncfile.createVariable('W',np.float32,('time','lev','lat','lon'))
    W.units = 'Pa s-1'
    W.description = 'time-averaged mass coupled eta-dot'
    W.time_op = 'average'
    QVAPOR = ncfile.createVariable('QVAPOR',np.float32,('time','lev','lat','lon'))
    QVAPOR.units = 'kg kg-1'
    QVAPOR.description = 'water vapor mixing ratio'
    QVAPOR.time_op = 'average'
    print('Q var added')
    TKE_PBL = ncfile.createVariable('TKE_PBL',np.float32,('time','lev','lat','lon'))
    TKE_PBL.units = 'm2 s-2'
    TKE_PBL.description = 'turbulent Kinetic Energy (TKE) from PBL schemes'
    TKE_PBL.time_op = 'average'
    HGT = ncfile.createVariable('HGT',np.float32,('time','lat','lon'))
    HGT.units = 'm'
    HGT.description = 'Terrain elevation'
    HGT.time_op = 'average'
    PSFC = ncfile.createVariable('PSFC',np.float32,('time','lat','lon'))
    PSFC.units = 'Pa'
    PSFC.description = 'surface pressure'
    PSFC.time_op = 'average'
    RAIN = ncfile.createVariable('RAIN',np.float32,('time','lat','lon'))
    RAIN.units = 'mm'
    RAIN.description = 'total precipitation'
    RAIN.time_op = 'average'
    PBLH = ncfile.createVariable('PBLH',np.float32,('time','lat','lon'))
    PBLH.units = 'm'
    PBLH.description = 'boundary layer height'
    PBLH.time_op = 'average'
    UST = ncfile.createVariable('UST',np.float32,('time','lat','lon'))
    UST.units = 'm s-1'
    UST.description = 'friction velocity'
    UST.time_op = 'average'
    SWDOWN = ncfile.createVariable('SWDOWN',np.float32,('time','lat','lon'))
    SWDOWN.units = 'W m-2'
    SWDOWN.description = 'Downward shortwave flux'
    SWDOWN.time_op = 'average'
    HFX = ncfile.createVariable('HFX',np.float32,('time','lat','lon'))
    HFX.units = 'W m-2'
    HFX.description = 'sensible heat flux'
    HFX.time_op = 'average'
    LH = ncfile.createVariable('LH',np.float32,('time','lat','lon'))
    LH.units = 'W m-2'
    LH.description = 'latent heat flux'
    LH.time_op = 'average'
    #T2 = ncfile.createVariable('T',np.float32,('T','lat','lon')) #no dimension 'T'
    T2 = ncfile.createVariable('T2', np.float32, ('time', 'lat', 'lon'))
    T2.units = 'K'
    T2.description = 'Temperature at 2m'
    T2.time_op = 'average'    
    U10 = ncfile.createVariable('U10',np.float32,('time','lat','lon'))
    U10.units = 'm s-1'
    U10.description = 'U component of wind at 10m'
    U10.time_op = 'average'
    V10 = ncfile.createVariable('V10',np.float32,('time','lat','lon'))
    V10.units = 'm s-1'
    V10.description = 'V component of wind at 10m'
    V10.time_op = 'average'
    #TODO Hongfei: Add other variables here
    print('adding arrag data to variables')
    lon[:] = lon1
    lat[:] = lat1
    lev[:] = z
    """P[0, :, :, :] = windpressureArr This array cannont be reshaped into 
    these dimensions because there are multiple time steps. We need to assume the 2nd index is zero
    """

    P[0,:1,:,:] = windpressureArr[1]
    print('added wind pressure')
    T[0,:1,:,:] = temperatureArr[1]
    print('temp array added')
    U[0,:1,:,:] = windspeedArr[1]
    print('wind speed added')
    V[0,:1,:,:] = winddirArr[1]
    print('wind direction added')
    W[0,:1,:,:] = zwindcomponentArr[0]
    print('z added')
    QVAPOR[0,:1,:,:] = watervaporArr[0]
    print('vapor added')
    TKE_PBL[0,:1,:,:] = turbulentkineticenergyArr[0]
    print('TKE PBL added')
    HGT[0,:,:] = terrainelevationArr[0]
    print('terrain elevation added')
    PSFC[0,:,:] = surfacepressureArr[0]
    RAIN[0,:,:] =  totalprecipitationArr[0]
    PBLH[0,:,:] = boundarylayerheightArr[0]
    UST[0,:,:] = frictionvelocityArr[0]
    SWDOWN[0,:,:] = downwardshortwavefluxArr[0]
    HFX[0,:,:] = sensibleheatfluxArr[0]
    LH[0,:,:] = latentpressureArr[0]
    T2[0,:,:] = temperatureat2mArr[0]
    U10[0,:,:] = uwindcomponentat10mArr[0]
    V10[0,:,:] = vwindcomponentat10mArr[0]
    #TODO Hongfei: Assign data to all variables here
    print ('adding description')
    ncfile.description = "From dataset containing interpolated met data"
    ncfile.history = "Created " + datetime.today().strftime("%d/%m/%y")
    ncfile.close()


##example grid2netcdf(inArr, groupName, 'windspeed_data')


def grid2netcdfFile(inArr, groupName, outCdf):
    print ('loading array')
    arr = np.load(inArr)
    ##reshape to 3d array and add fictional data
    # arrones = np.ones((1, arr.shape[1], arr.shape[2]))  # create array of one values for fake dat
    print ('reshaping array')
    # arr = arr.reshape(1, arr.shape[1], arr.shape[2])  # reshape first array
    # arr = np.append(arr, arrones, axis=0)  # append new array dat to ones
    height = arr.shape[1]
    width = arr.shape[2]
    zeroDim = arr.shape[0]

    lon = np.arange(0, arr.shape[1])
    lat = np.arange(0, arr.shape[2])
    x = arr
    z = np.arange(0, arr.shape[0])
    print('creating dimensions')
    f = nc4.Dataset(outCdf, 'w', format='NETCDF4')  # 'w' stands for write
    ##create group for first variable
    grp = f.createGroup(groupName)
    grp.createDimension('lon', height)
    grp.createDimension('lat', width)
    grp.createDimension('z', zeroDim)
    grp.createDimension('time', None)
    ##create variables
    print('creating variables')
    longitude = grp.createVariable('Longitude', 'f4', 'lon')
    latitude = grp.createVariable('Latitude', 'f4', 'lat')
    levels = grp.createVariable('Levels', 'i4', 'z')
    windspeed = grp.createVariable('Windspeed', 'f4', ('time', 'lon', 'lat', 'z'))
    time = grp.createVariable('Time', 'i4', 'time')

    ##pass in vars
    print('passing data')
    longitude[:] = lon #The "[:]" at the end of the variable instance is necessary
    latitude[:] = lat
    levels[:] = z
    windspeed[0,:,:,:] = arr
    # Add global attributes
    print('adding  description')
    f.description = "Example dataset containing interpolated met data"
    from datetime import datetime
    f.history = "Created " + datetime.today().strftime("%d/%m/%y")
    f.close()

##example grid2netcdf(inArr, groupName, 'windspeed_data')
