
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
sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
echo 'LANG="en_US.UTF-8"' > /etc/default/locale
dpkg-reconfigure --frontend=noninteractive locales
