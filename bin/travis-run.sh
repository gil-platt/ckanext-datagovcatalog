#!/bin/sh -e

echo "TESTING ckanext-datagovcatalog"

nosetests --ckan --with-pylons=subdir/test.ini ckanext/datagovcatalog/tests/ --nologcapture
