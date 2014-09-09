class firefox {
  package { ['firefox', 'dbus-x11', 'xvfb']:
    ensure => present;
  }
}