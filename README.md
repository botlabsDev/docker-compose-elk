# Basic ELKG (Elasticsearch, Logstash, Kibana and Grafana) for docker-compose

If you just quickly want to evaluate some data in Kibana or Grafana, this docker-compose file is your way to go.
It just starts and connects Elasticsearch, Logstash, Kibana and Grafana.

The source of the docker-compose file was initial posted by: https://www.gyanblog.com/gyan/how-run-elasticsearch-cluster-docker-kibana . It can also be found on variouse other sides on the internet.

If you aime to use the setup longer, please change the used passwords. CHANGE THE
PASSWORDS!

## How to start

```
$ sudo apt-get install -y docker docker-compose
$ git clone https://github.com/botlabsdev/basic-elkg
$ cd basic-elkg
$ ./setSystemLimits.sh
$ sudo docker-compose up
```

## Services available

* Elasticsearch: http://localhost:9200
* Elasticsearch: http://localhost:9300
* Logstash: http://localhost:5000
* Logstash: http://localhost:9600
* Kibana: http://localhost:5601
* Grafana: http://localhost:3000
  * user: admin
  * password: admin

## How to change the used ELK version? 

* ELK version numbers are stored in the '.env' file.
* Grafana always uses the last available version.
