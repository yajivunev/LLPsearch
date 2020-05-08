
def trimfile(file_name):
    trimmed = {}
    with open(file_name,"r+") as f:
        line = f.readline()
        while line != "TileInfoLoader       INFO Handling EndRun incident\n":
                if len(line.split())>=3 and line.split()[2]=='######################################################################################':
                    lil = []
                    evno = int(line.split()[4])
                    line = next(f)
                    while line.split()[2]!='######################################################################################' and line != "TileInfoLoader       INFO Handling EndRun incident\n":
                        a = (line.split()[5])[:10]
                        if a[-2:]=='e-': 
                            a = a[:-2]
                            lil.append(a)
                        else: lil.append(a)
                        line = next(f)
                    trimmed[evno] = lil
                else: line = next(f)
    return trimmed

# makes channel-id to eta,phi,r,z,layer map
def Map(file_name):
    map = {}
    with open(file_name,"r") as f:
        line = f.readline()
        for line in f:
            map[line.split()[0]] = [float(line.split()[4]),float(line.split()[5]),float(line.split()[6])/10.,float(line.split()[7])/10.,int(line.split()[3])]
    return map

#making raw (channel id, e) cell level info dictionary, event-wise
def rawcellinfo(raw):
    cellinfo = {}
    for event in raw.keys():
        cellinfo[event]=[]
        for i in range(len(raw[event])):
            if i % 2 == 0:
                #if raw[event][i+1] == "-3.11957e-": cellinfo[event].append([raw[event][i],float(-3.11957)])
                #elif raw[event][i+1] == "-2.45564e-": cellinfo[event].append([raw[event][i],float(-2.45564)])
                cellinfo[event].append([raw[event][i],float(raw[event][i+1])])
    return cellinfo

#rawcellinfo to (energy, eta, phi, r, z, sample) cell info ,per event#
def cellinfo(rawcellinfo):
    cellinfo = {}
    fails = []
    for i in rawcellinfo.keys():
        cellinfo["%s" % i] = []
        for cell in rawcellinfo[i]:
            if not cell[0] in map: 
                fails.append(cell[0])
            else:
#            if cell[0] in map:
                cellinfo["%s" % i].append([cell[1],map[cell[0]][0],map[cell[0]][1],map[cell[0]][2],map[cell[0]][3],map[cell[0]][4]])
    print(len(fails))
    return cellinfo


map = Map("map.txt")

#aod10 = trimfile("AOD10.txt")
#cinfo = cellinfo(rawcellinfo(aod10))
#print("dicts made")

cinfo = {}
for i in range(1,21):
	cinfo.update(cellinfo(rawcellinfo(trimfile("AOD%s.txt" % i))))
	print("made dict %s" % i)
	print(len(cinfo.keys()))

#aod13 = trimfile("AOD13.txt")
#cinfo.update(cellinfo(rawcellinfo(aod13)))
print("all dicts made")
import msgpack

with open('cinfo.msgpack', 'wb') as outfile:
    msgpack.pack(cinfo, outfile)

print("pickled")
