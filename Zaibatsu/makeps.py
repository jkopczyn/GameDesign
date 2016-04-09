#!/usr/bin/python
import shutil
import os
from subprocess import call

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


def template(templatedir, bordered=False):
  template = ""
  curr = open(templatedir+'header.eps', 'r')
  template += curr.read()
  curr.close()
  if bordered:
    curr = open(templatedir+'borders.eps', 'r')
    template += curr.read()
    curr.close()
  curr = open(templatedir+'helper_functions.eps', 'r')
  template += curr.read()
  curr.close()
  curr = open(templatedir+'coordinate_system.eps', 'r')
  template += curr.read()
  curr.close()
  return template

def main(outpath, inpath, templatedir, bordered=False):
  templatestring = template(templatedir, bordered)
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
  main(outpath, inpath, templatedir)
