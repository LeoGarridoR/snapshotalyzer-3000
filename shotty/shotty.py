import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Comandos para las instancias"""

@instances.command('list')
@click.option('--project', default=None,
     help="Sólo instancias para el proyecto (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            str(i.ami_launch_index),
            tags.get('Project', '<no project>')
            )))
    return

@instances.command('stop')
@click.option('--project', default=None,
   help='Solamente instacias de proyectos')
def stop_instances(project):
    "Detener instancias EC2"

    instances = filter_instances(project)

    for i in instances:
        print("Deteniendo {0}....".format(i.id))
        i.stop()

    return

if __name__ == '__main__':
    instances()
