import codecs
import sys
import os
import re
import csv
import coords
from os.path import basename

def main(filename):
    records=[]

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            RA = coords.ra_parse(row[0])
            DEC = float(row[1])
            if row[2] == "AND":
                outCONST = "Andromeda"
            elif row[2] == "ANT":
                outCONST = "Antlia"
            elif row[2] == "APS":
                outCONST = "Apus"
            elif row[2] == "AQR":
                outCONST = "Aquarius"
            elif row[2] == "AQL":
                outCONST = "Aquila"
            elif row[2] == "ARA":
                outCONST = "Ara"
            elif row[2] == "ARI":
                outCONST = "Aries"
            elif row[2] == "AUR":
                outCONST = "Auriga"
            elif row[2] == "BOO":
                outCONST = "Bootes"
            elif row[2] == "CAE":
                outCONST = "Caelum"
            elif row[2] == "CAM":
                outCONST = "Camelopardalis"
            elif row[2] == "CNC":
                outCONST = "Cancer"
            elif row[2] == "CVN":
                outCONST = "Canes Venatici"
            elif row[2] == "CMA":
                outCONST = "Canis Major"
            elif row[2] == "CMI":
                outCONST = "Canis Minor"
            elif row[2] == "CAP":
                outCONST = "Capricornus"
            elif row[2] == "CAR":
                outCONST = "Carina"
            elif row[2] == "CAS":
                outCONST = "Cassiopeia"
            elif row[2] == "CEN":
                outCONST = "Centaurus"
            elif row[2] == "CEP":
                outCONST = "Cepheus"
            elif row[2] == "CET":
                outCONST = "Cetus"
            elif row[2] == "CHA":
                outCONST = "Chamaeleon"
            elif row[2] == "CIR":
                outCONST = "Circinus"
            elif row[2] == "COL":
                outCONST = "Columba"
            elif row[2] == "COM":
                outCONST = "Coma Berenices"
            elif row[2] == "CRA":
                outCONST = "Corona Austrina"
            elif row[2] == "CRB":
                outCONST = "Corona Borealis"
            elif row[2] == "CRV":
                outCONST = "Corvus"
            elif row[2] == "CRT":
                outCONST = "Crater"
            elif row[2] == "CRU":
                outCONST = "Crux"
            elif row[2] == "CYG":
                outCONST = "Cygnus"
            elif row[2] == "DEL":
                outCONST = "Delphinus"
            elif row[2] == "DOR":
                outCONST = "Dorado"
            elif row[2] == "DRA":
                outCONST = "Draco"
            elif row[2] == "EQE":
                outCONST = "Equules"
            elif row[2] == "ERI":
                outCONST = "Eridanus"
            elif row[2] == "FOR":
                outCONST = "Fornax"
            elif row[2] == "GEM":
                outCONST = "Gemini"
            elif row[2] == "GRU":
                outCONST = "Grus"
            elif row[2] == "HER":
                outCONST = "Hercules"
            elif row[2] == "HOR":
                outCONST = "Horologium"
            elif row[2] == "HYA":
                outCONST = "Hydra"
            elif row[2] == "HYI":
                outCONST = "Hydrus"
            elif row[2] == "IND":
                outCONST = "Indus"
            elif row[2] == "LAC":
                outCONST = "Lacerta"
            elif row[2] == "LEO":
                outCONST = "Leo"
            elif row[2] == "LMI":
                outCONST = "Leo Minor"
            elif row[2] == "LEP":
                outCONST = "Lepus"
            elif row[2] == "LIB":
                outCONST = "Libra"
            elif row[2] == "LUP":
                outCONST = "Lepus"
            elif row[2] == "LYN":
                outCONST = "Lynx"
            elif row[2] == "LYR":
                outCONST = "Lyra"
            elif row[2] == "MEN":
                outCONST = "Mensa"
            elif row[2] == "MIC":
                outCONST = "Microscopium"
            elif row[2] == "MON":
                outCONST = "Monoceros"
            elif row[2] == "MUS":
                outCONST = "Musca"
            elif row[2] == "NOR":
                outCONST = "Norma"
            elif row[2] == "OCT":
                outCONST = "Octans"
            elif row[2] == "OPH":
                outCONST = "Ophiuchus"
            elif row[2] == "ORI":
                outCONST = "Orion"
            elif row[2] == "PAV":
                outCONST = "Pavo"
            elif row[2] == "PEG":
                outCONST = "Pegasus"
            elif row[2] == "PER":
                outCONST = "Perseus"
            elif row[2] == "PHE":
                outCONST = "Phoenix"
            elif row[2] == "PIC":
                outCONST = "Pictor"
            elif row[2] == "PSC":
                outCONST = "Pisces"
            elif row[2] == "PSA":
                outCONST = "Piscis Austrinus"
            elif row[2] == "PUP":
                outCONST = "Puppis"
            elif row[2] == "PYX":
                outCONST = "Pyxis"
            elif row[2] == "RET":
                outCONST = "Reticulum"
            elif row[2] == "SGE":
                outCONST = "Sagitta"
            elif row[2] == "SGR":
                outCONST = "Sagittarius"
            elif row[2] == "SCO":
                outCONST = "Scorpius"
            elif row[2] == "SCL":
                outCONST = "Sculptor"
            elif row[2] == "SCT":
                outCONST = "Scutum"
            elif row[2] == "SER":
                outCONST = "Serpens"
            elif row[2] == "SEX":
                outCONST = "Sextans"
            elif row[2] == "TAU":
                outCONST = "Taurus"
            elif row[2] == "TEL":
                outCONST = "Telescopium"
            elif row[2] == "TRI":
                outCONST = "Triangulum"
            elif row[2] == "TRA":
                outCONST = "Triangulum Austrinus"
            elif row[2] == "TUC":
                outCONST = "Tucana"
            elif row[2] == "UMA":
                outCONST = "Ursa Major"
            elif row[2] == "UMI":
                outCONST = "Ursa Minor"
            elif row[2] == "VEL":
                outCONST = "Vela"
            elif row[2] == "VIR":
                outCONST = "Virgo"
            elif row[2] == "VOL":
                outCONST = "Volanus"
            elif row[2] == "VUL":
                outCONST = "Vulpecula"                
                
            l,b = coords.eq2gal(RA,DEC, b1950=False, dtype='f8')
            Xgal,Ygal = coords.radec2aitoff(l,b)
            Xeq,Yeq = coords.radec2aitoff(RA,DEC)

            #construct output record
            record = '%s,%s,%s,%s,%s,%s,\"%s\",\"%s\"' % (RA,DEC,Xgal[0]*-1,Ygal[0],Xeq[0]*-1,Yeq[0],row[2],outCONST) 
            records.append(record)
            
    #print out results
    fl = codecs.open('constellationboundaries_formatted.csv', 'a', 'utf8')
    line = '\n'.join(records)
    fl.write(line + u'\r\n')
    fl.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python %(script)s <filename>' % {"script": inspect.getfile( inspect.currentframe() ) }
	else:
		main( sys.argv[1] )


