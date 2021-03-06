#!/usr/bin/python

import boto3
import click
#import os,sys
#import subprocess
#import glob
#from os import path

#f = open('C:/output.txt','w')
#sys.stdout = f

session = boto3.Session(profile_name='default',region_name='us-east-1')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters=[{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Script to Manages Snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snaphots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help="Only snapshots for project (tag Project:<name>)")
def list_snapshots(project):
    "List EC2 volumes snapshots"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(",".join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))

    return


@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(",".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""


@instances.command('snapshot',
    help="Create snapshot of volume")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create snapshots for Ec2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshot analyzer 3000")

        print("Starting {0}".format(i.id))

        i.start()
        i.wait_until_running()

    print("Jobs Done !")
    
    return

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        tags ={t['Key']: t['Value'] for t in i.tags or [] }
        print(','.join((
          i.id,
          i.instance_type,
          i.placement['AvailabilityZone'],
          i.state['Name'],
          i.public_dns_name,
          tags.get('Project')
          )))

    return

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project ")
def stop_instances(project):
    "Stop Ec2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project ")
def start_instances(project):
    "Start Ec2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return



if __name__ == '__main__':
    cli()
