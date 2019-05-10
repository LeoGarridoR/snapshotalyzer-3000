# snapshotalyzer-3000
Demo snapshot AWS EC2

## About

Este pryecto es una demo y utiliza boto3 para administrar snapshots de instancias EC2.

## Configuring

Se crea un perfil llamado shotty:
'aws configure --profile shotty'

Se crea un usuario IAM, con permisos para administrar EC2.

Para convertir lineas de codigo python a script se requiere retocar el codigo y agregar encabezado.

## Running

'pipenv run ipython shotty\shotty.py <command> <--project=PROJECT>'

*command* is list, start, stop
*project* is optional

## Parameters

Permite ejecutar comandos para EC2, en una cuenta accequible con credenciales.
