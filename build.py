import subprocess

TEMPLATE = '''
from {os}:{version}

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y python{py}
'''

TESTING = r'''
RUN apt-get install build-essential python{py}-dev python-virtualenv
RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python{py} /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage && \
'''


def gen_docker_file(os, version, py, testing=False):
    branch = '%s-%s-python%s' % (os, version, py)
    if py == '2':
        py = '2.7'
    dockerfile = TEMPLATE.format(os=os, version=version, py=py)
    if testing:
        branch += '-testing'
        dockerfile += TESTING.format(py=py)

    print(branch)
    print('==========================================')
    print(dockerfile)
    subprocess.call(['git', 'branch', branch])
    subprocess.call(['git', 'co', branch])


debians = (
    ('wheezy', ('2',)),
    ('jessie', ('2', '3')),
    ('stretch', ('2', '3')),
)

for deb, pyvers in debians:
    for py in pyvers:
        gen_docker_file('debian', deb, py)
        gen_docker_file('debian', deb, py, testing=True)
