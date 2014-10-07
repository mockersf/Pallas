(function() {
  var app = angular.module('target', []);

  app.controller('targetController', [ '$http', function($http){
    this.browsers = ['PhantomJS', 'Firefox', 'Chrome', 'Internet Explorer'];
    this.browser = this.browsers[0];
    this.proxy = "no proxy";

    var target = this;

    $http.get('/default-target.json').success(function(data){
      target.url = data.url;
      if (data.proxy) {
        target.proxy = 'browsermob';
        target.proxy_path = data.proxy;
      }
      if (data.browser)
        target.browser = data.browser;
    });

    this.start = function() {
      config = {};
      config['url'] = target.url;
      config['browser'] = target.browser;
      config['proxy'] = target.proxy;
      config['proxy_path'] = target.proxy_path;
      $http.post('/start', JSON.stringify(config))
        .success(function(data){
          s = sigma.instances()[0];
          sigma.parsers.gexf(parseXml(data), s, placeNodes);
        });
    };
  }]);

  app.controller('detailsController', [ '$http', '$scope', function($http, $scope){
    $scope.site = "";
    $scope.node = "";

    $scope.set_node = function(node) {
      $scope.node = node;
    }
  }]);
})();
