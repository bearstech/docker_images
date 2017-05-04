#!/usr/bin/env python
import subprocess
import time
import sys

sleep = str(int(time.time()))


TEMPLATES = dict(
    debian=r'''
from {image}

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python{py} ca-certificates adduser curl gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale \
    dpkg-reconfigure --frontend=noninteractive locales

CMD ["/bin/bash", "-c", "while true; do sleep {sleep}; done"]
''',
    debian_testing=r'''
from {image}

RUN apt-get update && apt-get install -y \
        build-essential python{py}-dev python-virtualenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python{py} /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ["/bin/bash", "-c", "while true; do sleep {sleep}; done"]
''',

    centos=r'''
from {image}

CMD ["/bin/bash", "-c", "while true; do sleep {sleep}; done"]
''',
    centos_testing=r'''
from {image}

RUN yum install -y -q \
    python-devel python-virtualenv \
    make automake gcc gcc-c++ kernel-devel

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

CMD ["/bin/bash", "-c", "while true; do sleep {sleep}; done"]
''',
)

all_branches = []


def gen_docker_file(os, version, py, testing=False):
    branch = '%s-%s-python%s' % (os, version, py)
    if py == '2':
        py = '2.7'
    if testing:
        image = 'bearstech/nukai:' + branch
        branch += '-testing'
        dockerfile = TEMPLATES[os + '_testing'].format(
            image=image, py=py, sleep=sleep)
    else:
        image = '{os}:{version}'.format(os=os, version=version)
        dockerfile = TEMPLATES[os].format(image=image, py=py, sleep=sleep)

    print(branch)
    print('==========================================')
    print(dockerfile)
    subprocess.call(['git', 'branch', branch])
    subprocess.check_call(['git', 'co', branch])
    all_branches.append(branch)
    with open('Dockerfile', 'w') as fd:
        fd.write(dockerfile)
    subprocess.call(['rm', '-f', 'build.py'])
    subprocess.check_call(['git', 'add', '-A'])
    subprocess.call(['git', 'commit', '-m', 'update'])
    if '--push' in sys.argv:
        subprocess.call(['git', 'push', 'origin', branch])


distros = (
    ('centos', (
        ('7', ('2',)),
    )),
    ('debian', (
        ('wheezy', ('2',)),
        ('jessie', ('2', '3')),
        ('stretch', ('2', '3')),
    )),
)


def linuxes():
    for distro, versions in distros:
        for ver, pyvers in versions:
            for py in pyvers:
                gen_docker_file(distro, ver, py)
                gen_docker_file(distro, ver, py, testing=True)


def main():
    try:
        linuxes()
    finally:
        subprocess.call(['git', 'co', 'debian-stretch-python3'])
        with open('Dockerfile') as fd:
            dockerfile = fd.read()
        subprocess.call(['git', 'co', 'master'])
        with open('Dockerfile', 'w') as fd:
            fd.write(dockerfile)
        subprocess.check_call(['git', 'add', 'Dockerfile'])
        subprocess.call(['git', 'commit', '-m', 'update'])
        if '--push' in sys.argv:
            subprocess.call(['git', 'push', 'origin', 'master'])


if __name__ == '__main__':
    main()
