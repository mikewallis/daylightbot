# daylightbot

Ah, daylightbot. For six months of the year every day gets longer, and I wanted to be reminded of this, so I created a bit of python that uses AstroPY to tell me official sunrise & sunset at my latitude, and an incredible bit of maths published in 1995[1] to calculate how much daylight you actually get. Seriously, I'm amazed that this was published so recently given that humans have been doing daylight maths for about twelve thousand years. Anyway, the code for this is quite elegant (needs numpy):
```
def daylength(dayOfYear, lat):
  latInRad = np.deg2rad(lat)
  declinationOfEarth = 23.45 * np.sin(np.deg2rad(360.0 * (283.0+dayOfYear)/366))
  if -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) <= -1.0:
      return 24.0
  elif -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) >= 1.0:
      return 0.0
  else:
      hourAngle = np.rad2deg(np.arccos(-np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth))))
      return int((2.0 * hourAngle/15.0) * (3600))
```
This returns daylength in seconds, which when applied to a timedelta can easily be transformed into HH:mm:ss

The rest of the code is a couple of functions from AstroPY to get some times for sunrise/set, logic for turning those numbers into human-readable times (because astrological time is not the same as what most humans understand time to be), some pseudorandom code for producing the tweets that make this at least look Turing-compliant and the logic for tweeting (TweePY) and logging everything.

[1] Forsythe et al., "A model comparison for daylength as a function of latitude and day of year", Ecological Modelling, 1995. (https://www.sciencedirect.com/science/article/pii/030438009400034F)
