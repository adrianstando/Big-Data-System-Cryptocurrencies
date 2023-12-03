# NiFi - HDFS

## IMPORTANT

While running for the first time, the following steps had to be done:

1. In docker-compose.yaml comment volumes in hdfs-namenode and nifi (lines 15-17 and 90-92).

2. Run

    ```
    docker-compose --env-file stack.env up -d
    ```

3. When the contriners are running, run the following commands:

    ```
    docker cp hdfs-namenode:/hadoop/dfs/name/ ./hdfs/namenode
    cp -r ./hdfs/namenode/name/* ./hdfs/namenode/
    rm -rf ./hdfs/namenode/name

    docker cp hdfs-namenode:/etc/hadoop/ ./hdfs/namenode_etc
    cp -r ./hdfs/namenode_etc/hadoop/* ./hdfs/namenode_etc/
    rm -rf ./hdfs/namenode_etc/hadoop

    docker cp nifi:/opt/nifi/nifi-current/conf/ ./nifi
    cp -r ./nifi/conf/* ./nifi/
    rm -rf ./nifi/conf
	
	docker cp nifi:/opt/nifi/nifi-current/logs/ ./nifi
    cp -r ./nifi/logs/* ./nifi/
    rm -rf ./nifi/logs
    ```

4. Run

    ```
    docker-compose down
    ```

5. Uncomment lines which were commented in 1.

6. You can run now the containers normally, e.g. with:

    ```
    docker-compose --env-file stack.env up -d
    ```

## ATTENTION - NiFI

Template for NiFi is in `template.xml` file. When running NiFi, please upload template and put it on the working area.

## Other comments:

In the `stack.env` file, set the following variables:

* `TS_AUTHKEY` - authentication key to tailscale

* `NEWS_IO_API_key` - authentication key to newsdata.io

* `API_KEY_CRYPTOPANIC` - authentication key to Cryptopanic

* `API_KEY_CRYPTOCOMPARE` - authentication key to Cryptocompare

* `API_KEY_ALPHAVANTAGE` - authentication key to Alpha Vantage

* `API_KEY_NEWSAPI` - authentication key to News API

* `path` - absolute path to the current directory (can be left as `.`)
