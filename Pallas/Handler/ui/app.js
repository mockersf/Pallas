(function() {
  var app = angular.module('target', []);

  app.factory('siteData', function() {
    return {
      site_url: '',
      site_name: '',
    };
  })

  app.controller('targetController', [ '$http', 'siteData', function($http, siteData){
    this.browsers = ['PhantomJS', 'Firefox', 'Chrome', 'Internet Explorer'];
    this.browser = this.browsers[0];
    this.proxy = "no proxy";
    this.siteData = siteData;
    this.validated = false;

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
      if (!this.validated) {
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
        this.siteData.site_url = target.url;
        this.validated = true;
      } else {
        sigma.instances()[0].graph.clear();
        sigma.instances()[0].refresh();
        this.siteData.site_url = '';
        this.validated = false;
      }
    };
  }]);

  app.controller('detailsController', [ '$http', '$scope', 'siteData', function($http, $scope, siteData){
    $scope.node = "";
    $scope.siteData = siteData;
    $scope.html_source = "";
    $scope.docu = null;
    $scope.css_selector = "";
    $scope.results = [];

    $scope.set_node = function(node) {
      $scope.node = node;
      if (node != "") {
        $http.get('/details/' + node + '.json').success(function(data){
          $scope.node_url = data.url;
          $scope.html_source = data.html;
          //fill the document with html_source
        });
      }
    };

    $scope.selectored = function() {
      $scope.results = $scope.docu.querySelectorAll($scope.css_selector);
    };
  }]);
})();
