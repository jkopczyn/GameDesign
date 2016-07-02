#!/usr/bin/python
import shutil
import os
from subprocess import call

def process(spec):
    accum = "\n"
    data_dict = parameterize_line(spec)
    symbols = data_dict['symbols']
    name = data_dict['name']
    points = data_dict['points']
    accum+="("+points+") putscore \n"
    outof = len(symbols) #symbols will be placed as the 1st 'out of' n
    if outof <= 7:
        for (n,s) in enumerate(symbols, start=1):
            if len(s) == 1 :
                accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placegood\n"
            elif len(s) == 3 and s[1]=='/':
                accum +="{"+lookup(s[0])+"top} "+"{"+lookup(s[2])+"bot} "+str(n)+" "+str(outof)+" placesplit\n"
            else:
                raise "error, one of the symbols wasn't a real symbol"
    else:
        for (n,s) in enumerate(symbols, start=1):
            if not len(s) == 1 :
                raise "error, one of the symbols wasn't a valid symbol for this length"
            if n< (outof/2):
                accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placeup\n"
            elif n < (outof -1):
                accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placedown\n"
            else:
                accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placemid\n"
    accum += "("+name+") putname"
    return accum

def parameterize_line(line):
    tokens = iter(line.split())
    data = {'symbols':[]}
    for t in tokens:
        try:
            data['points'] = str(int(t))
            break
        except ValueError:
            data['symbols'].append(t)
    data['name'] = ' '.join(tokens)
    return data


#A B C  diamond , halfcirc , square
# M N   ecks, cross
# U V   hex, star
def lookup(char):
    if 'A'==char:
        return "diamond"
    if 'B'==char:
        return "halfcirc"
    if 'C'==char:
        return "square"
    if 'M'==char:
        return "ecks"
    if 'N'==char:
        return "cross"
    if 'U'==char:
        return "hex"
    if 'V'==char:
        return "star"
    if '>'==char:
        return "convert"
    if '^'==char:
        return "convert"
    #return "error, ^ should have been caught earlier"
    #else
    return 'you broke it you fucker'


def template(templatedir, bordered=False, zones=False):
    template = ""
    curr = open(templatedir+'header.eps', 'r')
    template += curr.read()
    curr.close()
    if bordered:
        curr = open(templatedir+'borders.eps', 'r')
        template += curr.read()
        curr.close()
    if zones:
        curr = open(templatedir+'zones.eps', 'r')
        template += curr.read()
        curr.close()
    curr = open(templatedir+'helper_functions.eps', 'r')
    template += curr.read()
    curr.close()
    curr = open(templatedir+'coordinate_system.eps', 'r')
    template += curr.read()
    curr.close()
    if zones:
        curr = open(templatedir+'zonesconvert.eps', 'r')
        template += curr.read()
        curr.close()
    return template

def main(outpath, inpath, templatedir, bordered=False, zones=False):
    templatestring = template(templatedir, bordered, zones)
    cardlist = open(inpath)
    i=1
    while(True):
        card = cardlist.readline() #get the next card description
        if card == "" : #if it's empty, close the file and exit loop
            cardlist.close()
            break
	psout = process(card); #turn that description into PS
	cardprint = open('temp.eps','w')
	cardprint.write(templatestring) #copy the template into the file
	cardprint.write(psout) #create the specific card PS
	cardprint.close() #and it's done
	call(["eps2eps", "temp.eps", outpath+str(i)+'.eps'])
	#the file for the card
	i+=1 #so that each file is different

if __name__ == '__main__':
    #run directly
    outpath     = "./cardfile/"
    templatedir = "./eps_partials/"
    inpath      = "cardlist.txt"
    main(outpath, inpath, templatedir, zones=True)
