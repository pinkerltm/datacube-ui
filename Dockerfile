FROM opendatacube/datacube-core


RUN apt-get update && apt-get install -y \
    libgeos++-dev git python3-scipy postgresql-client imagemagick \
    && rm -rf /var/lib/apt/lists/*

ADD ./requirements/requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install \
    https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz \
    && rm -rf $HOME/.cache/pip

RUN pip3 install \
    -r /tmp/requirements.txt \
    && rm -rf $HOME/.cache/pip

ADD . /code
WORKDIR /code
CMD /code/run-django.sh
