Hari Sekhon PyTools
===================
[![Build Status](https://travis-ci.org/HariSekhon/pytools.svg?branch=master)](https://travis-ci.org/HariSekhon/pytools)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f7af72140c3b408b9659207ced17544f)](https://www.codacy.com/app/harisekhon/pytools)
[![GitHub stars](https://img.shields.io/github/stars/harisekhon/pytools.svg)](https://github.com/harisekhon/pytools/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/harisekhon/pytools.svg)](https://github.com/harisekhon/pytools/network)
[![Dependency Status](https://gemnasium.com/badges/github.com/HariSekhon/pytools.svg)](https://gemnasium.com/github.com/HariSekhon/pytools)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20OS%20X-blue.svg)](https://github.com/harisekhon/pytools#hari-sekhon-pytools)
[![DockerHub](https://img.shields.io/badge/docker-available-blue.svg)](https://hub.docker.com/r/harisekhon/pytools/)
[![](https://images.microbadger.com/badges/image/harisekhon/pytools.svg)](http://microbadger.com/#/images/harisekhon/pytools)

### Hadoop, Spark / PySpark, HBase, Pig, Ambari, IPython and Linux Tools ###

A few of the Hadoop, Spark & Linux tools I've written over the years. All programs have `--help` to list the available options.

For many more tools see the [Tools](https://github.com/harisekhon/tools) and [Advanced Nagios Plugins Collection](https://github.com/harisekhon/nagios-plugins) repos which contains many Hadoop, NoSQL, Web and infrastructure tools and Nagios plugins.

Hari Sekhon

Big Data Contractor, United Kingdom

https://www.linkedin.com/in/harisekhon

##### Make sure you run ```make update``` if updating and not just ```git pull``` as you will often need the latest library submodule and possibly new upstream libraries. #####

### Quick Start ###

#### Ready to run Docker image #####

All programs and their pre-compiled dependencies can be found ready to run on [DockerHub](https://hub.docker.com/r/harisekhon/pytools/).

List all programs:
```
docker run harisekhon/pytools
```
Run any given program:
```
docker run harisekhon/pytools <program> <args>
```

#### Automated Build from source #####

```
git clone https://github.com/harisekhon/pytools
cd pytools
make
```
Some Hadoop tools with require Jython, see [Jython for Hadoop Utils](https://github.com/harisekhon/pytools#jython-for-hadoop-utils) for details.

### Usage ###

All programs come with a ```--help``` switch which includes a program description and the list of command line options.

Environment variables are supported for convenience and also to hide credentials from being exposed in the process list eg. ```$PASSWORD```, ```$TRAVIS_TOKEN```. These are indicated in the ```--help``` descriptions in brackets next to each option and often have more specific overrides with higher precedence eg. ```$AMBARI_HOST```, ```$HBASE_HOST``` take priority over ```$HOST```.

### PyTools ###

- ```find_active_server.py``` - generic solution to return the first available healthy server or active master in high availability deployments, useful for chaining with single argument tools. Configurable tests include socket, http, https, ping, url and/or regex content match, multi-threaded for speed. Designed to extend tools that only accept a single ```--host``` option but for which the technology has later added multi-master support or active-standby masters (eg. Hadoop, HBase) or where you want to query cluster wide information available from any online peer (eg. Elasticsearch)
  - the following are simplified specialisations of the above program, just pass host arguments, all the details have been baked in, no switches required
    - ```find_active_hadoop_namenode.py``` - finds the active Hadoop Namenode in HDFS HA
    - ```find_active_hadoop_resource_manager.py``` - finds the active Hadoop Resource Manager in Yarn HA
    - ```find_active_hbase_master.py``` - finds the active HBase Master in HBase HA
    - ```find_active_solrcloud_node.py``` - finds the first available SolrCloud node
    - ```find_active_elasticsearch_node.py``` - finds the first available Elasticsearch node
- ```ambari_blueprints.py``` - Ambari Blueprint tool using Ambari API to find and fetch all blueprints or a specific blueprint to local json files, blueprint an existing cluster, or create a new cluster using a blueprint. Sorts and prettifies the resulting JSON template, and optionally strips out the excessive and overly specific configs to create generic more reusable templates. See the ```ambari_blueprints``` directory for a variety of Ambari blueprint templates generated by and deployable using this tool
- ```hadoop_hdfs_time_block_reads.jy``` - Hadoop HDFS per-block read timing debugger with datanode and rack locations for a given file or directory tree. Reports the slowest Hadoop datanodes in descending order at the end. Helps find cluster data layer bottlenecks such as slow datanodes, faulty hardware or misconfigured top-of-rack switch ports.
- ```hadoop_hdfs_files_native_checksums.jy``` - fetches native HDFS checksums for quicker file comparisons (about 100x faster than doing hdfs dfs -cat | md5sum)
- ```hadoop_hdfs_files_stats.jy``` - fetches HDFS file stats. Useful to generate a list of all files in a directory tree showing block size, replication factor, underfilled blocks and small files
- ```hbase_generate_data.py``` - inserts random generated data in to a given HBase table, with optional skew support with configurable skew percentage. Useful for testing region splitting, balancing, CI tests etc. Outputs stats for number of rows written, time taken, rows per sec and volume per sec written.
- ```hbase_show_table_region_ranges.py``` - dumps HBase table region ranges information, useful when pre-splitting tables
- ```hbase_calculate_table_region_row_distribution.py``` - calculates the distribution of rows across regions in an HBase table, giving per region row counts and % of total rows for the table as well as median and quartile row counts per regions
- ```hbase_calculate_table_row_key_distribution.py``` - calculates the distribution of row keys by configurable prefix length in an HBase table, giving per prefix row counts and % of total rows for the table as well as median and quartile row counts per prefix
- ```hbase_compact_tables.py``` - compacts HBase tables (for off-peak compactions). Defaults to finding and iterating on all tables or takes an optional regex and compacts only matching tables.
- ```hbase_flush_tables.py``` - flushes HBase tables. Defaults to finding and iterating on all tables or takes an optional regex and flushes only matching tables.
- ```pig-text-to-elasticsearch.pig``` / ```pig-text-to-solr.pig``` - bulk indexes unstructured files in Hadoop to Elasticsearch or Solr/SolrCloud clusters
- ```pig_udfs.jy``` - Pig Jython UDFs for Hadoop
- ```ipython-notebook-pyspark.py``` - per-user authenticated IPython Notebook + PySpark integration to allow each user to auto-create their own password protected IPython Notebook running Spark
- ```json_docs_to_bulk_multiline.py``` - converts json files to bulk multi-record one-line-per-json-document format for pre-processing and loading to big data systems like Hadoop and MongoDB, can recurse directory trees, and mix json-doc-per-file / bulk-multiline-json / directories / standard input, combines all json documents and outputs bulk-one-json-document-per-line to standard output for convenient command line chaining and redirection, optionally continues on error, collects broken records to standard error for logging and later reprocessing for bulk batch jobs, even supports single quoted json while not technically valid json is used by MongoDB and even handles embedded double quotes in 'single quoted json'
- ```json_to_xml.py``` - JSON to XML converter
- ```xml_to_json.py``` - XML to JSON converter
- ```spark_avro_to_parquet.py``` - PySpark Avro => Parquet converter
- ```spark_parquet_to_avro.py``` - PySpark Parquet => Avro converter
- ```spark_csv_to_avro.py``` - PySpark CSV => Avro converter, supports both inferred and explicit schemas
- ```spark_csv_to_parquet.py``` - PySpark CSV => Parquet converter, supports both inferred and explicit schemas
- ```spark_json_to_avro.py``` - PySpark JSON => Avro converter
- ```spark_json_to_parquet.py``` - PySpark JSON => Parquet converter
- ```docker_registry_show_tags.py / dockerhub_show_tags.py``` - shows tags for docker repos in a docker registry or on [DockerHub](https://hub.docker.com/u/harisekhon/) - Docker CLI doesn't support this yet but it's a very useful thing to be able to see live on the command line or use in shell scripts (use `-q`/`--quiet` to return only the tags for easy shell scripting). You can use this to pre-download all tags of a docker image before running tests across versions in a simple bash for loop, eg. ```docker_pull_all_tags.sh```
- ```dockerhub_search.py``` - search DockerHub with a configurable number of returned results (official `docker search` is limited to only 25 results), using `--verbose` will also show you how many results were returned to the termainal and how many DockerHub has in total (use ```-q / --quiet``` to return only the image names for easy shell scripting). This can be used to download all of my DockerHub images in a simple bash for loop eg. ```docker_pull_all_images.sh``` and can be chained with ```dockerhub_show_tags.py``` to download all tagged versions for all docker images eg. ```docker_pull_all_images_all_tags.sh```
- ```dockerfiles_check_git*.py``` - check Git tags & branches align with the containing Dockerfile's ```ARG *_VERSION```
- ```welcome.py``` - cool spinning welcome message greeting your username and showing last login time and user (there is also a perl version in my [Tools](https://github.com/harisekhon/tools) repo)
- ```find_duplicate_files.py``` - finds duplicate files in one or more directory trees via multiple methods including file basename, size, MD5 comparison of same sized files, or bespoke regex capture of partial file basename
- ```travis_debug_session.py``` - launches a Travis CI interactive debug build session via Travis API, tracks session creation and drops user straight in to the SSH shell on the remote Travis build, very convenient one shot debug launcher for Travis CI
- ```validate_*.py``` - validate files, directory trees and/or standard input streams for the following file types:
    - Avro
    - CSV
    - INI / Java Properties (also detects duplicate sections and duplicate keys within sections)
    - JSON (both normal and json-doc-per-line bulk / big data format as found in MongoDB and Hadoop json data files)
    - LDAP LDIF
    - Parquet
    - XML
    - YAML
  - directories are recursed, testing any files with relevant matching extensions (`.avro`, `.csv`, `json`, `parquet`, `.ini`/`.properties`, `.ldif`, `.xml`, `.yml`/`.yaml`)
  - used for Continuous Integration tests of various adjacent Spark data converts as well as configuration files for things like Presto, Ambari, Apache Drill etc found in my [DockerHub](https://hub.docker.com/u/harisekhon/) images [Dockerfiles master repo](https://github.com/HariSekhon/Dockerfiles) which contains docker builds and configurations for many open source Big Data & Linux technologies

#### Manual Setup ####

Enter the pytools directory and run git submodule init and git submodule update to fetch my library repo:

```
git clone https://github.com/harisekhon/pytools
cd pytools
git submodule init
git submodule update
pip install -r requirements.txt
```

### Jython for Hadoop Utils ###

The 3 Hadoop utility programs listed below require Jython (as well as Hadoop to be installed and correctly configured)

```
hadoop_hdfs_time_block_reads.jy
hadoop_hdfs_files_native_checksums.jy
hadoop_hdfs_files_stats.jy
```

Run like so:
```
jython -J-cp `hadoop classpath` hadoop_hdfs_time_block_reads.jy --help
```

The ```-J-cp `hadoop classpath` ``` bit does the right thing in finding the Hadoop java classes required to use the Hadoop APIs.

See below for procedure to install Jython if you don't already have it.

##### Automated Jython Install

```
make jython-install
```

##### Manual Jython Install

Jython is a simple download and unpack and can be fetched from http://www.jython.org/downloads.html

Then add the Jython untarred directory to the $PATH or specify the /path/to/jythondir/bin/jython explicitly when calling jython.

#### Configuration for Strict Domain / FQDN validation ####

Strict validations include host/domain/FQDNs using TLDs which are populated from the official IANA list is done via my [PyLib](https://github.com/harisekhon/pylib) library submodule - see there for details on configuring this to permit custom TLDs like ```.local``` or ```.intranet``` (both supported by default).

#### Python SSL certificate verification problems

If you end up with an error like:
```
./dockerhub_show_tags.py centos ubuntu
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:765)
```
It can be caused by an issue with the underlying Python + libraries due to changes in OpenSSL and certificates. One quick fix is to do the following:
```
pip uninstall -y certifi && pip install certifi==2015.04.28
```

### Updating ###

Run ```make update```. This will git pull and then git submodule update which is necessary to pick up corresponding library updates.

If you update often and want to just quickly git pull + submodule update but skip rebuilding all those dependencies each time then run ```make update-no-recompile``` (will miss new library dependencies - do full ```make update``` if you encounter issues).

### Testing

[Continuous Integration](https://travis-ci.org/HariSekhon/pytools) is run on this repo with tests for success and failure scenarios:
- unit tests for the custom supporting [python library](https://github.com/harisekhon/pylib)
- integration tests of the top level programs using the libraries for things like option parsing
- [functional tests](https://github.com/HariSekhon/pytools/tree/master/tests) for the top level programs using local test data and [Docker containers](https://hub.docker.com/u/harisekhon/)

To trigger all tests run:

```
make test
```

which will start with the underlying libraries, then move on to top level integration tests and functional tests using docker containers if docker is available.

### Contributions ###

Patches, improvements and even general feedback are welcome in the form of GitHub pull requests and issue tickets.

### See Also ###

* [Tools](https://github.com/harisekhon/tools) - 30+ tools for Hadoop, NoSQL, Solr, Elasticsearch, Pig, Hive, Web URL + Nginx stats watchers, SQL and NoSQL syntax recasers, various Linux CLI tools

* [The Advanced Nagios Plugins Collection](https://github.com/harisekhon/nagios-plugins) - 350+ programs for Nagios monitoring your Hadoop & NoSQL clusters. Covers every Hadoop vendor's management API and every major NoSQL technology (HBase, Cassandra, MongoDB, Elasticsearch, Solr, Riak, Redis etc.) as well as message queues (Kafka, RabbitMQ), continuous integration (Jenkins, Travis CI) and traditional infrastructure (SSL, Whois, DNS, Linux)

* [PyLib](https://github.com/harisekhon/pylib) - my personal python library leveraged in this repo as a submodule

* [Perl Lib](https://github.com/harisekhon/lib) - Perl version of above library

* [Spark Apps eg. Spark => Elasticsearch](https://github.com/harisekhon/spark-to-elasticsearch) - Scala application to index from Spark to Elasticsearch. Used to index data in Hadoop clusters or local data via Spark standalone. This started as a Scala Spark port of ```pig-text-to-elasticsearch.pig``` from this repo.

You might also be interested in the following really nice Jupyter notebook for HDFS space analysis created by another Hortonworks guy Jonas Straub:

* https://github.com/mr-jstraub/HDFSQuota/blob/master/HDFSQuota.ipynb
