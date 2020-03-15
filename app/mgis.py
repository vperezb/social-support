import mgrs

latitude = 42.0
longitude = -93.0

c = mgrs.MGRS().toMGRS(latitude, longitude).decode('UTF-8')

print(c)