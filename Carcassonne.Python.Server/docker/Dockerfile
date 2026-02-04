FROM mcr.microsoft.com/mssql/server:2022-latest AS base

USER root

RUN apt-get update && apt-get install unzip -y

RUN wget -O sqlpackage.zip https://go.microsoft.com/fwlink/?linkid=2297646 \
      && unzip sqlpackage.zip -d /tmp/sqlpackage \
      && chmod +x /tmp/sqlpackage/sqlpackage

COPY ./sh/setup-db.sh /sh/setup-db.sh
RUN chmod -R 777 /sh/.

ENTRYPOINT /sh/setup-db.sh & /opt/mssql/bin/sqlservr  