class python3 {
  package { ['python3']:
    ensure => present;
  }
  ->
  exec { 'easy_install':
    command => '/usr/bin/wget https://bootstrap.pypa.io/ez_setup.py -O - | /usr/bin/python3';
  }
  ->
  exec { 'install pip':
    command => '/usr/local/bin/easy_install pip';
  }
  ->
  exec { 'install selenium':
    command => '/usr/local/bin/pip install selenium';
  }
  ->
  exec { 'install browsermob proxy':
    command => '/usr/local/bin/pip install browsermob-proxy';
  }
  ->
  exec { '2to3 on browsermob proxy':
    command => '/usr/bin/2to3 -w /usr/local/lib/python3.2/dist-packages/browsermobproxy';
  }
  ->
  exec { 'manual modif for python3 to browsermob proxy':
    command => "/bin/sed -i \"s/resp.content/resp.content.decode('utf-8')/\" /usr/local/lib/python3.2/dist-packages/browsermobproxy/client.py";
  }
}
