FROM python:latest
COPY serviceDiscovery.py /serviceDiscovery.py
RUN mkdir /prometheus
RUN mkdir -p /service/serviceDiscovery
RUN chmod +x /serviceDiscovery.py
RUN pip install exoscale
CMD [ "python", "serviceDiscovery.py" ]