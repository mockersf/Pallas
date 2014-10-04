(function() {
  var parseXml;

  if (typeof window.DOMParser != "undefined") {
      parseXml = function(xmlStr) {
          return ( new window.DOMParser() ).parseFromString(xmlStr, "text/xml");
      };
  } else if (typeof window.ActiveXObject != "undefined" &&
         new window.ActiveXObject("Microsoft.XMLDOM")) {
      parseXml = function(xmlStr) {
          var xmlDoc = new window.ActiveXObject("Microsoft.XMLDOM");
          xmlDoc.async = "false";
          xmlDoc.loadXML(xmlStr);
          return xmlDoc;
      };
  } else {
      throw new Error("No XML parser found");
  }

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
        .success(function(data){
          var g = {
            nodes: [],
            edges: []
          };
          s = new sigma({
            graph: g,
            container: 'graph-container',
            renderer: {
              container: document.getElementById('graph-container'),
              type: 'canvas'
            },
            settings: {
              minNodeSize: 1,
              maxNodeSize: 16
            }
          });
          sigma.parsers.gexf(parseXml(data), s,
              function() {
                var i;
                var nodes = s.graph.nodes();
                var len = nodes.length;
                for (i = 0; i < len; i++) {
                    nodes[i].x = Math.random();
                    nodes[i].y = Math.random();
                    nodes[i].size = s.graph.degree(nodes[i].id);
                    nodes[i].color = nodes[i].center ? '#333' : '#666';
                }
                s.refresh();
                s.startForceAtlas2();
              }
          );
        });
    };

  }]);

})();
