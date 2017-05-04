
set -e

apt-get update && apt-get -y dist-upgrade
apt-get install -y --no-install-recommends \
    python{py} locales ca-certificates adduser curl gnupg
sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
echo 'LANG="en_US.UTF-8"' > /etc/default/locale
dpkg-reconfigure --frontend=noninteractive locales
