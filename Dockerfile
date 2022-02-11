ARG CKAN_VERSION=2.9
FROM openknowledge/ckan-dev:${CKAN_VERSION}
ARG CKAN_VERSION

RUN pip3 install --upgrade pip

COPY . /srv/app
WORKDIR /srv/app

# python cryptography takes a while to build
RUN if [[ "${CKAN_VERSION}" = "2.8" ]] ; then \
        pip install -r requirements-py2.txt -r dev-requirements-py2.txt -e . ; else \
        pip3 install -r requirements.txt -r dev-requirements.txt -e . ; fi

WORKDIR ${APP_DIR}
