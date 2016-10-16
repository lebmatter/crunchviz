from geocoder import osm, google
import time

loc=[]
fin = open('crunch\\static\\base_data\\companies.csv', 'r')
for line in fin:
    loc.append(line.split(',')[9])

sloc = set(loc)
sloc = list(sloc)
f = open('latl.csv', 'w')
wrong = []
for l in sloc:
    print "Getting osm for ", l
    # time.sleep(1)
    latl = google(l, key="AIzaSyDTodiKfrl8BWjpGCVdAR72VunifJQPtcI")
    print latl.latlng
    try:
        line = '{},{},{}\n'.format(l,latl.latlng[0], latl.latlng[1])
        f.write(line)
    except:
        print "failed to write"
        wrong.append(l)

print wrong
f.close()
fin.close()
