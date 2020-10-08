
resource "exoscale_nlb" "ccpNLB" {
  name        = "ccpNLB"
  description = "This is the Network Load Balancer"
  zone        = var.zone
}

resource "exoscale_nlb_service" "ccpNLBService" {
  zone             = exoscale_nlb.ccpNLB.zone
  name             = "ccpNLBService"
  description      = "ccpNLBService"
  nlb_id           = exoscale_nlb.ccpNLB.id
  instance_pool_id = exoscale_instance_pool.ccpInstancePool.id
  protocol       = "tcp"
  port           = 80
  target_port    = 8080
  strategy       = "round-robin"

  healthcheck {
    mode     = "http"
    port     = 8080
    uri      = "/health"
    interval = 5
    timeout  = 3
    retries  = 1
  }
}