#!/usr/bin/env python
import subprocess
import time
import sys

sleep = str(int(time.time()))

DEBIAN_CLEAN = r'''
RUN apt-get clean && \
    rm -rf /root/.cache && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /etc/dpkg/dpkg.cfg.d/02apt-speedup && \
    rm -rf /var/cache/debconf/*-old && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/man/* /usr/share/groff/* /usr/share/info/* && \
    rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/*
'''

DEBIAN_NODOC = r'''
path-exclude /usr/share/doc/*
# we need to keep copyright files for legal reasons
path-include /usr/share/doc/*/copyright
path-exclude /usr/share/man/*
path-exclude /usr/share/groff/*
path-exclude /usr/share/info/*
# lintian stuff is small, but really unnecessary
path-exclude /usr/share/lintian/*
path-exclude /usr/share/linda/*
'''

TEMPLATES = dict(
    debian=r'''
from {image}

COPY 01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends \
        python{py} locales ca-certificates adduser curl gnupg

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales

{clean}

CMD ["/bin/bash", "-c", "while true; do sleep {sleep}; done"]
''',
    debian_testing=r'''
from {image}

RUN apt-get update && apt-get install -y \
        build-essential python{py}-dev python-virtualenv

RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python{py} /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage

{clean}

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
            image=image, py=py, clean=DEBIAN_CLEAN, sleep=sleep)
    else:
        image = '{os}:{version}'.format(os=os, version=version)
        dockerfile = TEMPLATES[os].format(
            image=image, py=py, clean=DEBIAN_CLEAN, sleep=sleep)

    print(branch)
    print('==========================================')
    print(dockerfile)
    subprocess.call(['git', 'branch', branch])
    subprocess.check_call(['git', 'co', branch])
    all_branches.append(branch)
    with open('Dockerfile', 'w') as fd:
        fd.write(dockerfile)
    if branch.startswith('debian'):
        with open('01_nodoc', 'w') as fd:
            fd.write(DEBIAN_NODOC)
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
