#!/bin/bash

python replace.py

for i in {1..40}
do
	##echo "$i"
	mkdir -p $i
	cp *.lib mut$i.inp sqv.pdb minrlx.inp $i
	cd $i
	../molaris_dna  < mut$i.inp > mut.out
	../molaris_dna  < minrlx.inp > minrlx.out

	cd ..
done




