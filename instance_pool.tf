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
apt install -y nginx
EOF

}