(function() {
  var app = angular.module('target', []);

  app.factory('siteData', function() {
    return {
      site_url: '',
      site_name: '',
      current_node: null,
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
            target.siteData.current_node = data.current_page
            s = sigma.instances()[0];
            sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
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

    this.back_to_start = function() {
      $http.get('/back_to_start.json')
        .success(function(data){
          target.siteData.current_node = data.current_page
          s = sigma.instances()[0];
          sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
        });
    };
  }]);

  app.controller('detailsController', [ '$http', '$scope', 'siteData', function($http, $scope, siteData){
    $scope.node = "";
    $scope.siteData = siteData;
    $scope.html_source = "";
    $scope.docu = null;
    $scope.css_selector = "";
    $scope.results = [];
    $scope.selected = null;

    $scope.set_node = function(node) {
      $scope.node = node;
      $scope.results = [];
      $scope.docu = null;
      $scope.selected = null;
      if (node != "") {
        $http.get('/details/' + node + '.json').success(function(data){
          $scope.node_url = data.url;
          $scope.html_source = data.html;
          $scope.docu = (new DOMParser()).parseFromString($scope.html_source, 'text/html');
          $scope.has_path_from_current = data.has_path;
        });
      }
    };

    $scope.selectored = function() {
      var results = [].slice.call($scope.docu.querySelectorAll($scope.css_selector));
      $scope.results = [];
      $scope.selected = null;
      var i = 1;
      var match;
      results.forEach(function(result) {
        match = {
          name: 'match ' + i + ' for \'' + $scope.css_selector + '\'',
          outerHTML: result.outerHTML,
          object: result,
        }
        i++;
        $scope.results.push(match);
//        $scope.results.push(result.outerHTML);
      })
    };

    $scope.view_match = function(id) {
      $scope.selected = id;
    };

    $scope.go_to = function(id) {
      var connection = {};
      connection['css'] = $scope.css_selector;
      connection['nb'] = id;
      $http.post('/add_connection_and_go', JSON.stringify(connection))
        .success(function(data){
          $scope.siteData.current_node = data.current_page
          s = sigma.instances()[0];
          sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
        });
    };

    $scope.follow_existing_connections = function(page_id) {
      var query = {};
      query['target'] = page_id;
      $http.post('/follow_existing_connections', JSON.stringify(query))
        .success(function(data){
          $scope.siteData.current_node = data.current_page
          s = sigma.instances()[0];
          sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
        });
    };

  }]);
})();
