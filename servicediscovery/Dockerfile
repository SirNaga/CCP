FROM python:latest
COPY serviceDiscovery.py /serviceDiscovery.py
RUN mkdir /prometheus
RUN mkdir -p /srv/service-discovery
RUN chmod +x /sd_agent.py
RUN pip install exoscale
CMD [ "python", "serviceDiscovery.py" ]