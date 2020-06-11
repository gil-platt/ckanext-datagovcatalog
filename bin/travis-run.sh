#!/bin/sh -e

echo "TESTING ckanext-datagovcatalog"

nosetests --ckan \
          --nologcapture \
          --with-pylons=subdir/test.ini \
          --with-coverage \
          --cover-package=ckanext.datagovcatalog \
          --cover-inclusive \
          --cover-erase \
          --cover-tests
