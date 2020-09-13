from skyfield.api import load

planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']

ts = load.timescale()
t = ts.now()
astrometric = earth.at(t).observe(mars)
ra, dec, distance = astrometric.radec()

print(t)

import skyfield
import datetime
import json

class TSEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, skyfield.timelib.Time):
            return {"__TS__": obj.utc_datetime().timestamp()}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def as_TS(dct):
    if '__TS__' in dct:
        return ts.from_datetime(datetime.datetime.fromtimestamp(dct['__TS__']).replace(tzinfo=skyfield.api.utc))
    return dct

j = json.dumps([t, "a"], cls=TSEncoder)
print(j)
t2 = json.loads(j, object_hook=as_TS)
print(t2)
