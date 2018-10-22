#!/bin/bash
if [ ! -d data ]
then
	wget http://maartenmarx.nl/teaching/zoekmachines/Data/goeievraag.zip
	unzip goeievraag.zip
	mv goeievraag data
	cd data
	unzip '*.zip'
	rm *.zip
	cd ..
	rm goeievraag.zip
fi

if [ -e data/questions.csv ]
then 
	head -1426 data/questions.csv > data/q1000.csv
fi

if [ -e data/answers.csv ]
then
	head -3657 data/answers.csv > data/a1000.csv
fi
