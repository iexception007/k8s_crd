#!/usr/bin/python
# -*- coding: utf-8 -*-


from kubernetes import client
from kubernetes.client.rest import ApiException
#from pprint import pprint
from common.logger import *
#import sys
import urllib3
urllib3.disable_warnings()


DEBUG_MODE = False

#K8S_HOST  = 'https://192.168.1.191:6443'
K8S_HOST  = 'https://dev-7:6443'
API_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyZXBsaWNhc2V0LWNvbnRyb2xsZXItdG9rZW4tanFoY2oiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoicmVwbGljYXNldC1jb250cm9sbGVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYmEyY2FjYjItOTNkMy0xMWU4LTkxYmQtMDAxNjNlMGY3ZDk1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnJlcGxpY2FzZXQtY29udHJvbGxlciJ9.QOtqtv6PW5gh7TdI9_5wkUcanivikjyszy-9HAKle2zhHPQbrQu0_eaDVEJalUpv4_QsV78jrM3NfgpK4vaDJpuVjzgY9Q8enHGlQOGE3wFQHbjO06-czNunoigo17wC4a0-H__aia-FLNnduB3gaPGC86lxkWUm_Rue20WHZLT39O4WBovqzfefUVe8j0KpGRypTl5MZRfVEKZuATFusbx6fbmlnu795scaLSsrry8PcDyYo5PT0Bct90kEgOnvDnI26g8zr_tNhdizL4vY9YusQGXPKOq1WyZxCBO3Bzp-r38H9WwDQuEL4y-YdQttIJv3mQykCurTN9bXgwe-kw'


class K8sHelper(object):
    def __init__(self):
        configuration            = client.Configuration()
        configuration.host       = K8S_HOST
        configuration.verify_ssl = False
        configuration.debug      = DEBUG_MODE
        configuration.api_key    = {"authorization":"Bearer "+ API_TOKEN}
        self.k8s_api =  client.CustomObjectsApi(client.ApiClient(configuration))

    def GetCustomObject(self, group, version, plural, name):
        try:
            return self.k8s_api.get_cluster_custom_object(group, version, plural, name)
        except ApiException as e:
            pass
        #    logger.error("Exception when calling GetCustomObject: %s\n" % e)

    def SetCustomObject(self, group, version, plural, name, body):
        try:
            co = self.GetCustomObject(group, version, plural, name)
            if co == None:
                self.k8s_api.create_cluster_custom_object(group, version, plural, body)
                return

            if co.get('metadata').get('name') != name:
                self.k8s_api.create_cluster_custom_object(group, version, plural, body)
                return

            self.k8s_api.patch_cluster_custom_object(group, version, plural, name, body)
            #self.k8s_api.replace_cluster_custom_object(group, version, plural, name, body)

        except ApiException as e:
            logger.error("Exception when calling SetCustomObject: %s\n" % e)

    def DelCustomObject(self, group, version, plural, name):
        try:
            body = client.V1DeleteOptions() # V1DeleteOptions |
            grace_period_seconds = 30
            orphan_dependents = True
            #propagation_policy = 'propagation_policy_example'
            self.k8s_api.delete_cluster_custom_object(group, version, plural, name, body, grace_period_seconds=grace_period_seconds, orphan_dependents=orphan_dependents)
        except ApiException as e:
            logger.error("Exception when calling DelCustomObject: %s\n" % e)

###############################################################################################
import yaml

def LoadYaml(file_name):
    with open(file_name) as f:
        return yaml.load(f)


def display_co(co):
    logger.info("ovs_bridge          = %s" % co.get('spec').get('ovs_bridge'))
    logger.info("pod_security_groups = %s" % co.get('spec').get('pod_security_groups'))
    logger.info("pod_subnet          = %s" % co.get('spec').get('pod_subnet'))
    logger.info("project             = %s" % co.get('spec').get('project'))
    logger.info("service_subnet      = %s" % co.get('spec').get('service_subnet'))



def test_del_co(helper, name):
    logger.info("DelCustomObject(%s)" % name)
    helper.DelCustomObject('openstack.org', 'v1', 'kuryrnets', name)


def test_get_co(helper, name):
    logger.info("GetCustomObject(%s)" % name)
    co = helper.GetCustomObject('openstack.org', 'v1', 'kuryrnets', name)
    if co != None:
        display_co(co)


def test_set_co(helper):
    """
    body = {
    "apiVersion": "openstack.org/v1",
    "kind": "KuryrNet",
    "metadata": {
        "name": "cluster2",
    },
    "spec": {
        "podSubnet": 333336,
        "serviceSubnet": 44446
    }
}"""

    yaml_file = os.getcwd() + '/config/cluster2.yaml'
    body = LoadYaml(yaml_file)
    helper.SetCustomObject('openstack.org', 'v1', 'kuryrnets', 'cluster2', body)

def main():
    k8s_helper = K8sHelper()
    test_get_co(k8s_helper, 'cluster1')
    test_set_co(k8s_helper)
    test_get_co(k8s_helper, 'cluster2')
#    test_del_co(k8s_helper, 'cluster2')


if __name__ == "__main__":
    main()