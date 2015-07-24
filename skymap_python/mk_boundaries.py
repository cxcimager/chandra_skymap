import codecs
import sys
import os
import re
import csv
import coords
from os.path import basename
import json

def main(filename):
    j = 0;
    outCONST = ["Andromeda","Antlia","Apus","Aquarius","Aquila","Ara ","Aries","Auriga","Bootes","Caelum","Camelopardalis","Cancer ","Canes Venatici","Canis Major ","Canis Minor ","Capricornus ","Carina ","Cassiopeia","Centaurus","Cepheus","Cetus ","Chamaeleon","Circinus","Columba","Coma Berenices","Corona Australis","Corona Borealis","Corvus","Crater","Crux","Cygnus ","Delphinus","Dorado","Draco","Equuleus","Eridanus","Fornax","Gemini","Grus","Hercules","Horologium","Hydra","Hydrus","Indus","Lacerta","Leo ","Leo Minor","Lepus","Libra","Lupus","Lynx","Lyra","Mensa","Microscopium","Monoceros","Musca","Norma","Octans","Ophiuchus","Orion","Pavo","Pegasus","Perseus","Phoenix","Pictor","Pisces","Piscis Austrinus","Puppis","Pyxis","Reticulum","Sagitta ","Sagittarius","Scorpius","Sculptor","Scutum","Serpens","Sextans","Taurus","Telescopium","Triangulum ","Triangulum Australe","Tucana","Ursa Major ","Ursa Minor ","Vela","Virgo","Volans","Vulpecula"];
    
    #print out results
    fl = codecs.open('GalBound.json', 'w', 'utf8')
    fl2 = codecs.open('EqBound.json', 'w', 'utf8')
    fl3 = codecs.open('RADecBound.json', 'w', 'utf8')
    fl4 = codecs.open('TestBound.json', 'w', 'utf8')
    fl.write("{\n\t\"boundaries\": [\n")
    fl2.write("{\n\t\"boundaries\": [\n")
    fl3.write("{\n\t\"boundaries\": [\n")
    fl4.write("{\n\t\"boundaries\":\n[\n")

    json_data=open(filename)
    data = json.load(json_data)

    while (j < 88):
        i = 1;
        records=[]
        records2=[]
        records3=[]
        records4=[]
        while (i < len(data["boundaries"][j])-2):

            RA = data["boundaries"][j][i]
            DEC = data["boundaries"][j][i+1]         

            l,b = coords.eq2gal(RA,DEC, b1950=False, dtype='f8')
            Xgal,Ygal = coords.radec2aitoff(l,b)
            Xeq,Yeq = coords.radec2aitoff(RA,DEC)

            #construct output record
            record = '%s,%s' % (Xgal[0]*-1,Ygal[0]) 
            records.append(record)
            record2 = '%s,%s' % (Xeq[0]*-1,Yeq[0]) 
            records2.append(record2)
            record3 = '%s,%s' % (RA,DEC) 
            records3.append(record3)
            record4 = '{"x":'+str(Xgal[0]*-1)+',"y":'+str(Ygal[0])+'}'
            records4.append(record4)
            i = i+2

        line = ','.join(records)
        fl.write('[\"' + outCONST[j] + '\",')
        line2 = ','.join(records2)
        fl2.write('[\"' + outCONST[j] + '\",')
        line3 = ','.join(records3)
        fl3.write('[\"' + outCONST[j] + '\",')
        line4 = ','.join(records4)
        fl4.write('{"name":\"' + outCONST[j] + '\","box":[')
        if (j < 87):
            fl.write(line + '],\n')
            fl2.write(line2 + '],\n')
            fl3.write(line3 + '],\n')
            fl4.write(line4 + ']},\n')
        if (j == 87):
            fl.write(line + ']\n')
            fl2.write(line2 + ']\n')
            fl3.write(line3 + ']\n')
            fl4.write(line4 + ']}\n')
        j = j+1

    fl.write("\n\t]\n}")
    fl2.write("\n\t]\n}")
    fl3.write("\n\t]\n}")
    fl4.write("]\n}")
    fl.close()
    fl2.close()
    fl3.close()
    fl4.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python %(script)s <filename>' % {"script": inspect.getfile( inspect.currentframe() ) }
	else:
		main( sys.argv[1] )


