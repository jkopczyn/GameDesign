#!/usr/bin/python
import makeps

if __name__ == '__main__':
  outpath = "./cardfile/bordered/"
  templatedir = "./eps_partials/"
  inpath = "cardlist.txt"
  makeps.main(outpath, inpath, templatedir, True)
