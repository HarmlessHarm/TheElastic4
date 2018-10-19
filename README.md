# TheElastic4
Elastic Search assignment for the zoekmachines course at University of Amsterdam


## Obtaining data set
run `./get_data.sh` to download and unzip the data set

## Set up
1. Python 3.6.4+
2. Elasticsearch 6.2+ and Kibana 6.2+
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
pip install -r requirements
```

5. Set up the app module
```
pip install -e ./
```

### Tutorials:
To get a grip for elasticsearch I'd recommend following some tutorials
- PyCon2018 ElasticSearch [video](https://www.youtube.com/watch?v=6_P_h2bDwYs), [repo](https://github.com/julieqiu/pycon-2018-pyelasticsearch)