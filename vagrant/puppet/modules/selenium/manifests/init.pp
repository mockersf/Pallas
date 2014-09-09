class selenium {
  package { ['selenium']:
    ensure => present,
    provider => pip,
  }
}