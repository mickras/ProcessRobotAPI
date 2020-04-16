FROM python:3

RUN apt-get update && apt-get install -y \
curl

# Install odbc
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN ACCEPT_EULA=Y apt-get install mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
RUN source ~/.bashrc
RUN apt-get update && apt-get install -y \
unixodbc-dev

RUN chmod +rwx /etc/ssl/openssl.cnf
RUN sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

WORKDIR /usr/src/app

COPY requirements_python3_8_2.txt ./
RUN pip install --no-cache-dir -r requirements_python3_8_2.txt

COPY . .

CMD [ "python", "./api.py" ]