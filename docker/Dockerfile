FROM ubuntu:latest

# Combine all apt-get install commands or Docker will attempt to use cache
RUN apt-get update && apt-get install -y \
        git \
        python \
        python-dev \
        vim

ADD run_tests.sh /opt/

ENTRYPOINT ["/opt/run_tests.sh"]
