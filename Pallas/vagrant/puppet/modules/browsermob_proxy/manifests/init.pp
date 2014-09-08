class browsermob_proxy {
  package { ['default-jdk', 'unzip']:
    ensure => present;
  }
  ->
  exec { 'download browsermob proxy':
    command => '/usr/bin/wget -nv https://s3-us-west-1.amazonaws.com/lightbody-bmp/browsermob-proxy-2.0-beta-9-bin.zip',
    creates => '/home/vagrant/browsermob-proxy-2.0-beta-9-bin.zip',
  }
  ->
  exec { 'unzip browsermob proxy':
    command => '/usr/bin/unzip browsermob-proxy-2.0-beta-9-bin.zip',
    require => Exec['download browsermob proxy']
  }
  ->
  package { ['browsermob-proxy']:
    ensure => present,
    provider => pip,
  }
}