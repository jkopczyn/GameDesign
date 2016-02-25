g = lambda s: "./headers/"+s
sources = ["net.anastigmatix.MetaPre","net.anastigmatix.filter","DSCDecode","net.anastigmatix.StreamIO","net.anastigmatix.BinaryIO","net.anastigmatix.Import","net.anastigmatix.PNG"]
sources = map(g,sources)
dest = open("importwithdependencies.eps",'w')
for s in sources:
	f=open(s)
	dest.write(f.read()+"\n")
	f.close()
dest.close()
