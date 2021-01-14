import numpy as np
import pandas as pd
import sqlalchemy as sa
from pyproj import Proj, transform
from scipy.interpolate import griddata
import credentials_db
import os

print('libs imported')

db = credentials_db.dbstring
usr = credentials_db.username
pswrd = credentials_db.password

print('creating connection to database')
engine = sa.create_engine('mssql+pyodbc://' + usr + ':' + pswrd + '@' + db + ',915/SOCRATES?driver=ODBC Driver 13 for SQL Server')

print(engine)
usrSuper = credentials_db.usernameSuper
pswrdSuper = credentials_db.passwordSuper
engineSuperUser = sa.create_engine('mssql+pyodbc://syncRoot:v^_!nv3rs10n TRA1n!NG-::@we27211/Sync.Weather?driver=ODBC Driver 13 for SQL Server')
print ('connection to database successful')
engineSuperUser = sa.create_engine('mssql+pyodbc://' + usrSuper + ':' + pswrdSuper + '@we27211/Sync.Weather?driver=ODBC Driver 13 for SQL Server')
print ('connection to database successful')

#check connection as super user
try:
    engineSuperUser.connect()
    print ('connected as super user to met data')
except:
    print ('unable to connect to database as super user')

# check connection as super user
try:
    engine.connect()
    print('connected as user to met data')
except:
    print('unable to connect to database as user')


