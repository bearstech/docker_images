#!/usr/bin/env python
import subprocess
import time
import sys

sleep = str(int(time.time()))

DEBIAN_BUILD = r'''
set -e

echo /docker_clean.sh
cat <<-EOF > /docker_clean.sh
set -e

apt-get clean
rm -rf /root/.cache
rm -rf /tmp/* /var/tmp/*
rm -rf /etc/dpkg/dpkg.cfg.d/02apt-speedup
rm -rf /var/cache/debconf/*-old
rm -rf /var/lib/apt/lists/*
rm -rf /usr/share/doc/*
rm -rf /usr/share/groff/* /usr/share/info/*
rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/*
find /usr/share/man -type f -delete
EOF

echo /etc/dpkg/dpkg.cfg.d/01_nodoc
cat <<-EOF > /etc/dpkg/dpkg.cfg.d/01_nodoc
path-exclude /usr/share/doc/*
path-exclude /usr/share/groff/*
path-exclude /usr/share/info/*
# lintian stuff is small, but really unnecessary
path-exclude /usr/share/lintian/*
path-exclude /usr/share/linda/*
path-exclude /usr/share/locale/*
path-include /usr/share/locale/locale.alias
path-include /usr/share/locale/en*
EOF

apt-get update && apt-get -y dist-upgrade
apt-get install -y --no-install-recommends \
    python$1 locales ca-certificates adduser curl gnupg

# set a clean locale
sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
echo 'LANG="en_US.UTF-8"' > /etc/default/locale
dpkg-reconfigure --frontend=noninteractive locales

# make service start on apt install
echo "exit 0"> /usr/sbin/policy-rc.d
echo "echo N 3" > /sbin/runlevel
chmod +x /sbin/runlevel
'''

TEMPLATES = dict(
    debian=r'''
from {image}

COPY build.sh /docker_build.sh

RUN bash /docker_build.sh {py} && bash /docker_clean.sh

CMD ["/bin/bash", "-c", "while true; do sleep {sleep}; done"]
''',
    debian_testing=r'''
from {image}

RUN apt-get update && apt-get install -y \
        build-essential python{py}-dev python-virtualenv && \
    mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python{py} /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage && \
    bash /docker_clean.sh

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
        dockerfile = TEMPLATES[os].format(
            image=image, py=py, sleep=sleep)

    print(branch)
    print('==========================================')
    print(dockerfile)
    subprocess.call(['git', 'branch', branch])
    subprocess.check_call(['git', 'co', branch])
    all_branches.append(branch)
    with open('Dockerfile', 'w') as fd:
        fd.write(dockerfile)
    if branch.startswith('debian'):
        with open('build.sh', 'w') as fd:
            fd.write(DEBIAN_BUILD)
    subprocess.call(['rm', '-f', 'build.py', 'clean.sh', '01_nodoc'])
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
        with open('build.sh', 'w') as fd:
            fd.write(DEBIAN_BUILD)
        subprocess.check_call(['git', 'add', 'Dockerfile'])
        subprocess.check_call(['git', 'add', 'build.sh'])
        subprocess.call(['git', 'commit', '-m', 'update'])
        if '--push' in sys.argv:
            subprocess.call(['git', 'push', 'origin', 'master'])


if __name__ == '__main__':
    main()
