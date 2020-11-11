FROM python:latest
COPY sd_agent.py /sd_agent.py
RUN mkdir /prometheus
RUN mkdir -p /srv/service-discovery
RUN chmod +x /sd_agent.py
RUN pip install exoscale
CMD [ "python", "sd_agent.py" ]