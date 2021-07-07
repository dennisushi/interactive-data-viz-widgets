import matplotlib.pyplot as plt
import mpld3
import numpy as np



class LinkedView(plugins.PluginBase):
    """A simple plugin showing how multiple axes can be linked"""

    JAVASCRIPT = """
    mpld3.register_plugin("linkedview", LinkedViewPlugin);
    LinkedViewPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LinkedViewPlugin.prototype.constructor = LinkedViewPlugin;
    LinkedViewPlugin.prototype.requiredProps = ["idpts", "idline", "data"];
    LinkedViewPlugin.prototype.defaultProps = {}
    function LinkedViewPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LinkedViewPlugin.prototype.draw = function(){
      var fig = this.fig

      var pts = mpld3.get_element(this.props.idpts);
      var line = mpld3.get_element(this.props.idline);
      var data = this.props.data;

      function mouseover(d, i){
        line.data = data[i];
        line.elements().transition()
            .attr("d", line.datafunc(line.data))
            .style("stroke", this.style.fill);
      }
      pts.elements().on("mouseover", mouseover);
    };
    """

    def __init__(self, points, line, linedata):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedview",
                      "idpts": utils.get_id(points, suffix),
                      "idline": utils.get_id(line),
                      "data": linedata}
  """
  fig, ax = plt.subplots(2)

  # scatter periods and amplitudes
  np.random.seed(0)
  s = 20
  P = 0.2 + np.random.random(size=s)
  A = np.random.random(size=s)
  x = np.linspace(0, 10, 100)
  data = np.array([[x, Ai * np.sin(x / Pi)]
                   for (Ai, Pi) in zip(A, P)])
  points = ax[1].scatter(P, A, c=P + A,
                         s=200, alpha=0.5)
  ax[1].set_xlabel('Period')
  ax[1].set_ylabel('Amplitude')

  # create the line object
  lines = ax[0].plot(x, 0 * x, '-w', lw=3, alpha=0.5)
  ax[0].set_ylim(-1, 1)

  ax[0].set_title("Hover over points to see lines")

  # transpose line data and add plugin
  linedata = data.transpose(0, 2, 1).tolist()
  plugins.connect(fig, LinkedView(points, lines[0], linedata))

  mpld3.display()
  #mpld3.fig_to_html(fig)
  """
  
 class MouseXXXPosition(plugins.PluginBase):
    """Like MousePosition, but only show the X coordinate"""

    JAVASCRIPT="""
  mpld3.register_plugin("mousexxxposition", MouseXXXPositionPlugin);
  MouseXXXPositionPlugin.prototype = Object.create(mpld3.Plugin.prototype);
  MouseXXXPositionPlugin.prototype.constructor = MouseXXXPositionPlugin;
  MouseXXXPositionPlugin.prototype.requiredProps = ["labels"];
  MouseXXXPositionPlugin.prototype.defaultProps = {
    fontsize: 12,
    fmt: "0d",
    voffset: 10,
    hoffset: 0,
    css: ""
  };
  function MouseXXXPositionPlugin(fig, props) {
    mpld3.Plugin.call(this, fig, props);
  }
  MouseXXXPositionPlugin.prototype.draw = function() {
    var labels = this.props.labels;
    var labels_ymax = labels.length; 
    var labels_xmax = labels[0].length; 

    var fig = this.fig;
    var is_in = 1; 
    var fmt = d3.format(this.props.fmt);
    var tooltip = d3.select("body").append("div")
                .attr("class", "mpld3-tooltip")
                .style("position", "absolute")
                .style("z-index", "100")
                .style("visibility", "hidden");
    
    var styles = this.props.css
    var styleSheet = document.createElement("style")
    styleSheet.type = "text/css"
    styleSheet.innerText = styles
    document.head.appendChild(styleSheet)

    var coords = fig.canvas.append("text").attr("class", "mpld3-coordinates").style("text-anchor", "end").style("font-size", this.props.fontsize).attr("x", this.fig.width - 5).attr("y", this.fig.height - 5);
    for (var i = 0; i < this.fig.axes.length; i++) {
      var update_coords = function() {
        var ax = fig.axes[i];
        return function() {
          var pos = d3.mouse(this);
          var x = Math.floor(ax.x.invert(pos[0]));
          var y = Math.floor(ax.y.invert(pos[1]));

          var left = 0;

          if (y<0){
            y = 0;
            left = 1;
          }
          else if(y >labels_ymax - 1 ){
            y = labels_ymax;
            left = 1;
          }

          if (x<0){
            x = 0;
            left = 1;
          }
          else if(x > labels_xmax-1){
            x = labels_xmax;
            left = 1;
          }

          if (left == 0){
            var label_xy = labels[y][x];

            tooltip.html( "X:" + fmt(x)+"<br>"+
                          "Y:" + fmt(y)+"<br>"+
                          label_xy)
                    .style("visibility", "visible")

            //var vo = this.props.voffset;
            //var ho = this.props.hoffset;
            var vo = 0;
            var ho = 15;
            tooltip
                  .style("top", d3.event.pageY + vo + "px")
                  .style("left",d3.event.pageX + ho + "px");
          }
          else if (left==1){
            tooltip.html("").style("visibility","hidden")
          }
        };
      }();

      var leave = function(){
        return function(){
          console.log("LEFT");
          is_in = 0;
        }
      }();

      fig.axes[i].baseaxes
        .on("mousemove", update_coords).bind(this)
        .on("mouseout", leave);
        //function() {tooltip.html.style("visibility", "hidden");});
    }
  };"""

    def __init__(self, fontsize=12, fmt="8.0f", labels=[[]], 
                        voffset=10, hoffset=0, css=""):
        #default_css = 
        self.dict_ = {"type": "mousexxxposition",
                      "fontsize": fontsize,
                      "fmt": fmt, 
                      "labels": labels,
                      "voffset": voffset,
                      "hoffset":hoffset,
                      "css":css}

  """
    css = "/""
  .mpld3-tooltip{
    color: #101010;
    background-color: #ffffff;
    padding: 10px;
    border-radius: 5px;
  }
  "/""

  fig, ax = plt.subplots()

  # scatter periods and amplitudes
  np.random.seed(0)
  s = 20
  P = 0.2 + np.random.random(size=s)
  A = np.random.random(size=s)
  x = np.linspace(0, 10, 100)
  data = np.array([[x, Ai * np.sin(x / Pi)]
                   for (Ai, Pi) in zip(A, P)])

  im = ax.imshow(map.pixel_map)
  #plt.show()
  # transpose line data and add plugin
  linedata = data.transpose(0, 2, 1).tolist()
  #labels = np.empty((100,100), dtype="<U10")
  #labels = [[1,1],[0,0]]

  labels = []
  h, w = map.pixel_map.shape[:2]
  for i in range (h):
    labels.append([])
    for j in range(w):
      labels_ij = ""
      labels_ij += "name: "+ map.tile_map[i][j].tile_type.name
      labels[i].append( labels_ij )

  plot_margin = 0.25

  x0, x1, y0, y1 = plt.axis()
  plt.axis((x0 - plot_margin,
            x1 + plot_margin,
            y0 - plot_margin,
            y1 + plot_margin))

  plugins.connect(fig, MouseXXXPosition(labels = labels, css=css))

  mpld3.display()
  """
