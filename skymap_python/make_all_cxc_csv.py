import Image
import codecs
import sys
import os
import re
import csv
import coords
import mimetypes
import inspect
import urllib2
from pyavm import AVM,NoAVMPresent
from xml.sax.saxutils import escape

VALID_MIME_TYPES = ['image/tiff']
BASE_RESOURCE_URL = 'http://chandra.harvard.edu/photo/'

#define AVM archive top-level directories
avmdirs = ['2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999']
records=[]
counter = 0

#open data file for cross referencing information
for line in open('/Volumes/EPO/ImageArchive/obsids-releases.txt').readlines():
    thmb_flag = 0
    filepath = line.split('\t')[0]
    checkimg = line.split('\t')[4]
    
    i=0
    # Get the path to all files in each subdirectory
    item = os.path.join(filepath.strip(),checkimg.strip())
    
    if checkimg != 'None':
        
        URL = 'None'
        Date = 'None'
        Name = 'None'
        Img = 'None'
        Cat = 'None'
        RA ='None'
        DEC = 'None'
        Title = 'None'
        Headline = 'None'
        Type = 'None'
        Dist = 'None'
        
        # Check the mime type of the file
        #mime_type = mimetypes.guess_type(item)[0]
        #if mime_type in VALID_MIME_TYPES and i == 0:
        if i==0:

                # Grab AVM for the file if it exists
                try:
                        print item

                        #error catch
                        if os.path.split(item)[0] == '2004/darkenergy':
                            item = '2004/darkenergy/abell2029_xray.jpg'
                        if os.path.split(item)[0] == '2001/orion_mov':
                            item = '2001/orion_mov/orion_mov.jpg'
                            
                        #jpegs seem to work more consistently with pyavm - use the main jpg image for AVM
                        filename, fileext = os.path.splitext(item)
                        try:
                            avm = AVM(filename+'.jpg')
                            ThmbLink = BASE_RESOURCE_URL+filename+'_250.jpg'
                            ThmbLink2 = BASE_RESOURCE_URL+filename+'_420.jpg'
                            ThmbLink3 = BASE_RESOURCE_URL+filename+'_map.jpg'
                            if os.path.split(item)[0] == '2004/darkenergy':
                                item = '2004/darkenergy/darkenergy_3panel.tif'
                            
                        except:
                            check = 'trouble reading AVM: '+item
                            badfiles.append(check)
                            continue

                        URL = (avm.ReferenceURL).strip('\n')
                        Date = avm.Date
                        try:
                            Name = avm.Subject.Name[0]
                        except:
                            print "Missing Name:" +item
                            continue
                        
                        try:
                            f = urllib2.urlopen(urllib2.Request(ThmbLink3))
                            Img = ThmbLink
                        except:
                            Img = avm.ResourceURL
                            thmb_flag += 1

                        if Img == avm.ResourceURL:
                            try:
                                f = urllib2.urlopen(urllib2.Request(ThmbLink))
                                Img = ThmbLink
                            except:
                                Img = avm.ResourceURL
                                thmb_flag += 1
                            
                        if Img == avm.ResourceURL:
                            try:                                
                                f = urllib2.urlopen(urllib2.Request(ThmbLink2))
                                Img = ThmbLink2
                            except:
                                Img = avm.ResourceURL
                                thmb_flag += 1

                        if thmb_flag == 2:
                            print "Missing both thumbnails! (" + ThmbLink + "): " + item

                        Cat = re.split("\.",avm.Subject.Category[0])
                        Title = avm.Title[0].replace('\"','\'')

                        try:
                            Headline = avm.Headline.replace('\"','\'')
                        except:
                            print 'Missing Headline:' +item
                            continue
                        
                        #coordinate conversions
                        try:
                            RA = avm.Spatial.ReferenceValue[0]
                            DEC = avm.Spatial.ReferenceValue[1]
                            l,b = coords.eq2gal(RA,DEC, b1950=False, dtype='f8')
                            Xgal,Ygal = coords.radec2aitoff(l,b)
                            Xeq, Yeq = coords.radec2aitoff(RA, DEC)
                        except:
                            print 'Missing spatial info:' +item
                            continue
                        
                        #category parser
                        if Cat[0] == "A":
                            Dist = "SS"
                        if Cat[0] == "B":
                            Dist = "MW"
                        if Cat[0] == "C":
                            Dist = "LU"
                        if Cat[0] == "D":
                            Dist = "EU"
                        if Cat[1] == "1":
                            Type = "Planet"
                        if Cat[1] == "2":
                            Type = "IP"
                        if Cat[1] == "3":
                            Type = "Star"
                            try:
                                if Cat[2] == "1":
                                    if Cat[3] == "7":
                                        SubType = "WD"
                                    if Cat[3] == "8":
                                        SubType = "SN"
                                    if Cat[3] == "9":
                                        SubType = "NS"
                                    if Cat[3] == "10":
                                        SubType = "BH"
                            except:
                                continue
                        if Cat[1] == "4":
                            Type = "Nebula"
                            try:
                                if Cat[2] == "1":
                                    if Cat[3] == "1":
                                        SubType = "ISM"
                                    if Cat[3] == "2":
                                        SubType = "SF"
                                    if Cat[3] == "3":
                                        SubType = "PN"
                                    if Cat[3] == "4":
                                        SubType = "SNR"
                                    if Cat[3] == "5":
                                        SubType = "Jet"
                            except:
                                continue
                        if Cat[1] == "5":
                            Type = "Galaxy"
                            try:
                                if Cat[2] == "1":
                                    if Cat[3] == "1":
                                        SubType = "Spiral"
                                    if Cat[3] == "2":
                                        SubType = "Barred"
                                    if Cat[3] == "3":
                                        SubType = "Lenticular"
                                    if Cat[3] == "4":
                                        SubType = "Elliptical"
                                    if Cat[3] == "5":
                                        SubType = "Ring"
                                    if Cat[3] == "6":
                                        SubType = "Irregular"
                                    if Cat[3] == "7":
                                        SubType = "Interacting"
                                    if Cat[3] == "8":
                                        SubType = "GravLens"
                                if Cat[2] == "2":
                                    if Cat[3] == "1":
                                        SubType = "Giant"
                                    if Cat[3] == "2":
                                        SubType = "Dwarf"
                                if Cat[2] == "3":
                                    if Cat[3] == "1":
                                        SubType = "Normal"
                                    if Cat[3] == "2":
                                        SubType = "AGN"
                                    if Cat[3] == "3":
                                        SubType = "Starburst"
                                    if Cat[3] == "4":
                                        SubType = "UL"
                            except:
                                continue
                        if Cat[1] == "6":
                            Type = "Cosmology"            

                        #coordinate conversions
                        l,b = coords.eq2gal(RA,DEC, b1950=False, dtype='f8')
                        Xgal,Ygal = coords.radec2aitoff(l,b)
                        Xeq, Yeq = coords.radec2aitoff(RA, DEC)

                        #construct output record
                        record = '\"%s\",\"%s\",\"%s\",%6.2f,%6.2f,%s,%s,%s,%s,%s,%s,\"%s\",\"%s\",%s,\"%s\",\"%s\",\"%s\"' % (Dist,Type,SubType,RA,DEC,RA,DEC,Xgal[0]*-1,Ygal[0],Xeq[0]*-1,Yeq[0],Title,Name,Date,URL,Headline,Img) 
                        records.append(record)
                        counter+=1

                except NoAVMPresent:
                        i=0
                        check = 'Missing all AVM: '+item
                        badfiles.append(check)
                        continue
  
#print out results
fl = codecs.open('cxc_sources.csv', 'a', 'utf8')
line = '\n'.join(records)
fl.write(line + u'\r\n')
fl.close()
print "Records processed: " + str(counter)

