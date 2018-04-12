#!/bin/bash

for i in {1..786}
do
	cd $i
	../getelec.sh
	cd ..
done
