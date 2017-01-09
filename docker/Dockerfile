FROM ubuntu:latest

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

# Combine all apt-get install commands or Docker will attempt to use cache
RUN apt-get update && apt-get install -y \
        git \
        python \
        python-dev \
        vim

ADD run_tests.sh /opt/

ENTRYPOINT ["/opt/run_tests.sh"]
