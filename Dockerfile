FROM python:3.11-slim-bullseye

LABEL org.opencontainers.image.authors="Nsandax"
LABEL "Vendor"="Nsandax"
LABEL version="0.4"

ENV PYTHONUNBUFFERED=1
WORKDIR /erp

RUN apt-get update && apt-get upgrade -y
# Production config (https)
RUN apt-get install apt-transport-https
# Install necessary package for django runtime
RUN apt-get install -y default-libmysqlclient-dev \
        pkg-config \
        libpango-1.0-0  \ 
        libharfbuzz0b \
        libpangoft2-1.0-0 \
        libpangocairo-1.0-0 \
        libxml2-dev \ 
        libxslt-dev \
        libffi-dev \
        libcairo2-dev \
        libpango1.0-dev --fix-missing

# Install gcc
RUN apt-get install -y build-essential

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Comment this Line on production Image
# RUN pip3 install django_dump_die

# Create the erp rootless user
ARG USERNAME=erp
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

COPY others.requirements.txt others.requirements.txt
RUN pip3 install -r others.requirements.txt

RUN apt-get install unixodbc -y

RUN pip3 install Django==3.2.16
# [Optional] Set the default user. Omit if you want to keep the default as root.
# USER $USERNAME

RUN apt-get install curl -y

RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Debian 9
RUN curl https://packages.microsoft.com/config/debian/9/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

#Debian 10
RUN curl https://packages.microsoft.com/config/debian/10/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

#Debian 11
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip3 install Django==3.2.16
RUN pip3 install redis==5.0.1

# Remove Unused packages 
RUN  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
   && rm -rf /var/lib/apt/lists/*

# Copy erp files in Container
COPY ./ ./

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000
