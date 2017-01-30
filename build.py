import subprocess
import sys

DEBIAN = '''
from {os}:{version}

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y python{py}
'''

DEBIAN_TESTING = r'''
RUN apt-get install -y build-essential python{py}-dev python-virtualenv
RUN mkdir -p /tmp/nuka_provisionning/nuka && \
    virtualenv -p python{py} /tmp/nuka_provisionning/nuka && \
    /tmp/nuka_provisionning/nuka/bin/pip install -U pip coverage
'''

all_branches = []


def gen_docker_file(os, version, py, testing=False):
    branch = '%s-%s-python%s' % (os, version, py)
    if py == '2':
        py = '2.7'
    dockerfile = DEBIAN.format(os=os, version=version, py=py)
    if testing:
        branch += '-testing'
        dockerfile += DEBIAN_TESTING.format(py=py)

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


debians = (
    ('wheezy', ('2',)),
    ('jessie', ('2', '3')),
    ('stretch', ('2', '3')),
)


def debian():
    for deb, pyvers in debians:
        for py in pyvers:
            gen_docker_file('debian', deb, py)
            gen_docker_file('debian', deb, py, testing=True)


def main():
    try:
        debian()
    finally:
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
