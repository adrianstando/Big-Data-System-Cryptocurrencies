# Hive

Version 2.3.2
(metastore-postgresql 2.3.0)

Login and password are the same: hive.

We ran into some issues with regular volume mounting, thus eventually we created a named volume (pgdata) for hive-metastore-postgresql.

# Unused

## HBase

Version: 2.2.6 (prevoiusly 1.2.6)

Finally, we don't use HBase, as we weren't able to properly configure everything, yet we feel that we were close to proper solution.

## Happybase

If you want to use Happybase, you have to run following commands on spark-master container:

```
apk add python2-dev
apk add python3-dev
apk add gcc
pip install --upgrade pip
pip3 install --upgrade pip
pip install wheel
pip3 install wheel
apk add musl-dev
pip install cython
pip3 install cython
pip install thriftpy2
pip install happybase
pip3 install thriftpy2
pip3 install happybase
```

In some cases it casts a weird Error: `AttributeError: license_paths`