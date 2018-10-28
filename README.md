# TheElastic4
Elastic Search assignment for the zoekmachines course at University of Amsterdam

#### Authors
| Name  | Stud. Nr.  |
|---|---|
| Harm Manders  | 10677186  |
| Kjeld Oostra  | 10748598  |
| Sander Hansen | 10995080  |

#### Assignment
Make an elasticsearch powered search engine on one of multiple data sets.
Full assignment on [maartenmarx.nl](http://nbviewer.jupyter.org/url/maartenmarx.nl/teaching/zoekmachines/Assignments/ASSIGNMENTS/AssignmentWeek8.ipynb).   
The data set chosen was the [goeievragen.nl]('goeievragen.nl') data set. A set of 400K questions and 1.4M answers from a dutch site.   
We have a [wiki]() where all the features of the search enine are described in detail.


## Installation
```
git clone https://github.com/HarmlessHarm/TheElastic4.git
```
#### Obtaining data set
Download the data set from [maartenmarx.nl](http://maartenmarx.nl/teaching/zoekmachines/Data/goeievraag.zip) made easy with one simple script!   
It will download the data set and unzip it and structure it in directories.
```
./get_data.sh
```

#### Installing develop environment
1. Install Python 3.6.4+
2. Install Elasticsearch 6.2+ and Kibana 6.2+
- For OS X, you can use [Homebrew](https://brew.sh/):
```
brew update
brew install kibana
brew install elasticsearch

brew services start elasticsearch
brew services start kibana
```
- For Windows or Linux, see the Elastic downloads page for[Elasticsearch](https://www.elastic.co/downloads/elasticsearch) and [Kibana](https://www.elastic.co/downloads/kibana).

- Make sure you can visit http://localhost:5601/ and http://localhost:9200/ in your browser.

3. In repo root set up virtual env
```
python3 -m venv venv
source venv/bin/activate
```

4. Install the necessary pyhton requirements
```
pip install -r requirements.txt
```

5. Set up the app module
```
pip install -e ./
```

## Usage
1. Activate your virtual environment
```
source venv/bin/activate
```
2. Import all the data into elasticsearch server
```
python elasticapp/index_data.py
```
3. Start up server
```
python elasticapp/run.py
```
4. Search away at [localhost:5000](http://localhost:5000)

<!-- ## Tutorials: -->
<!-- To get a grip for elasticsearch I'd recommend following some tutorials -->
<!-- - PyCon2018 ElasticSearch [video](https://www.youtube.com/watch?v=6_P_h2bDwYs), [repo](https://github.com/julieqiu/pycon-2018-pyelasticsearch), [completed repo](https://github.com/HarmlessHarm/elastic_tut) -->
