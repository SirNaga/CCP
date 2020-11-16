import exoscale
import os
import signal
import time as timer


#setting enviromental variables
os.environ["EXOSCALE_API_KEY"] = os.environ["EXOSCALE_KEY"]
os.environ["EXOSCALE_API_SECRET"] = os.environ["EXOSCALE_SECRET"]
instancePoolId = os.environ['EXOSCALE_INSTANCEPOOL_ID']
zone = os.environ['EXOSCALE_ZONE']
targetPort = os.environ['TARGET_PORT']

class SignalHandler:
  termSignal = False
  def __init__(self):
    signal.signal(signal.SIGTERM, self.exitProcess)

  def exitProcess(self):
    self.termSignal = True


handler = SignalHandler

while not handler.termSignal:
    # Get Exoscale instance
    exoscaleConnection = exoscale.Exoscale()
    exoscaleZone = exoscaleConnection.compute.get_zone(zone)

    instances = list(exoscaleConnection.compute.get_instance_pool(instancePoolId, exoscaleZone).instances)
    instanceIPv4Addresses = list()

    for instance in instances:
        if instance.state == "running":
            instanceIPv4Addresses.append("\"" + instance.ipv4_address + ":" + str(targetPort) + "\"")

    # Write file for prometheus targets
    targetsFile = open("/prometheus/targets.json", "w")
    targetsFile.write("[{\"targets\": [" + (", ".join(instanceIPv4Addresses)) + "]}]")
    targetsFile.close()

    # Write file for required path
    targetsFileConfig = open("/srv/service-discovery/config.json", "w")
    targetsFileConfig.write("[{\"targets\": [" + (", ".join(instanceIPv4Addresses)) + "]}]")
    targetsFileConfig.close()

    timer.sleep(10)
