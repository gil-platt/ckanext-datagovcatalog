#!/bin/bash
# Setup and run extension tests. This script should be run in a _clean_ CKAN
# environment. e.g.:
#
#     $ docker-compose run --rm app ./test.sh
#

set -o errexit
set -o pipefail

TEST_CONFIG=/srv/app/src_extensions/datagovcatalog/test.ini

# Wrapper for paster/ckan.
# CKAN 2.9 replaces paster with ckan CLI. This wrapper abstracts which comand
# is called.
#
# In order to keep the parsing simple, the first argument MUST be
# --plugin=plugin-name. The config option -c is assumed to be
# test.ini because the argument ordering matters to paster and
# ckan, and again, we want to keep the parsing simple.
function ckan_wrapper () {
  if command -v ckan > /dev/null; then
    shift  # drop the --plugin= argument
    ckan -c $TEST_CONFIG "$@"
  else
    paster "$@" -c $TEST_CONFIG
  fi
}


## Copied from official okfn development file
# https://github.com/okfn/docker-ckan/blob/master/ckan-dev/2.8/setup/start_ckan_development.sh

# Install any local extensions in the src_extensions volume
echo "Looking for local extensions to install..."
echo "Extension dir contents:"
ls -la $SRC_EXTENSIONS_DIR
for i in $SRC_EXTENSIONS_DIR/*
do
    if [ -d $i ];
    then

        if [ -f $i/pip-requirements.txt ];
        then
            pip install -r $i/pip-requirements.txt
            echo "Found requirements file in $i"
        fi
        if [ -f $i/requirements.txt ];
        then
            pip install -r $i/requirements.txt
            echo "Found requirements file in $i"
        fi
        if [ -f $i/dev-requirements.txt ];
        then
            pip install -r $i/dev-requirements.txt
            echo "Found dev-requirements file in $i"
        fi
        if [ -f $i/setup.py ];
        then
            cd $i
            if command -v python > /dev/null;
            then
                python $i/setup.py develop
            else
                python3 $i/setup.py develop
            fi
            echo "Found setup.py file in $i"
            cd $APP_DIR
        fi

        # Point `use` in test.ini to location of `test-core.ini`
        if [ -f $i/test.ini ];
        then
            echo "Updating \`test.ini\` reference to \`test-core.ini\` for plugin $i"
            if command -v paster > /dev/null;
            then
                paster --plugin=ckan config-tool $i/test.ini "use = config:../../src/ckan/test-core.ini"
            else
                ckan config-tool $i/test.ini "use = config:../../src/ckan/test-core.ini"
            fi
        fi
    fi
done

ckan_wrapper --plugin=ckan db init
ckan_wrapper --plugin=ckanext-harvest harvester initdb

# start_ckan_development.sh &
pytest --ckan-ini=$TEST_CONFIG --cov=ckanext.datagovcatalog --disable-warnings /srv/app/src_extensions/datagovcatalog/ckanext/datagovcatalog/tests/
