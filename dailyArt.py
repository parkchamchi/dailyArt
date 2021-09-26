from fetchArt import fetchArt
from formatArt import formatArt

art = fetchArt()
print("Got art...")
formatArt(art)
print("Done.")