#!/usr/bin/python

import boto3
import click
#import os,sys
#import subprocess
#import glob
#from os import path

#f = open('C:/output.txt','w')
#sys.stdout = f

session = boto3.Session(profile_name='default',region_name='us-west-2')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "List EC2 instances"
    for i in ec2.instances.all():
        print(','.join((
          i.id,
          i.instance_type,
          i.placement['AvailabilityZone'],
          i.state['Name'],
          i.public_dns_name )))

    return

if __name__ == '__main__':
    list_instances()
