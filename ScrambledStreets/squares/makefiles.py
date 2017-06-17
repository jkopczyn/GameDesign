#!/usr/bin/python
import shutil
import os

outpath = "./cardfile/"
basepath = "template.eps"
inpath = "cardlist.txt"
base = open(basepath) #the template
template = base.read()
base.close() #there is nothing more to see
cardlist = open(inpath)

#take a line and break it down into individual symbols
def process(spec):
	accum = "\n"
	symbols = spec.split()
	while symbols:
		#format: shape orientation color
		accum += "gsave "
		color = symbols.pop()
		position = symbols.pop()
		shape = symbols.pop()
		accum+= orientlookup(position)
		accum+= colorlookup(color)
		accum+= shapelookup(shape)
		accum+="grestore \n"
	return accum
	#now do something with those symbols.
	#for what to do, punt to lookup()

def shapelookup(char):
    if char in [str(n) for n in range(8)]:
        return "type"+char+" "
    return 'you broke it you fucker (shape)'

def orientlookup(char):
    if char in {'0','1','2','3'}:
        return char+" "
    return 'you broke it you fucker (orientation)'

def colorlookup(char):
    #color: B, W, G, for black, white, gray
    if 'B'==char:
        return "0 "
    if 'G'==char:
        return "1 "
    if 'W'==char:
        return "2 "
    return 'you broke it you fucker (color)'

#format: shape orientation color
#	type: V for short curve: smallcurve, L for big curve: tallcurve, C for both on a side: semicirc
#S for distinct sides: diag, I for vertical: vertline, _ for horizontal: horizline
#	orientation: 0 is BL, 1 is TL, 2 is TR, 3 is BR
#for things that are left-right symmetric, 0=3, 1=2
#for things that are top-bottom symmetric, 0=1, 2=3
#if it's on a short edge, that's the one that goes on the B/T
#	color: B, W, G, for black, white, gray
#

i=1

while(True):
    card = cardlist.readline() #get the next card description
    if card == "" : #if it's empty, close the file and exit loop
        cardlist.close()
        break
    psout = process(card); #turn that description into PS
    cardprint = open(outpath+str(i)+'.eps','w+') #the file for the card
    cardprint.write(template) #copy the template into the file
    cardprint.write(psout) #create the specific card PS
    cardprint.close() #and it's done
    i+=1 #so that each file is different

