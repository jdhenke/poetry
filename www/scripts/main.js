/* configure requirejs dependencies */
requirejs.config({
  shim: {
    'jquery.typeahead': ['jquery'],
    'd3': {
      exports: "d3",
    },
    'underscore': {
      exports: '_',
    },
    'backbone': {
      deps: ['underscore'],
      exports: 'Backbone',
    },
  }
});

/* main javascript for page */
requirejs(["celestrium/graphViewer"], 
  new GraphViewer("#workspace").init();
});