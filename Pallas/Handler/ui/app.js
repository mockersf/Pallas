(function() {
  var app = angular.module('target', []);

  app.controller('targetController', [ '$http', function($http){
    this.browsers = ['PhantomJS', 'Firefox', 'Chrome', 'Internet Explorer'];
    this.browser = this.browsers[0];

    var target = this;

    $http.get('/default-target.json').success(function(data){
      target.url = data.url;
      if (data.browser)
        target.browser = data.browser;
    });
    this.start = function() {
      $http.post('/start', '{"url": "' + target.url + '", "browser": "' + target.browser + '"}')
    };
  }]);

})();