def metdat2grid(outDir, endStep, sampStep = 1):
    print('writing SQL statement')
    sql = "SELECT [SiteNumber],[SiteName],avg([Latitude]) as Latitude, " \
          "avg([Longitude]) as Longitude FROM [Sync.Weather].[dbo].[Metview] " \
          "where [SiteName] not in ('100N') group by [SiteNumber],[SiteName] order by [SiteNumber]asc"

    print('querying database for location information')
    hanfordMetLocs = pd.read_sql_query(sql, engineSuperUser)
    print('adjusting lat and lon values')
    hanfordMetLocs['LongitudeAdj'] = 0 - hanfordMetLocs['Longitude']
    locations = hanfordMetLocs[['Latitude', 'LongitudeAdj']]
    proj4326 = "+proj=longlat +datum=WGS84 +no_defs"
    proj2856 = "+proj=lcc +lat_1=47.33333333333334 +lat_2=45.83333333333334 +lat_0=45.33333333333334 +lon_0=-120.5 +x_0=500000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    inProj = Proj(proj4326)
    outProj = Proj(proj2856)
    print('converting and projecting locations to stateplane meters')
    xcoords, ycoords = [], []
    for xi in range(0, len(hanfordMetLocs)):
        x, y = transform(inProj, outProj, hanfordMetLocs['LongitudeAdj'][xi], hanfordMetLocs['Latitude'][xi])
        xcoords.append(x), ycoords.append(y)
    xcoords, ycoords = np.array(xcoords).astype(int), np.array(ycoords).astype(int)
    pnts = np.dstack(([xcoords], [ycoords])).reshape(30, 2)
    # add updated coordinates to table
    print('Adding coordinates to dataframe')
    hanfordMetLocs['xcoord_stateplane'], hanfordMetLocs['ycoord_stateplane'] = xcoords, ycoords
    print('identifying grid extents')
    xmin, xmax, ymin, ymax = hanfordMetLocs['xcoord_stateplane'].min(), hanfordMetLocs['xcoord_stateplane'].max(), \
                             hanfordMetLocs['ycoord_stateplane'].min(), hanfordMetLocs['ycoord_stateplane'].max()
    print(xmin, xmax, ymin, ymax)
    print('creating grids')
    grid_x, grid_y = np.mgrid[int(xmin):int(xmax):100, int(ymin):int(ymax):100]

    sql2 = "SELECT [SiteNumber] ,[SiteName],[avgWindDir],[avgWindSpeed],[avgTemp],[avgPrecip],[avgPrssr],[sampdatetime]" \
       "FROM [SOCRATES].[metdata].[Metview2017_hourly]" \
       "where SiteNumber not in ('300A')" \
       "order by SiteNumber,[sampdatetime] asc"
    print ('creating data frame from SQL query')
    df = pd.read_sql_query(sql2, engine)
    print ('creating index')
    df.set_index('sampdatetime', inplace=True) ##set index
    # df['sampdate'] = df.index
    df = df.fillna(method='backfill')
    print('creating index')
    df['timeunix'] = df.index.astype(np.int64) / 10 ** 11  ##create unix time
    print('creating unix int timestamp')
    times = df['timeunix'].unique()
    print('building empty array')
    """
    initial array shape below (0, 849, 1123) is derived from the coordinate extent
    to be mapped into to 2D space, such that np.empty((<time step>, <number of units in Y direction>, <number of units in X direction>))
    Y (849 here) is equivalent to the difference between the max and minimum Y value derived from latitude. X (1123) is equivalent to the 
    difference between the max and minimum along the X direction. Because the grid resolution is 100, and is done in meters (state plane)
    the geographic distance is 100 * 849, 849000 meters latitude, and 100 * 1123, 1123000 meters longitudinally  
    """
    """
    these will be filled when data is available
    emptyPressure = np.empty((0, 849, 1123))
    emptyWindSpeed = np.empty((0, 849, 1123))
    emptyTemperature = np.empty((0, 849, 1123))
    emptyWindDir = np.empty((0, 849, 1123))
    emptyzwindcomponent = np.empty((0, 849, 1123))
    emptywatervapor = np.empty((0, 849, 1123))
    emptyturbulentkineticenergy = np.empty((0, 849, 1123))
    emptyterrainelevation = np.empty((0, 849, 1123))
    emptysurfacepressure = np.empty((0, 849, 1123))
    emptytotalprecipitation = np.empty((0, 849, 1123))
    emptyboundarylayerheight = np.empty((0, 849, 1123))
    emptyfrictionvelocity = np.empty((0, 849, 1123))
    emptydownwardshortwaveflux = np.empty((0, 849, 1123))
    emptysensibleheatflux = np.empty((0, 849, 1123))
    emptylatentpressure = np.empty((0, 849, 1123))
    emptytemperatureat2m = np.empty((0, 849, 1123))
    emptyuwindcomponentat10m = np.empty((0, 849, 1123))
    emptyvwindcomponentat10m = np.empty((0, 849, 1123))
    
    """
    ##temporary array of zero vals
    emptyPressure = np.zeros((1, 849, 1123))
    emptyWindSpeed = np.zeros((1, 849, 1123))
    emptyTemperature = np.zeros((1, 849, 1123))
    emptyWindDir = np.zeros((1, 849, 1123))
    emptyzwindcomponent = np.zeros((1, 849, 1123))
    emptywatervapor = np.zeros((1, 849, 1123))
    emptyturbulentkineticenergy = np.zeros((1, 849, 1123))
    emptyterrainelevation = np.zeros((1, 849, 1123))
    emptysurfacepressure = np.zeros((1, 849, 1123))
    emptytotalprecipitation = np.zeros((1, 849, 1123))
    emptyboundarylayerheight = np.zeros((1, 849, 1123))
    emptyfrictionvelocity = np.zeros((1, 849, 1123))
    emptydownwardshortwaveflux = np.zeros((1, 849, 1123))
    emptysensibleheatflux = np.zeros((1, 849, 1123))
    emptylatentpressure = np.zeros((1, 849, 1123))
    emptytemperatureat2m = np.zeros((1, 849, 1123))
    emptyuwindcomponentat10m = np.zeros((1, 849, 1123))
    emptyvwindcomponentat10m = np.zeros((1, 849, 1123))


    for t in times[0:endStep]:  ##run for first 24 hours
        print('start loop ')
        mask = df['timeunix'] == t
        df2 = df.loc[mask]
        dt = pd.to_datetime(df2['timeunix'].head(1) * 10 ** 11)
        print('coverting data to array for ts ' + str(dt))
        windSpeedInterpolate = np.array(df2['avgWindSpeed'])
        tempInterpolate = np.array(df2['avgTemp'])
        windDirInterpolate = np.array(df2['avgWindDir'])
        pressureInterpolate = np.array(df2['avgPrssr'])
        print('interpolating to grid')
        gridPressure = griddata(pnts, pressureInterpolate, (grid_x, grid_y), method='nearest')
        print('appending pressure')
        emptyPressure = np.append(emptyPressure, gridPressure.reshape(1, 849, 1123), axis=0)
        gridWindSpeed = griddata(pnts, windSpeedInterpolate, (grid_x, grid_y), method='nearest')
        print('appending wind speed')
        emptyWindSpeed = np.append(emptyWindSpeed, gridWindSpeed.reshape(1, 849, 1123), axis=0)
        gridTemperature = griddata(pnts, tempInterpolate, (grid_x, grid_y), method='nearest')
        print('appending temperature')
        emptyTemperature = np.append(emptyTemperature, gridTemperature.reshape(1, 849, 1123), axis=0)
        print('appending wind direction')
        gridWindDir = griddata(pnts, windDirInterpolate, (grid_x, grid_y), method='nearest')
        emptyWindDir = np.append(emptyWindDir, gridWindDir.reshape(1, 849, 1123), axis=0)
        
    #TODO Hongfei:Load more data from database and asssign into the remailing empty** variables

        print(emptyWindSpeed.shape)
        print(emptyTemperature.shape)
        print(emptyWindDir.shape)
    print('saving arrays')
    np.save(os.path.join(outDir, 'windpressure.npy'), emptyPressure)
    np.save(os.path.join(outDir, 'windspeed.npy'), emptyWindSpeed)
    np.save(os.path.join(outDir, 'temperature.npy'), emptyTemperature)
    np.save(os.path.join(outDir, 'winddir.npy'), emptyWindDir)

    #W: zwindcomponent.npy
    #QVAPOR: watervapor.npy
    #TKE_PBL: turbulentkineticenergy.npy
    #HGT: terrainelevation.npy
    #PSFC: surfacepressure.npy
    #RAIN: totalprecipitation.npy
    #PBLH: boundarylayerheight.npy
    #UST: frictionvelocity.npy
    #SWDOWN: downwardshortwaveflux.npy
    #HFX: sensibleheatflux.npy
    #LH: latentpressure.npy
    #T2: temperatureat2m.npy
    #U10: uwindcomponentat10m.npy
    #V10: vwindcomponentat10m.npy

    print('saving arrays with zero dat')
    np.save(os.path.join(outDir, 'zwindcomponent.npy'), emptyzwindcomponent)
    np.save(os.path.join(outDir, 'watervapor.npy'), emptywatervapor)
    np.save(os.path.join(outDir, 'turbulentkineticenergy.npy'), emptyturbulentkineticenergy)
    np.save(os.path.join(outDir, 'terrainelevation.npy'), emptyterrainelevation)
    np.save(os.path.join(outDir, 'surfacepressure.npy'), emptysurfacepressure)
    np.save(os.path.join(outDir, 'totalprecipitation.npy'), emptytotalprecipitation)
    np.save(os.path.join(outDir, 'boundarylayerheight.npy'), emptyboundarylayerheight)
    np.save(os.path.join(outDir, 'frictionvelocity.npy'), emptyfrictionvelocity)
    np.save(os.path.join(outDir, 'downwardshortwaveflux.npy'), emptydownwardshortwaveflux)
    np.save(os.path.join(outDir, 'sensibleheatflux.npy'), emptysensibleheatflux)
    np.save(os.path.join(outDir, 'latentpressure.npy'), emptylatentpressure)
    np.save(os.path.join(outDir, 'temperatureat2m.npy'), emptytemperatureat2m)
    np.save(os.path.join(outDir, 'uwindcomponentat10m.npy'), emptyuwindcomponentat10m)
    np.save(os.path.join(outDir, 'vwindcomponentat10m.npy'), emptyvwindcomponentat10m)

##example
## interpolate2grid('C:/files/EED_ML_LDRD/climatedatarrays', 12)


