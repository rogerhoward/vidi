# Setting up server environment

# hostname
sudo hostname pastec

# Updates and installs

echo "updating apt-get repositories"
sudo apt-get update -q

echo "installing basic tools"
sudo apt-get install -y -q cmake git htop avahi-utils

echo "installing opencv and other dependencies"
sudo apt-get install -y -q libopencv-dev libmicrohttpd-dev libjsoncpp-dev

# Installing pastec
echo "bulding and installing pastec..."
cd /home/vagrant/

echo "...cloning pastec from github"
git clone https://github.com/Visu4link/pastec.git
chown -R vagrant:vagrant pastec
mkdir pastec/build
cd pastec/build

echo "...building pastec from source"
cmake ../
make
chown -R vagrant:vagrant /home/vagrant

echo "...downloading visualWordsORB"
curl http://pastec.io/files/visualWordsORB.tar.gz > visualWordsORB.tar.gz
tar -xzf visualWordsORB.tar.gz
rm -fR visualWordsORB.tar.gz

sudo cat > /etc/init.d/pastec <<EOF
#!/bin/sh
### BEGIN INIT INFO
# Provides:          pastec
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       A pastec service
### END INIT INFO

SCRIPT=sudo cd /home/vagrant/pastec/build/; sudo pastec -p 8000 visualWordsORB.dat &
RUNAS=vagrant

PIDFILE=/var/run/pastec.pid
LOGFILE=/var/log/pastec.log

start() {
  if [ -f /var/run/$PIDNAME ] && kill -0 $(cat /var/run/$PIDNAME); then
    echo 'Service already running' >&2
    return 1
  fi
  echo 'Starting service…' >&2
  local CMD="$SCRIPT &> \"$LOGFILE\" & echo \$!"
  su -c "$CMD" $RUNAS > "$PIDFILE"
  echo 'Service started' >&2
}

stop() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
    echo 'Service not running' >&2
    return 1
  fi
  echo 'Stopping service…' >&2
  kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
  echo 'Service stopped' >&2
}

uninstall() {
  echo -n "Are you really sure you want to uninstall this service? That cannot be undone. [yes|No] "
  local SURE
  read SURE
  if [ "$SURE" = "yes" ]; then
    stop
    rm -f "$PIDFILE"
    echo "Notice: log file is not be removed: '$LOGFILE'" >&2
    update-rc.d -f pastec remove
    rm -fv "$0"
  fi
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  uninstall)
    uninstall
    ;;
  retart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall}"
esac
EOF
sudo chmod +x /etc/init.d/pastec
sudo service pastec start

echo "pastec server should be available at http://localhost:8001/"