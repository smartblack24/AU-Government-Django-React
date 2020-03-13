import os

from fabric import Connection
from invocations.console import confirm
from invoke import task

STAGE_PROJECT_PATH = os.path.join('/', 'var', 'www', 'sitename')
PROD_PROJECT_PATH = os.path.join('/', 'home', 'ubuntu', 'sitename')
server = ''


def pull(server, PROJECT_PATH):
    with server.cd(PROJECT_PATH):
        print('Start getting files from bitbucket')
        if confirm('Stash and pull?'):
            server.run('git stash')
            if 'www' in PROJECT_PATH:
                server.run('git pull origin dev', pty=True)
            else:
                server.run('git pull', pty=True)
            server.run('git stash pop')
    print('Getting files from bitbucket completed')


def stop_server(server, PROJECT_PATH):
    with server.cd(PROJECT_PATH):
        if server.host == '128.199.74.157':
            server.run('docker-compose -f docker-compose.stage.yaml kill')
        elif server.host == 'ec2-54-206-38-56.ap-southeast-2.compute.amazonaws.com':
            server.run('/home/ubuntu/.local/bin/docker-compose -f docker-compose.prod.yaml kill')


def start_server(server, PROJECT_PATH):
    with server.cd(PROJECT_PATH):
        if server.host == '128.199.74.157':
            server.run('docker-compose -f docker-compose.stage.yaml up -d')
        elif server.host == 'ec2-54-206-38-56.ap-southeast-2.compute.amazonaws.com':
            server.run('/home/ubuntu/.local/bin/docker-compose -f docker-compose.prod.yaml up -d')


def rebuild_node(server, PROJECT_PATH):
    with server.cd(PROJECT_PATH):
        if server.host == '128.199.74.157':
            server.run('docker-compose -f docker-compose.stage.yaml run node yarn build')
        elif server.host == 'ec2-54-206-38-56.ap-southeast-2.compute.amazonaws.com':
            server.run('/home/ubuntu/.local/bin/docker-compose run node yarn build')


@task
def deploy(server):
    if confirm('Deploy to prod?'):
        server = Connection(
            'ubuntu@ec2-54-206-38-56.ap-southeast-2.compute.amazonaws.com')
        PROJECT_PATH = PROD_PROJECT_PATH
        print("Deploying to Production server")

    else:
        server = Connection('128.199.74.157')
        PROJECT_PATH = STAGE_PROJECT_PATH
        print("Deploying to Stage server")

    stop_server(server, PROJECT_PATH)
    pull(server, PROJECT_PATH)

    if confirm('Rebuild yarn?'):
        rebuild_node(server, PROJECT_PATH)
    start_server(server, PROJECT_PATH)
    print("Deploying to server is done!")


@task
def restart_stage_server(server):
    server = Connection('128.199.74.157')
    if confirm('Restart Staging server?'):
        stop_server(server, STAGE_PROJECT_PATH)
        start_server(server, STAGE_PROJECT_PATH)
        print('Stage server was restarted')

    else:
        print('Server restart is canseled')


@task
def restart_prod_server(server):
    server = Connection(
        'ubuntu@ec2-54-206-38-56.ap-southeast-2.compute.amazonaws.com')
    if confirm('Restart Production server?'):
        stop_server(server, PROD_PROJECT_PATH)
        start_server(server, PROD_PROJECT_PATH)
        print('Production server was restarted')

    else:
        print('Server restart is canseled')
