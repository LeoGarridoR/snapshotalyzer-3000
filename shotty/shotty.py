import boto3
import botocore
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
def cli():
    """Shotty administra snapshots"""

@cli.group('snapshots')
def snapshots():
    """Comandos para snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
     help="Sólo snapshots para el proyecto (tag Project:<name>)")
def list_volumes(project):
    "Lista los snapshots de los volumenes en las instancias EC2"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
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
    """Comandos para volumenes"""

@volumes.command('list')
@click.option('--project', default=None,
     help="Sólo volumenes para el proyecto (tag Project:<name>)")
def list_volumes(project):
    "Lista los volumenes de las instancias EC2"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group('instances')
def instances():
    """Comandos para las instancias"""

@instances.command('snapshot',
     help="Crea snapshots de todos los volumenes")
@click.option('--project', default=None,
     help="Sólo instancias para el proyecto (tag Project:<name>)")
def create_snapshots(project):
    "Crea snapshots para instancias EC2"

    instances = filter_instances(project)

    for i in instances:
        print("Deteniendo {0}...".forma(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print(" Creando snapshots de {0}...".format(v.id))
            v.create_snapshot(Description="Creado por Snapshotalyzer 3000")

        print("Starting {0}...".format(i.id))

        i.start()
        i.wait_until_running()

    print("Trabajo terminado!")

    return

@instances.command('list')
@click.option('--project', default=None,
     help="Sólo instancias para el proyecto (tag Project:<name>)")
def list_instances(project):
    "Lista las instancias EC2"

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
   help='Solamente instancias de proyectos')
def stop_instances(project):
    "Detener instancias EC2"

    instances = filter_instances(project)

    for i in instances:
        print("Deteniendo {0}....".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("  No pudo detener {0}. ".format(i.id) + str(e))
            continue

    return

@instances.command('start')
@click.option('--project', default=None,
   help='Solamente instancias de proyectos')
def stop_instances(project):
    "Iniciar instancias EC2"

    instances = filter_instances(project)

    for i in instances:
        print("Iniciando {0}....".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("  No se pudo iniciar {0}. ".format(i.id) + str(e))
            continue

    return

if __name__ == '__main__':
    cli()
