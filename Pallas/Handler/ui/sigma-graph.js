var colors = {
  default: '#666',
  current: '#000',
  selected: '#66D',
  selectedCurrent: '#00F',
  connected: '#6D6',
  connectedCurrent: '#0F0',
  start: '#800'
};

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
  sigma.classes.graph.addMethod('isPathFrom', function(nodeId) {
    var k
    var isPathFrom = {}
    edges = this.edges()
    for (k in edges) {
      e = edges[k]
      if (e.source === nodeId)
        isPathFrom[e.id] = e;
    }
    return isPathFrom;
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
    var nodesToColor = s.graph.hasPathTo(nodeId);
    nodesToColor[nodeId] = e.data.node;
    var edgesToColor = s.graph.isPathFrom(nodeId);
    scp = angular.element(document.getElementById("details")).scope();
    if (last_node_click === nodeId) {
      nodesToColor = {};
      edgesToColor = {};
      last_node_click = undefined;
      scp.$apply(scp.set_node(""))
    } else {
      last_node_click = nodeId;
      scp.$apply(scp.set_node(nodeId))
    }

    s.graph.nodes().forEach(function(n) {
      if (nodesToColor[n.id]) {
        if (n.id === nodeId) {
          if (n.id == scp.siteData['current_node'])
            n.color = colors['selectedCurrent'];
          else
            n.color = colors['selected'];
        } else {
          if (n.id == scp.siteData['current_node'])
            n.color = colors['connectedCurrent'];
          else
            n.color = colors['connected'];
        }
      }
      else {
        if (n.id == scp.siteData['current_node'])
          n.color = colors['current'];
        else
          n.color = n.color_origin;
      }
    });

    s.graph.edges().forEach(function(n) {
      if (edgesToColor[n.id])
        n.color = colors['connected'];
      else
        n.color = n.color_origin;
    });

    s.refresh();
  });
})()

var last_node_click;

function placeNodes() {
  var i;
  var nodes = s.graph.nodes();
  var edges = s.graph.edges();
  var len = nodes.length;
  scp = angular.element(document.getElementById("details")).scope();
  for (i = 0; i < len; i++) {
      nodes[i].x = Math.random();
      nodes[i].y = Math.random();
      nodes[i].size = s.graph.degree(nodes[i].id);
      if (nodes[i].label == 'start')
          nodes[i].color = colors['start']
      else
          nodes[i].color = colors['default'];
      nodes[i].color_origin = nodes[i].color;
      if (nodes[i].id == scp.siteData['current_node'])
          nodes[i].color = colors['current']
  }
  len = edges.length;
  for (i = 0; i < len; i++) {
      edges[i].type = 'curvedArrow';
      edges[i].color = colors['default'];
      edges[i].color_origin = edges[i].color;
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
