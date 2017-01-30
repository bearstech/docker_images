import subprocess

TEMPLATE = '''
from {os}:{version}

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y python{py}
'''

TESTING = r'''
RUN apt-get install -y build-essential python{py}-dev python-virtualenv
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
    subprocess.check_call(['git', 'co', branch])
    with open('Dockerfile', 'w') as fd:
        fd.write(dockerfile)
    subprocess.check_call(['git', 'add', 'Dockerfile'])
    subprocess.call(['git', 'ci', '-m', 'update'])


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
        subprocess.check_call(['git', 'ci', '-m', 'update'])


if __name__ == '__main__':
    main()
