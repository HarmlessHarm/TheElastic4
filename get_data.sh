wget http://maartenmarx.nl/teaching/zoekmachines/Data/goeievraag.zip
unzip goeievraag.zip
mv goeievraag data
cd data
unzip '*.zip'
rm *.zip
cd ..
rm goeievraag.zip
head -1000 data/questions.csv > data/q1000.csv
head -1000 data/answers.csv > data/a1000.csv