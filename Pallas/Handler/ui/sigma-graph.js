(function() {
  sigma.classes.graph.addMethod('neighbors', function(nodeId) {
    var k
    var neighbors = {}
    var index = this.allNeighborsIndex[nodeId] || {};

    for (k in index)
      neighbors[k] = this.nodesIndex[k];

    return neighbors;
  });
  sigma.classes.graph.addMethod('hasPathTo', function(nodeId) {
    var k
    var hasPathTo = {}
    edges = this.edges()
    for (k in edges) {
      e = edges[k]
      if (e.source === nodeId)
        hasPathTo[e.target] = this.nodesIndex[e.target];
    }
    return hasPathTo;
  });

  var g = {
    nodes: [],
    edges: []
  };
  var s = new sigma({
    graph: g,
    container: 'graph-container',
    renderer: {
      container: document.getElementById('graph-container'),
      type: 'canvas'
    },
    settings: {
      minNodeSize: 4,
      maxNodeSize: 16,
      doubleClickEnabled: false,
      defaultEdgeArrow: 'target'
    }
  });
  sigma.plugins.dragNodes(s, s.renderers[0]);
  s.bind('clickNode', function(e) {
    var nodeId = e.data.node.id;
    var toColor = s.graph.hasPathTo(nodeId);
    toColor[nodeId] = e.data.node;

    s.graph.nodes().forEach(function(n) {
      if (toColor[n.id])
        n.color = '#0f0';
      else
        n.color = '#666';
    });
    s.refresh();
  });
})()

function placeNodes() {
  var i;
  var nodes = s.graph.nodes();
  var edges = s.graph.edges();
  var len = nodes.length;
  for (i = 0; i < len; i++) {
      nodes[i].x = Math.random();
      nodes[i].y = Math.random();
      nodes[i].size = s.graph.degree(nodes[i].id);
      nodes[i].color = '#666';
  }
  len = edges.length;
  for (i = 0; i < len; i++) {
      edges[i].type = 'curvedArrow';
  }
  s.refresh();
  s.startForceAtlas2();
  setTimeout(function() { s.killForceAtlas2(); }, 2000);
}

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
