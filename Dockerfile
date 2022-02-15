FROM ubuntu as builder

# Set up code directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy requirements
COPY requirements.txt .

# Install dependecies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip python3-dev curl gcc wget
RUN pip3 install -r requirements.txt
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && apt-get install -y nodejs

RUN npm install -g ganache-cli

CMD ["/bin/bash", "-c", "brownie --help"]