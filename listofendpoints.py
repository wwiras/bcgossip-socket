from kubernetes import client, config

def main():

    config.load_incluster_config()
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces(watch=False)
    for svc in services.items:
        print(svc)
        if svc.spec.selector:
            # convert the selector dictionary into a string selector
            # for example: {"app":"redis"} => "app=redis"
            selector = ''
            for k,v in svc.spec.selector.items():
                selector += k + '=' + v + ','
                selector = selector[:-1]
                print(selector)
                # Get the pods that match the selector
                # pods = v1.list_pod_for_all_namespaces(label_selector=selector)
                # pods = v1.list_pod_for_all_namespaces(selector)
                # 
    # pods = v1.list_pod_for_all_namespaces()
    # pods = v1.list_pod_for_all_namespaces(selector={"run":"my-nginx"})
    # for pod in pods.items:
    #     print(pod.metadata.name)

if __name__ == '__main__':
    main()