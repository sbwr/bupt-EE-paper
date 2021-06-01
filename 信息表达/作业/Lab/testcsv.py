import codecs  
from multiprocessing import Pool
 
import os
import re
import sys
import csv
 
if __name__ == '__main__' :
    infile = "./outSort"
    with open('Features.csv', 'wb+') as csvfile:
        csvfile.write(codecs.BOM_UTF8) 
        spamwriter = csv.writer(csvfile,dialect='excel')
        spamwriter.writerow(['Sign', 'Count', 'Feature', 'Info'])
        for each in [line for line in csvfile(infile)] :
            list = ['0']
            sublist1 = ['','','']
            sublist2 = ['','','']
            segs = each.split('\t')
            if not segs :
                break
            list.append(segs[0])
            list.append(segs[1])
            list.append(segs[2])
            if segs[3]:
                sublist1.append(segs[3])
            if segs[4]:
                sublist2.append(segs[4])
            spamwriter.writerow(list)
            spamwriter.writerow(sublist1)
            spamwriter.writerow(sublist2)
        
