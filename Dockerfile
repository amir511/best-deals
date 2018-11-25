FROM python:3.6.6
FROM postgres:9.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/
RUN apt-get update
RUN apt-get install python3-pip -y
RUN python3 -m pip install -r requirements.txt
ADD . /src/
EXPOSE 5432
USER postgres
RUN pg_createcluster 9.3 main --start
RUN /etc/init.d/postgresql start
RUN psql --command "CREATE USER bestdeals WITH SUPERUSER PASSWORD 'bestdeals';"
RUN createdb -O best_deals bestdeals
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
USER me
EXPOSE 8000
RUN python3 manage.py migrate
CMD ["python3", "project_entry.py"]