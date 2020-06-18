#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install solr-jetty libpq-dev postgresql

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/ckan/ckan
cd ckan
export latest_ckan_release_branch=`git branch --all | grep remotes/origin/release-v | sort -r | sed 's/remotes\/origin\///g' | head -n 1`
echo "CKAN branch: $latest_ckan_release_branch"
git checkout $latest_ckan_release_branch
python setup.py develop
pip install -r requirements.txt --allow-all-external
pip install -r dev-requirements.txt --allow-all-external
cd -

echo "Creating the PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'

echo "SOLR config..."
# Solr is multicore for tests on ckan master, but it's easier to run tests on
# Travis single-core. See https://github.com/ckan/ckan/issues/2972
sed -i -e 's/solr_url.*/solr_url = http:\/\/127.0.0.1:8983\/solr/' ckan/test-core.ini
printf "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart


echo "-----------------------------------------------------------------"
echo "Initialising the database..."
cd ckan
paster db init -c test-core.ini

cd ..
echo "-----------------------------------------------------------------"
echo "Installing Harvester"
git clone https://github.com/ckan/ckanext-harvest
cd ckanext-harvest
git checkout master

python setup.py develop
pip install -r pip-requirements.txt

paster harvester initdb -c ../ckan/test-core.ini

cd ..
echo "-----------------------------------------------------------------"
echo "Installing Geodatagov"
git clone https://github.com/GSA/ckanext-geodatagov
cd ckanext-geodatagov
git checkout test_collections  # TODO just testing temporary master

python setup.py develop
pip install -r pip-requirements.txt

cd ..
echo "-----------------------------------------------------------------"
echo "Installing Spatial"
git clone https://github.com/ckan/ckanext-spatial
cd ckanext-spatial
git checkout master

python setup.py develop
pip install -r pip-requirements.txt

cd ..
echo "-----------------------------------------------------------------"
echo "Installing DataGovTheme"
git clone https://github.com/GSA/ckanext-datagovtheme
cd ckanext-datagovtheme
git checkout master

python setup.py develop

cd ..
echo "-----------------------------------------------------------------"
echo "Installing ckanext-datagovcatalog and its requirements..."
python setup.py develop
pip install -r dev-requirements.txt

echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir

echo "travis-build.bash is done."