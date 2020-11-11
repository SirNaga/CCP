import os
os.environ["EXOSCALE_API_KEY"] = os.environ["EXOSCALE_KEY"]
os.environ["EXOSCALE_API_SECRET"] = os.environ["EXOSCALE_SECRET"]
import exoscale
import time
ZONE = os.environ['EXOSCALE_ZONE']
if ZONE is None:
        ZONE = "AT-VIE-1";
INSTANCE_POOL = os.environ['EXOSCALE_INSTANCEPOOL_ID']
prometheusFile = "/prometheus/targets.json"
srvDis = "/srv/service-discovery/config.json"
prometheusPort = os.environ['TARGET_PORT']
checkInterval = 30
while True:
        try:
                exo = exoscale.Exoscale()
                zone = exo.compute.get_zone(ZONE)
                instances = list(exo.compute.get_instance_pool(INSTANCE_POOL, zone).instances)
                part1 = "[{\"targets\": [ "
                part2 = ""
                part3 = " ]}]"
                ips = list()
                for inst in instances:
                        if inst.state == "running" :
                                ips.append("\""+inst.ipv4_address+":"+str(prometheusPort)+"\"")

                f = open(prometheusFile, "w")
                f.write(part1+(", ".join(ips))+part3)
                print(part1+(", ".join(ips))+part3)
                f.close()
                f = open(srvDis, "w")
                f.write(part1+(", ".join(ips))+part3)
                f.close()
        except Exception as e:
                print("Something bad went wrong...we will try it again later! -> "+ str(e))
        time.sleep(checkInterval)