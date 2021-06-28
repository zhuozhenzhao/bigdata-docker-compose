# VERSION 1.10.2
# AUTHOR: Thiago Cordon Rodrigues
# DESCRIPTION: Airflow container with JAVA 8 and SPARK binaries
# BUILD: docker build --rm -t docker-airflow-spark:latest .
# BASED ON: https://github.com/puckel/docker-airflow

# stretch debian version allows JAVA JDK 8
FROM python:3.6-stretch
LABEL maintainer="cordon-thiago"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.7
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_GPL_UNIDECODE yes

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY requirements.txt /requirements.txt

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        iputils-ping \
        telnet \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install -r requirements.txt \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install 'redis>=2.10.5,<3' \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base \
    && python --version \
    && pip freeze

###############################
## Begin JAVA installation
###############################
# Java is required in order to spark-submit work
# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y gnupg2 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EB9B1D8886F44E2A && \
    add-apt-repository "deb http://security.debian.org/debian-security stretch/updates main" && \ 
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    pip freeze && \
    java -version $$ \
    javac -version

# Setup JAVA_HOME 
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME
###############################
## Finish JAVA installation
###############################

COPY entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow/airflow.cfg

###############################
## SPARK files and variables
###############################
# Spark submit binaries and jars (Spark binaries must be the same version of spark cluster)
COPY hadoop/hadoop_bin /usr/hadoop
COPY hadoop/hadoop_config /usr/hadoop/etc/hadoop
COPY spark/spark_bin /usr/spark

# Create SPARK_HOME env var
ENV HADOOP_HOME /usr/hadoop
RUN export HADOOP_HOME
ENV HADOOP_CONF_DIR /usr/hadoop/etc/hadoop
RUN export HADOOP_CONF_DIR

ENV SPARK_HOME /usr/spark
RUN export SPARK_HOME
ENV SPARK_CONF_DIR /usr/spark/conf
RUN export SPARK_CONF_DIR
ENV SPARK_DIST_CLASSPATH /usr/hadoop/etc/hadoop:/usr/hadoop/share/hadoop/common/lib/*:/usr/hadoop/share/hadoop/common/*:/usr/hadoop/share/hadoop/hdfs:/usr/hadoop/share/hadoop/hdfs/lib/*:/usr/hadoop/share/hadoop/hdfs/*:/usr/hadoop/share/hadoop/mapreduce/lib/*:/usr/hadoop/share/hadoop/mapreduce/*:/usr/hadoop/share/hadoop/yarn:/usr/hadoop/share/hadoop/yarn/lib/*:/usr/hadoop/share/hadoop/yarn/*
RUN export SPARK_DIST_CLASSPATH

ENV PATH $PATH:/usr/spark/bin:/usr/hadoop/bin:/usr/hadoop/sbin
###############################
## Finish SPARK files and variables
###############################

RUN chown -R airflow: ${AIRFLOW_HOME}
RUN chmod +x entrypoint.sh

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint
