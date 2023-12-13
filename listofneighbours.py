from kubernetes import client, config

def main():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods from service name : bcgossip")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    
    nlist = []
    for i in ret.items:
        if(i.metadata.labels):
            for k,v in i.metadata.labels.items():
                if (k=='run') and (v=='bcgossip'):
                    nlist.append(i.status.pod_ip)

    print(nlist)


if __name__ == '__main__':
    main()