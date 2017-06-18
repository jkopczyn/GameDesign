#!/usr/bin/python
import sys
import os

OUTPATH = "./cardfile/"
BASEPATH = "template.eps"
INPATH = "cardlist.txt"

#take a line and break it down into individual symbols
def process(spec):
	accum = "\n"
	symbols = spec.split()
	while symbols:
		#format: shape orientation color
		color = symbols.pop()
		position = symbols.pop()
		shape = symbols.pop()
		accum += " ".join([
                    "gsave",
                    orientlookup(position),
                    colorlookup(color),
                    shapelookup(shape),
                    "grestore",
                    "\n"])
	return accum

def shapelookup(char):
    if char in [str(n) for n in range(8)]:
        return "type"+char
    return 'you broke it you fucker (shape)'

def orientlookup(char):
    if char in {'0','1','2','3'}:
        return char
    return 'you broke it you fucker (orientation)'

def colorlookup(char):
    #color: B, W, G, for black, white, gray
    return {'B': '0', 'G': '1', 'W': '2'}.get(
            char, 'you broke it you fucker (color)')


def main(inpath=None):
    if not inpath:
        inpath = INPATH
    base = open(BASEPATH)
    template = base.read()
    base.close()
    cardlist = open(inpath)
    i=1
    while(True):
        card = cardlist.readline()
        if card == "" :
            cardlist.close()
            break
        cardprint = open(OUTPATH+str(i).rjust(5,'0')+'.eps','w+')
        cardprint.write(template) #copy the template into the file

        psout = process(card);
        cardprint.write(psout) #create the card-specific PS
        cardprint.close()
        i+=1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
