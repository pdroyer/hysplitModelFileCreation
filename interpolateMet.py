
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy as sa
from pyproj import Proj, transform
from scipy.interpolate import griddata
import credentials_db

print ('imported libraries')

# from pandas.plotting import register_matplotlib_converters
pd.options.mode.use_inf_as_na = True
# register_matplotlib_converters()
print ('imported libraries')

##log in a super user with ADF level connection
##Only I will be able to log in as super user
db = credentials_db.dbstring
usr = credentials_db.username
pswrd = credentials_db.password

print('creating connection to databaes')
engine = sa.create_engine('mssql+pyodbc://' + usr + ':' + pswrd + '@' + db + ',915/SOCRATES?driver=ODBC Driver 13 for SQL Server')
print(engine)
print ('connection to database successful')

usrSuper = credentials_db.usernameSuper
pswrdSuper = credentials_db.passwordSuper

engineSuperUser = sa.create_engine('mssql+pyodbc://syncRoot:v^_!nv3rs10n TRA1n!NG-::@we27211/Sync.Weather?driver=ODBC Driver 13 for SQL Server')
print ('connection to database successful')

engineSuperUser = sa.create_engine('mssql+pyodbc://' + usrSuper + ':' + pswrdSuper + '@we27211/Sync.Weather?driver=ODBC Driver 13 for SQL Server')
print ('engineSuperUser')
print ('connection to database successful')


"""
select locations for sites. Here I had to take mean lat/lon values because there were several for
each site. Exclude site 100N - duplicate record 
"""
sql = "SELECT [SiteNumber],[SiteName],avg([Latitude]) as Latitude, " \
      "avg([Longitude]) as Longitude FROM [Sync.Weather].[dbo].[Metview] " \
      "where [SiteName] not in ('100N') group by [SiteNumber],[SiteName] order by [SiteNumber]asc"

print ('querying database for location information')
hanfordMetLocs = pd.read_sql_query(sql, engineSuperUser)

"""
update longitude to account for negative distance from prime meridian
project to state plane for better resolution
"""

hanfordMetLocs['LongitudeAdj'] = 0 - hanfordMetLocs['Longitude']
locations = hanfordMetLocs[['Latitude', 'LongitudeAdj']]
proj4326 = "+proj=longlat +datum=WGS84 +no_defs"
proj2856 = "+proj=lcc +lat_1=47.33333333333334 +lat_2=45.83333333333334 +lat_0=45.33333333333334 +lon_0=-120.5 +x_0=500000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
inProj = Proj(proj4326)
outProj = Proj(proj2856)

##convert coordinates to state plane for easier eclidean style interpretation

print('converting and projecting locations')
xcoords, ycoords = [], []
for xi in range (0, len(hanfordMetLocs)):
    x, y = transform(inProj,outProj,hanfordMetLocs['LongitudeAdj'][xi],hanfordMetLocs['Latitude'][xi])
    xcoords.append(x), ycoords.append(y)
##convert to 2-D array for interpolation using scipy interpolate
xcoords, ycoords = np.array(xcoords).astype(int), np.array(ycoords).astype(int)

##plot met stations
plt.plot(xcoords - xcoords.min(), ycoords - ycoords.min(), 'bo')

pnts = np.dstack(([xcoords], [ycoords])).reshape(30,2)
#add updated coordinates to table
print('Adding coordinates to dataframe')
hanfordMetLocs['xcoord_stateplane'], hanfordMetLocs['ycoord_stateplane'] = xcoords, ycoords

##define extents for interpolation
xmin, xmax, ymin, ymax = hanfordMetLocs['xcoord_stateplane'].min(), hanfordMetLocs['xcoord_stateplane'].max(), hanfordMetLocs['ycoord_stateplane'].min(), hanfordMetLocs['ycoord_stateplane'].max()
print(xmin, xmax, ymin, ymax)
#ceeate gird with  100X100 resolution
grid_x, grid_y = np.mgrid[int(xmin):int(xmax):100,int(ymin):int(ymax):100]

"""integrate data from database for select time step
   query data by time step to create an iterator 
"""

#return list of timestamps for loops

sql = "SELECT [SiteNumber] ,[SiteName],[avgWindDir],[avgWindSpeed],[avgTemp],[avgPrecip],[avgPrssr],[sampdatetime]" \
       "FROM [SOCRATES].[metdata].[Metview2017_hourly]" \
       "where SiteNumber not in ('300A')" \
       "order by SiteNumber,[sampdatetime] asc"

df = pd.read_sql_query(sql, engine)
df = df.fillna(method='ffill') ##remove NA vals
df['timeunix'] = df['sampdatetime'].astype(np.int64) / 10**11 ##create unix time field
times = df['timeunix'].unique()


##create empty arrays to which data will be appended
emptyWindSpeed = np.empty((0, 849, 1123))
emptyTemperature = np.empty((0, 849, 1123))
emptyWindDir = np.empty((0, 849, 1123))


for t in times[0:23]: ##run for first 24 hours
    print ('start loop ')
    mask = df['timeunix'] == t
    df2 = df.loc[mask]
    dt = pd.to_datetime(df2['timeunix'].head(1) * 10 ** 11)
    print ('coverting data to array for ts ' + str(dt))
    windSpeedInterpolate = np.array(df2['avgWindSpeed'])
    tempInterpolate = np.array(df2['avgTemp'])
    windDirInterpolate = np.array(df2['avgWindDir'])
    print ('interpolating to grid')
    gridWindSpeed = griddata(pnts, windSpeedInterpolate, (grid_x, grid_y), method='nearest')
    print ('appending wind speed')
    emptyWindSpeed = np.append(emptyWindSpeed, gridWindSpeed.reshape(1,849,1123), axis=0)
    gridTemperature = griddata(pnts, tempInterpolate, (grid_x, grid_y), method='nearest')
    print('appending temperature')
    emptyTemperature = np.append(emptyTemperature, gridTemperature.reshape(1,849,1123), axis=0)
    print('appending wind direction')
    gridWindDir = griddata(pnts, windDirInterpolate, (grid_x, grid_y), method='nearest')
    emptyWindDir = np.append(emptyWindDir, gridWindDir.reshape(1,849,1123), axis=0)
    print (emptyWindSpeed.shape)
    print (emptyTemperature.shape)
    print(emptyWindDir.shape)

np.save('C:/files/EED_ML_LDRD/climatedatarrays/windspeed.npy', emptyWindSpeed)
np.save('C:/files/EED_ML_LDRD/climatedatarrays/temperature.npy', emptyTemperature)
np.save('C:/files/EED_ML_LDRD/climatedatarrays/winddir.npy', emptyWindDir)


##show sub plots
print('plotting data')
plt.subplot(221)
plt.plot(xcoords - xcoords.min(), ycoords - ycoords.min(),  'bo')
plt.title('Met stations')
plt.ylabel('ycoord state plane')
plt.xlabel('xcoord state plane')
plt.subplot(222)
plt.imshow(gridWindSpeed)
plt.title('Original')
plt.subplot(223)
plt.imshow(gridTemperature)
plt.title('Nearest')
plt.subplot(224)
plt.imshow(gridWindDir)
plt.title('Linear')