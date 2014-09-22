class python-modules {
  package { ['selenium']:
    ensure => present,
    provider => pip,
  }
  package { ['pytest']:
    ensure => present,
    provider => pip,
  }
  package { ['pytest-cov']:
    ensure => present,
    provider => pip,
  }
  package { ['flask']:
    ensure => present,
    provider => pip,
  }
  package { ['wtforms']:
    ensure => present,
    provider => pip,
  }
}