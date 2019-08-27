#!/usr/bin/env python
# coding=utf-8
#安装python3和pip
#安装以下sdk模块
#pip install aliyun-python-sdk-core-v3
#python2.x
#pip install aliyun-python-sdk-core

#pip install aliyun-python-sdk-slb
#pip install aliyun-python-sdk-ecs
import sys
import json
import argparse
from aliyunsdkcore.client import AcsClient
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkslb.request.v20140515.RemoveBackendServersRequest import RemoveBackendServersRequest 
from aliyunsdkslb.request.v20140515.AddBackendServersRequest import AddBackendServersRequest
from aliyunsdkslb.request.v20140515.SetBackendServersRequest import SetBackendServersRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
import sys
import json
import argparse
from aliyunsdkcore.client import AcsClient
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkslb.request.v20140515.RemoveBackendServersRequest import RemoveBackendServersRequest 
from aliyunsdkslb.request.v20140515.AddBackendServersRequest import AddBackendServersRequest
from aliyunsdkslb.request.v20140515.SetBackendServersRequest import SetBackendServersRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

#  需填写ak信息，可用区
AccessKey='xxxxxx'
AccessKeySecret='xxxxxx'
RegionId = "cn-beijing"

# 需要先获取 aliyun 账号的 AccessKey 信息
client = AcsClient(AccessKey,AccessKeySecret,RegionId);

def help_doc():
    slbinfo = '''
                  !!!something wrong, plz check it!!!
    usage: alislb.py [-h] [--add | --delete | --update | --get]
                          instance ip weight [instance ip weight ...]
    针对 SLB 进行相关操作

    positional arguments:
    instance BackendServers   实例ID  ip weight

    optional arguments:
        -h, --help       show this help message and exit
        -a, --add        add ecs. (e.g. --add instance ip weight)
        -d, --delete     delete ecs . (e.g. --delete instance ip)
        -u, --update     update esc weight. (e.g. --update instance ip weight)
        -g, --get        get slb info, default all. (e.g. --get instance)
    '''
    print(slbinfo)

def get_ecs_instance(ip):
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    request.add_query_param('RegionId','cn-beijing')
    request.add_query_param('PrivateIpAddresses',[str(ip)])
    request.set_PageSize(100)
    try:
        response = client.do_action_with_exception(request)
        info = json.loads(response)['Instances']['Instance']
        if info:
            return [instance_info['InstanceId'] for instance_info in info]
        #print(info)
    except Exception as e:
        print "Get Inner IP Address Faild."
        sys.exit()
    


def get_slb_info(instance):
    request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
    response = client.do_action_with_exception(request)
    SLBInfo = json.loads(response)
    LoadBalancerIdList = []
    for SLBInstance in SLBInfo['LoadBalancers']['LoadBalancer']:
        LoadBalancerIdList.append(SLBInstance['LoadBalancerId'])

    if instance == 'all':
        Ali_Slb_Info = {}
        for SLBInstance in SLBInfo['LoadBalancers']['LoadBalancer']:
            request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
            request.set_LoadBalancerId(SLBInstance['LoadBalancerId'])
            response = client.do_action_with_exception(request)
            Ali_Slb_Info[SLBInstance['LoadBalancerId']] = json.loads(response.decode('utf-8'))
        print(LoadBalancerIdList)
    elif instance in LoadBalancerIdList:
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(instance)
        response = client.do_action_with_exception(request)
        response = json.loads(response.decode('utf-8'))
        print(response['BackendServers'])
        return response['BackendServers']['BackendServer']

    else:
        print("输入错误,请输入 all 或 SLB实例ID ！")


def add_slb_ecs(instance , ip, weight):
    ecsid  = get_ecs_instance(ip) 
    BackendServers=[{"ServerId":ecsid[0],"Weight":weight},]
    request = AddBackendServersRequest()
    request.set_accept_format('json')
    request.set_BackendServers(json.dumps(BackendServers))
    request.set_LoadBalancerId(instance)
    try:   
        response = client.do_action_with_exception(request)
        print(response)
    except Exception as e:
        print e
    # python3    print(str(response, encoding='utf-8'))
    # python2    print(response)
    # print(response)

def delete_slb_ecs(instance , ip):
    slbids = get_slb_info(instance)
    ecsids = [ServerId_info['ServerId'] for ServerId_info in slbids]
    ecsid  = get_ecs_instance(ip) 
    #BackendServers=[{"ServerId":ecsid[0],"Weight":weight},]
    BackendServers=[{"ServerId":ecsid[0]},]
    print(BackendServers)
    if [Flase for ecs in ecsid if ecs not in ecsids]:
        print('slb or ecs is not found')
    else:
        request = RemoveBackendServersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(instance)
        request.set_BackendServers(json.dumps(BackendServers))
        try:
            response = client.do_action_with_exception(request)
            print(response)
        except Exception as e:
            print e
        
        # python3    print(str(response, encoding='utf-8'))
        # python2    print(response)
        #(response)   

def update_slb_ecs(instance, ip, weight):
    ecsid = get_ecs_instance(ip)
    BackendServers=[{"ServerId":ecsid[0],"Weight":weight},]
    if  not ecsid:
        print('ecs is not found')
    else:
        request = SetBackendServersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(instance)
        request.set_BackendServers(json.dumps(BackendServers))
        response = client.do_action_with_exception(request)
        # python3    print(str(response, encoding='utf-8'))
        # python2    print(response)
        print(response)


parser = argparse.ArgumentParser(description='针对 SLB INSTANC 进行相关操作')
parser.add_argument('LIST', metavar=' instance ip weight', type=str, nargs='+',
                    help='实例 IP 权重')
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--add', action='store_true', help='add ecs. (e.g. --add instance ip weight)')
group.add_argument('-d', '--delete', action='store_true', help='delete ecs. (e.g. --delete instance ip)')
group.add_argument('-u', '--update', action='store_true', help="update ecs info. (e.g. --update instance ip weight)")
group.add_argument('-g', '--get', action='store_true', help='get slb info. (e.g. --get instance)')

args = parser.parse_args()
# print(args.add)
# print(args.LIST)

if args.add:
    # print(args.add)
    if len(args.LIST) != 3:
        help_doc()
        sys.exit(1)
    instance = args.LIST[0]
    ip = args.LIST[1]
    weight = args.LIST[2]
    add_slb_ecs(instance, ip, weight)

elif args.delete:
    if len(args.LIST) != 2:
        help_doc()
        sys.exit(1)
    print(args.delete)
    instance = args.LIST[0]
    ip = args.LIST[1]
#    weight = args.LIST[2]
    delete_slb_ecs(instance, ip)

elif args.update:
    # print(args.update)
    if len(args.LIST) != 3:
        help_doc()
        sys.exit(1)
    instance = args.LIST[0]
    ip = args.LIST[1]
    weight = args.LIST[2]
    update_slb_ecs(instance, ip, weight)


elif args.get:
    # print(len(args.LIST))
    if len(args.LIST) != 1:
        help_doc()
        sys.exit(1)

    instance = args.LIST[0]
    get_slb_info(instance)
    # print(args.get)
else:
    help_doc()
    sys.exit(1)
