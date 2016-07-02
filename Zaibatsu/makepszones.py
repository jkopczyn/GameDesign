#!/usr/bin/python
import makeps

if __name__ == '__main__':
  outpath = "./cardfile/zones/"
  templatedir = "./eps_partials/"
  inpath = "prunedcardlist.txt"
  makeps.main(outpath, inpath, templatedir, zones=True)
