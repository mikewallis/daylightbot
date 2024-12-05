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

The rest of the code is a couple of functions from Astroplan (https://astroplan.readthedocs.io/en/latest/index.html) to get some times for sunrise/set, logic for turning those numbers into human-readable times (because astrological time is not the same as what most humans understand time to be), some pseudorandom code for producing the tweets that make this at least look Turing-compliant and the logic for tweeting (TweePY) and logging everything.

I don't need to provide all the tweepy and human-interest tweet generating stuff, if you're reading this you're more than capable of coming up with your own interface. So instead, have the command-line version. Still needs Astroplan and datetime (`pip install astroplan datetime` will sort out all the dependencies) to work but you'll get a useful output. If you're using python newer than 3.6 (because you're using atproto or something) you might also need to install astropy at the end, because astroplan sometimes doesn't play nicely with newer versions of numpy.

Usage: `daylight.py <-d|--date YYYY-MM-DD> <-l|--lat LATITUDE> <-g|--long LONGITUDE>` - eg: `daylight.py --date 2022-11-09 --lat 55.95` will return data for the 9th of November at the latitude of Edinburgh. Not specifying either will give the data for the current day in Edinburgh, because I'm lazy and that's where my office is. Error handling is (so far) non-existant, don't put in illegal dates or claim you're at latitude -1, or something. And remember: the output is in UTC. If you're in Seattle it'll tell you dawn is in the middle of the night. It isn't.

Want to get the UTC dawn/dusk times for every full degree of latitude from Lands End (~50N) to John O'Groats (~59N)? Bash loops are your friends. (note: longitude default to 3.18W, because cf. "Edinburgh", "office", and "lazy" above, so change longitude if you need to-the-second precision)

![FJxpTsOXIAITPIo](https://user-images.githubusercontent.com/14231683/150778881-4997d4d4-e963-402a-af82-48c742a00106.png)

Want something similar, only for a range of dates? Bash loops. Want to do different dates and different longitutes? Nested bash loops. 

I'll make timezones an option in a future version.

[1] Forsythe et al., "A model comparison for daylength as a function of latitude and day of year", Ecological Modelling, 1995. (https://www.sciencedirect.com/science/article/pii/030438009400034F)
