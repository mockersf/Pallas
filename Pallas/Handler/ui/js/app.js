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
        config['name'] = target.name;
        config['browser'] = target.browser;
        config['proxy'] = target.proxy;
        config['proxy_path'] = target.proxy_path;
        $http.post('/start', JSON.stringify(config))
          .success(function(data){
            target.siteData.current_node = data.current_page
            s = sigma.instances()[0];
            sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
          });
        this.siteData.site_name = target.name;
        this.validated = true;
      } else {
        sigma.instances()[0].graph.clear();
        sigma.instances()[0].refresh();
        this.siteData.site_name = '';
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
    $scope.connections = [];
    $scope.selected = null;
    $scope.nodeTab = 'none';
    $scope.css_searched = false;

    $scope.reset_current_node = function() {
      $scope.node = "";
      $scope.results = [];
      $scope.connections = [];
      $scope.docu = null;
      $scope.selected = null;
      $scope.nodeTab = 'none';
      $scope.css_selector = "";
      $scope.css_searched = false;
    }

    $scope.set_node = function(node) {
      $scope.reset_current_node();
      if (node != "") {
        $scope.node = node;
        $http.get('/details/' + node + '.json').success(function(data){
          $scope.node_url = data.url;
          $scope.html_source = data.html;
          $scope.docu = (new DOMParser()).parseFromString($scope.html_source, 'text/html');
          $scope.has_path_from_current = data.has_path;
          $scope.nodeTab = 'cssSelector';
          if (node == "start")
            $scope.nodeTab = 'URL';
          data.connections.forEach(function(connection) {
            details = {
              connection: connection.connection,
              id: connection.id,
              name: connection.connection.type + " " + JSON.stringify(connection.connection.data)
            }
            $scope.connections.push(details);
          });
        });
      }
    };

    $scope.follow_connection = function(index) {
      connection_id = $scope.connections[index].id;
      $scope.reset_current_node();
      $http.get('/follow/' + connection_id + '.json').success(function(data){
        $scope.siteData.current_node = data.current_page
        s = sigma.instances()[0];
        sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
      });
    };

    $scope.selectored = function() {
      var results = [].slice.call($scope.docu.querySelectorAll($scope.css_selector));
      $scope.results = [];
      $scope.selected = null;
      $scope.css_searched = true;
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

    $scope.go_to_url = function() {
        $scope.reset_current_node();
        config = {};
        config['url'] = $scope.url;
        $http.post('/go_to_url', JSON.stringify(config))
          .success(function(data){
            $scope.siteData.current_node = data.current_page
            s = sigma.instances()[0];
            sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
          });
    };

    $scope.view_match = function(id) {
      $scope.selected = id;
    };

    $scope.go_to = function(id) {
      var connection = {};
      connection['css'] = $scope.css_selector;
      connection['nb'] = id;
      $scope.reset_current_node();
      $http.post('/add_connection_and_go', JSON.stringify(connection))
        .success(function(data){
          $scope.siteData.current_node = data.current_page
          s = sigma.instances()[0];
          sigma.parsers.gexf(parseXml(data.gexf), s, placeNodes);
        });
    };

    $scope.follow_existing_connections = function(page_id) {
      var query = {};
      $scope.reset_current_node();
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
