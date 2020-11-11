import exoscale
import os
import time as timer


os.environ["EXOSCALE_API_KEY"] = os.environ["EXOSCALE_KEY"]
os.environ["EXOSCALE_API_SECRET"] = os.environ["EXOSCALE_SECRET"]
instancePoolId = os.environ['EXOSCALE_INSTANCEPOOL_ID']
zone = os.environ['EXOSCALE_ZONE']
targetPort = os.environ['TARGET_PORT']
preffix = "[{\"targets\": [ "
suffix = " ]}]"


while True:

        exoscaleConnection = exoscale.Exoscale()
        exoscaleZone = exoscaleConnection.compute.get_zone(zone)
        instances = list(exoscaleConnection.compute.get_instance_pool(instancePoolId, exoscaleZone).instances)
        instanceIPv4Addresses = list()

        for instance in instances:
                if instance.state == "running":
                        instanceIPv4Addresses.append("\"" + instance.ipv4_address + ":" + str(targetPort) + "\"")

        targetsFile = open("/prometheus/targets.json", "w")
        targetsFile.write(preffix + (", ".join(instanceIPv4Addresses)) + suffix)
        targetsFile.close()
        targetsFileConfig = open("/srv/service-discovery/config.json", "w")
        targetsFileConfig.write(preffix + (", ".join(instanceIPv4Addresses)) + suffix)
        targetsFileConfig.close()
        timer.sleep(10)