Pallas
======
[![Build Status](https://travis-ci.org/mockersf/Pallas.svg?branch=master)](https://travis-ci.org/mockersf/Pallas)
[![Coverage Status](https://coveralls.io/repos/mockersf/Pallas/badge.png)](https://coveralls.io/r/mockersf/Pallas)

Python application to help map a website and write tests as [page objects](https://code.google.com/p/selenium/wiki/PageObjects) using Selenium.
Can currently use Firefox or PhantomJS to browse, and browsermobprroxy to check http calls.


To Do
-----

* remove actions from node start
* stop redrawing nodes at random places after actions
* flow should be : input css selector -> search -> select an object -> beginning or continue -> choose action on object (click, input, ...) and order of actions -> validate connection
* going to an iframe of a page is a new page
* connection from multiple actions
* save / load current status as xml


Running Tests
-------------
Project includes a vagrant configuration with everything needed to run, and a script in /test that run pytest and starts Pallas.
```bash
$ cd vagrant
$ vagrant up
$ vagrant ssh
$ /Pallas/test/run_test.sh
```


See also
--------

* http://www.seleniumhq.org
* http://bmp.lightbody.net


Note on Patches/Pull Requests
-----------------------------

* Fork the project.
* Make your feature addition or bug fix.
* Add tests for it. This is important so I don't break it in a future version unintentionally.
* Send me a pull request. Bonus points for topic branches.


Copyright
---------

Copyright 2014 François Mockers

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
