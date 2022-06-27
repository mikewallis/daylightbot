#!/usr/bin/env python3
# coding: utf-8

# libraries
from astroplan import Observer
from astropy.time import Time
import datetime
from astroplan import download_IERS_A
import numpy as np
import astropy.units as u
import getopt,sys

def daylength(dayOfYear, lat):
  latInRad = np.deg2rad(lat)
  declinationOfEarth = 23.45*np.sin(np.deg2rad(360.0*(284.25+dayOfYear)/365))
  if -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) <= -1.0:
      return 24.0
  elif -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) >= 1.0:
      return 0.0
  else:
      hourAngle = np.rad2deg(np.arccos(-np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth))))
      return int((2.0*hourAngle/15.0)*(3600))

def main(argv):

    date_arg=''
    lat_arg=''
    long_arg=''

    try:
        opts,args = getopt.getopt(argv,"hd:l:g:",["date=","lat=","long="])
    except getopt.GetoptError:
            print("usage: daylight.py (--date <YYYY-mm-dd>) (--lat <latitude>) (--long <longitude>)")

    for opt,arg in opts:
            if opt in ("-h", "--help"):
                print("usage: daylight.py (--date <YYYY-mm-dd>) (--lat <latitude>) (--long <longitude>)")
                sys.exit()
            elif opt in ("-d", "--date"):
                date_arg = arg
            elif opt in ("-l","--lat"):
                lat_arg = arg
            elif opt in ("-g","--long"):
                long_arg = arg

    if date_arg:
        today=datetime.datetime.strptime(date_arg,"%Y-%m-%d")
#        print("setting date_arg to "+str(today))
    else:
        today=datetime.date.today()
#        print("setting date_arg to default ("+str(today)+")")

    today_date=today.strftime('%Y-%m-%d')
    today_day=int(today.strftime('%j'))-1

    if today_day % 14 == 0:
        download_IERS_A()

    if lat_arg:
        actual_lat=float(lat_arg)
    else:
        actual_lat=55.9533
    if long_arg:
        actual_long=float(long_arg)
    else:
        actual_long=-3.1883

    loc = Observer(latitude=actual_lat*u.deg, longitude=actual_long*u.deg, elevation=0*u.m,timezone="UTC") 

    t = Time('{} 12:00:00'.format(today_date), precision=0)
    sun_rise = (loc.sun_rise_time(t, which="nearest"))
    sun_set = (loc.sun_set_time(t, which="nearest"))

    sunup = str(sun_rise.iso)
    sundown = str(sun_set.iso)

    today_daylight=datetime.timedelta(seconds=daylength(today_day,actual_lat),microseconds=0)
    daylight = str(today_daylight)

    log_message="day "+str(today_day)+" | lat: "+str(actual_lat)+" | long: "+str(actual_long)+" | daylight: "+daylight+" | dawn: "+ sunup.split()[1].split('.')[0] + " | dusk: " + sundown.split()[1].split('.')[0]

    print (log_message)


if __name__ == "__main__":
    main(sys.argv[1:])

