
set -e

apt-get clean
rm -rf /root/.cache
rm -rf /tmp/* /var/tmp/*
rm -rf /etc/dpkg/dpkg.cfg.d/02apt-speedup
rm -rf /var/cache/debconf/*-old
rm -rf /var/lib/apt/lists/*
rm -rf /usr/share/doc/*
rm -rf /usr/share/man/* /usr/share/groff/* /usr/share/info/*
rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/*
