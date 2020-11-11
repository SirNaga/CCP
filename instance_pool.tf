variable "zone" {
  default = "at-vie-1"
}

resource "exoscale_instance_pool" "ccpInstancePool" {
  zone = var.zone
  name = "ccpInstancePool"
  template_id = data.exoscale_compute_template.ubuntu.id
  size = 3
  service_offering = "micro"
  disk_size = 10
  key_pair = ""
  security_group_ids = [exoscale_security_group.sg.id]

  timeouts {
    delete = "10m"
  }

  user_data = <<EOF
#!/bin/bash

set -e
apt update

#install docker //exercise way - not recommended
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

#pulls the image and runs it
sudo docker pull janoszen/http-load-generator:latest
sudo docker run -d --rm -p 80:8080 janoszen/http-load-generator

#exuting the node exporter as suggested in the exercise
sudo docker run -d -p 9100:9100 \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter \
  --path.rootfs=/host
EOF
}