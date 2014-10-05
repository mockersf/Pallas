class python-modules {
  package { ['libx32z1-dev', 'libxml2-dev', 'libxslt1-dev', 'python-dev']:
    ensure => present,
  }
  package { ['selenium', 'flask', 'lxml', 'pygexf']:
    ensure => present,
    provider => pip,
  }
  package { ['pytest', 'pytest-cov']:
    ensure => present,
    provider => pip,
  }
  package { ['wtforms']:
    ensure => present,
    provider => pip,
  }
}
