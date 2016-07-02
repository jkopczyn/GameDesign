#!/usr/bin/python
import shutil
import os
from subprocess import call

def process(params):
    accum = "\n"
    symbols = params['symbols']
    name = params['name']
    points = params['points']
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
    map_dict = {
        'A': "diamond", 'B': "halfcirc", 'C': "square", 'M': "ecks",
        'N': "cross", 'U': "hex", 'V': "star", '>': "convert",'^': "convert",
    }
    return map_dict.get(char, 'you broke it')

def append_file(before, directory, target_file):
    with open(directory+target_file, 'r') as f:
        after = before + f.read()
    return after

def template(templatedir, bordered=False, zones=False):
    template = append_file("", templatedir, 'header.eps')
    if bordered:
        template = append_file(template, templatedir, 'borders.eps')
    if zones:
        template = append_file(template, templatedir, 'zones.eps')
    template = append_file(template, templatedir, 'helper_functions.eps')
    template = append_file(template, templatedir, 'coordinate_system.eps')
    if zones:
        template = append_file(template, templatedir, 'zonesconvert.eps')
    return template

def main(outpath, inpath, templatedir, bordered=False, zones=False):
    templatestring = template(templatedir, bordered, zones)
    cardlist = open(inpath)

    temp_file = 'temp.eps'
    blank_name_counter=[1]
    while(True):
        card = cardlist.readline() #get the next card description
        if card == "" : #if it's empty, close the file and exit loop
            cardlist.close()
            break
        params = parameterize_line(card)
        psout = process(params); #turn that description into PS
        create_simple_eps(temp_file, templatestring, psout)
        call(["eps2eps", temp_file, filename(outpath, params['name'], blank_name_counter)])

def create_simple_eps(target_file, template, unique_parts):
    f = open(target_file, 'w')
    f.write(template)
    f.write(unique_parts)
    f.close

def filename(outpath, name, reference_to_idx_of_unnamed):
    to_fill = outpath+"{}.eps"
    if name:
        return to_fill.format(name)
    else:
        blank_name= str(reference_to_idx_of_unnamed[0])
        reference_to_idx_of_unnamed[0]+=1
        return to_fill.format(blank_name)

if __name__ == '__main__':
    #run directly
    outpath     = "./cardfile/"
    templatedir = "./eps_partials/"
    inpath      = "cardlist.txt"
    main(outpath, inpath, templatedir, zones=True)
