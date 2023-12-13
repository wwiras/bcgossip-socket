from kubernetes import client, config
import socket

def main():
    
    # service name
    svc_name = "bcgossip"

    #getting its own (latest) ip addr
    mynode = socket.gethostbyname(socket.gethostname())
    print(f'My node IPaddr : {mynode}')

    # load k8s configs and getting all metadata
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    
    # initial empty neighbour list
    nlist = []

    # getting all neighbours (pods) except its own IP
    print(f"Listing all negihbours (IP addr) from service name : {svc_name}")
    for i in ret.items:
        if(i.metadata.labels):
            for k,v in i.metadata.labels.items():
                if (k=='run') and (v==svc_name):
                    if (mynode==i.status.pod_ip):
                        continue
                    else:
                        nlist.append(i.status.pod_ip)
    print(nlist)


if __name__ == '__main__':
    main()