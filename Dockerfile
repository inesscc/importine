# start by pulling the python image
#FROM python:3.8-alpine
FROM python:3.9

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app


# Install cron and jobs
RUN apt-get update -y && apt-get -y install cron
RUN echo "*/2 * * * * cd /app && Rscript /app/code/download_last_ene_data.R /app/data/ /app/data/ TRUE" > /etc/cron.d/download-data
RUN echo "" >> /etc/cron.d/download-data 
RUN chmod 0644 /etc/cron.d/download-data
RUN crontab /etc/cron.d/download-data
#RUN cron esta línea debe ser ejecutada en cmd

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["code/app.py" ]
#CMD python3 code/app.py; cron
