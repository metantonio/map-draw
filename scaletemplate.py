from branca.element import Template, MacroElement

def leyenda(htmlMap):
    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>@Metantonio</title>
      <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
      
      <script>
      $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

      </script>
    </head>
    <body>

     
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
         border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 300px;'>

    <button type="button" class="collapsible">    
        <div class='legend-title'>Escala de Colores</div>
    </button> 
    <div class='legend-scale content'>
      <ul class='legend-labels'>
        <li><span style='background:red;opacity:0.7;'></span>100%</li>
        <li><span style='background:rgba(255, 85, 0, 1);opacity:0.7;'></span>90%</li>
        <li><span style='background:rgba(255, 170, 1, 1);opacity:0.7;'></span>80%</li>
        <li><span style='background:rgba(255, 255, 1, 1);opacity:0.7;'></span>70%</li>
        <li><span style='background:rgba(190, 235, 20, 1);opacity:0.7;'></span>60%</li>
        <li><span style='background:rgba(128, 215, 40, 1);opacity:0.7;'></span>50%</li>
        <li><span style='background:rgba(63, 195, 60, 1);opacity:0.7;'></span>40%</li>
        <li><span style='background:rgba(0, 175, 80, 1);opacity:0.7;'></span>30%</li>
        <li><span style='background:rgba(0, 113, 193, 1);opacity:0.7;'></span>20%</li>
        <li><span style='background:rgba(129, 159, 221, 1);opacity:0.7;'></span>10%</li>
        <li><span style='background:rgba(255, 205, 248, 1);opacity:0.7;'></span>0%</li>

      </ul>
    </div>
    </div>

    <script>
        var coll = document.getElementsByClassName("collapsible");
        var i;

        for (i = 0; i < coll.length; i++) {
          coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
              content.style.display = "none";
            } else {
              content.style.display = "block";
            }
          });
        }
        </script>
 
    </body>
    </html>

    <style type='text/css'>
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
        .collapsible {
          color: #777;
          cursor: pointer;
          background-color:rgba(255, 255, 255, 0.8);
          width: 100%;
          border: none;
          text-align: left;
          outline: none;
          font-size: 15px;
        }
        .active, .collapsible:hover {
          background-color:rgba(255, 255, 255, 0.8);
          opacity=0.7;
        }
        .content {
          padding: 18px;
          display: none;
          overflow: hidden;
          
        }

    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    return htmlMap.get_root().add_child(macro)

    #return htmlMap
