#!/usr/bin/python
import shutil
import os

outpath = "./cardfile/rotate/"
basepath = "rotatedcardsbase.eps"
inpath = "prunedcardlist.txt"
base = open(basepath) #the template
template = base.read()
base.close() #there is nothing more to see
cardlist = open(inpath)



def process(spec):
	accum = "\n"
	symbols = spec.split()
	points = symbols.pop()
	accum+="("+points+") putscore \n"
	outof = len(symbols) #symbols will be placed as the 1st 'out of' n
	if outof <= 7:
		for (n,s) in enumerate(symbols, start=1):
			if len(s) == 1 :
				accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placegood\n"
			elif len(s) == 3 and s[1]=='/':	
				accum +="{"+lookup(s[0])+"top} "+"{"+lookup(s[2])+"bot} "+str(n)+" "+str(outof)+" placesplit\n"
			else:
				return "error, one of the symbols wasn't a real symbol"
		return accum
	else:
		for (n,s) in enumerate(symbols, start=1):
			if not len(s) == 1 :
				return "error, one of the symbols wasn't a valid symbol for this length"
			if n< (outof/2):
				accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placeup\n"
			elif n < (outof -1):
				accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placedown\n"
			else:
				accum +="{"+lookup(s)+"} "+str(n)+" "+str(outof)+" placemid\n"
		return accum

	#return spec+"\n"

#A B C  diamond , halfcirc , square

# M N   ecks, cross
# X Y   hex, star
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
	if 'X'==char or 'U'==char: #'X' is deprecated
		return "hex"
	if 'Y'==char or 'V'==char: #so is 'Y'
		return "star"
	if '>'==char:
		return "convert"
	if '^'==char:
		return "convert"
		#return "error, ^ should have been caught earlier"
	#else
	return 'you broke it you fucker'



i=1

while(True):
	card = cardlist.readline() #get the next card description
	if card == "" : #if it's empty, close the file and exit loop
		cardlist.close()
		break
	psout = process(card); #turn that description into PS
	cardprint = open(outpath+str(i)+'.eps','w') #the file for the card
	cardprint.write(template) #copy the template into the file
	cardprint.write(psout) #create the specific card PS 
	cardprint.close() #and it's done
	i+=1 #so that each file is different


