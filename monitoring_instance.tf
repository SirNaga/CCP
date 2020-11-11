resource "exoscale_compute" "MonitoringInstancePrometheus" {
  zone         = var.zone
  display_name = "MonitoringInstancePrometheus"
  template_id  = data.exoscale_compute_template.ubuntu.id
  size         = "Micro"
  disk_size    = 10
  key_pair     = ""
  security_group_ids = [exoscale_security_group.sg.id]
  user_data = <<EOF
#!/bin/bash

set -e
sudo apt update

#install prometheus and setup files
apt-get -y install prometheus

echo "global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']
  - job_name: Monitoring Server Node Exporter
    static_configs:
      - targets:
          - 'localhost:9100'
  - job_name: Service Discovery
    file_sd_configs:
      - files:
          - /etc/prometheus/targets.json
        refresh_interval: 10s" > /etc/prometheus/prometheus.yml;
systemctl restart prometheus
#END install prometheus and setup files

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

git clone https://github.com/SirRacuga/CCP.git
cd CCP/servicediscovery
docker build --tag servicediscovery:1.0 .

docker run \
    -d \
    -e EXOSCALE_KEY=${var.exoscale_key} \
    -e EXOSCALE_SECRET=${var.exoscale_secret} \
    -e EXOSCALE_ZONE=${var.zone} \
    -e EXOSCALE_INSTANCEPOOL_ID=${exoscale_instance_pool.ccpInstancePool.id} \
    -e TARGET_PORT=9100 \
    -v /etc/prometheus:/prometheus \
    servicediscovery:1.0
EOF
}