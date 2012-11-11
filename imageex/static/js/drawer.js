/* orignaly from
 * © 2009 ROBO Design
 * http://www.robodesign.ro
 */
$(function() {
	var defaultClassifier = "svc1";
	var canvaso, contexto;
	var loadedImages = {};
	var imageInfo = {
	   width: 0,
	   height: 0,
	   pos: { x: 0, y: 0 },
	   url: null
	};
	
	// Find the canvas element.
	canvaso = document.getElementById('imageView');
	if (!canvaso) {
	  alert('Error: I cannot find the canvas element!');
	  return;
	}
	
	// Get the 2D canvas context.
	contexto = canvaso.getContext('2d');
	if (!contexto) {
	  alert('Error: failed to getContext!');
	  return;
	}
	
	function createCanvas(id) {
	    var container = canvaso.parentNode;
	    var canvasTemp = document.createElement('canvas');
	    if (!canvasTemp) {
	      alert('Error: I cannot create a new canvas element!');
	      return null;
	    }
	    canvasTemp.id     = id;
	    canvasTemp.width  = canvaso.width;
	    canvasTemp.height = canvaso.height;
	    //container.appendChild(canvasTemp);
	    return canvasTemp;
	}
	
	function getSubCanvas(context,x,y,w,h) {
	   var canvasTemp = document.createElement('canvas');
	   var contextTemp = canvasTemp.getContext('2d');
	   canvasTemp.width  = w;
       canvasTemp.height = h;
       imageData = context.getImageData(x,y,w,h);
       contextTemp.putImageData(imageData, 0, 0);
       return canvasTemp;
	}
	
	// This object holds the implementation of each drawing tool.
	var tools = {};
	
	tools.brush = function(size) {
	    var tool = this;
	    this.started = false;
	    this.size = size | 4;
	    this.color = 'black';
	    this.maskcolor = this.color;
	    this.canvas = createCanvas('brushCanvas');
	    this.context = this.canvas.getContext('2d');
	    this.maskempty = true;
	    
	    // This is called when you start holding down the mouse button.
	    // This starts the pencil drawing.
	    this.mousedown = function(ev) {
	        tool.context.fillStyle = tool.maskcolor;
	        tool.context.strokeStyle = tool.maskcolor;
            tool.context.lineWidth = tool.size;
            contexto.fillStyle = tool.color;
            contexto.strokeStyle = tool.color;
            contexto.lineWidth = tool.size;
            
	        tool.context.beginPath();
            tool.context.moveTo(ev._x, ev._y);
            contexto.beginPath();
	        contexto.moveTo(ev._x, ev._y);
	        
	        tool.started = true;
	        tool.maskempty = false;
	    };
	
	    this.mousemove = function (ev) {
	      if (tool.started) {
	        tool.draw(ev._x, ev._y);
	        tool.context.moveTo(ev._x, ev._y);
	        contexto.moveTo(ev._x, ev._y);
	      }
	    };
	
	    this.mouseup = function (ev) {
	      if (tool.started) {
	        tool.mousemove(ev);
	        tool.started = false;
	      }
	    };
	
	    this.draw = function(x, y) {
	      var dotoffset = (tool.size > 1) ? tool.size/2 : tool.size;
	      
	      tool.context.lineTo(x, y);
	      tool.context.stroke();
		  //tool.context.beginPath();
          tool.context.fillRect((x-dotoffset), (y-dotoffset), tool.size, tool.size);

          contexto.lineTo(x, y);
          contexto.stroke();
          //contexto.beginPath();
          contexto.fillRect((x-dotoffset), (y-dotoffset), tool.size, tool.size);
	    };
	    
	    this.reset = function() {
          tool.context.clearRect(0, 0, tool.canvas.width, tool.canvas.height);
          tool.maskempty = true;
        };
	
	};
	
	
	tools.rectangle = function() {
	    var tool = this;
	    this.started = false;
	    this.color = 'black';
	    this.lineWidth = 2;
	    this.rectangle = null;
	    
	    this.mousedown = function (ev) {
	        contexto.fillStyle = tool.color;
            contexto.strokeStyle = tool.color;
            contexto.lineWidth = tool.lineWidth;
	        tool.started = true;
	        tool.rectangle = { x: ev._x, y: ev._y };
	    };
	
	    this.mousemove = function (ev) {
	      if (tool.started) {
	        resetCanvas();
	        tx = tool.rectangle.x;
	        ty = tool.rectangle.y;
	        contexto.strokeRect(tx, ty, ev._x - tx, ev._y - ty);
	      }
	    };
	
	    // This is called when you release the mouse button.
	    this.mouseup = function (ev) {
	      if (tool.started) {
	        tool.mousemove(ev);
	        tool.started = false;
	        tool.rectangle.width  = ev._x - tool.rectangle.x;
	        tool.rectangle.height = ev._y - tool.rectangle.y;
	        if(tool.rectangle.width < 0) {
	           tool.rectangle.width *= -1;
	           tool.rectangle.x -= tool.rectangle.width;
	        }
	        if(tool.rectangle.height < 0) {
	           tool.rectangle.height *= -1;
               tool.rectangle.y -= tool.rectangle.height;
            }
	      }
	    };
	    
	    this.reset = function() {
          tool.rectangle = null;
        };
	    
	};
	
	
    // The active tools instance.
    var activeTools = {
       brush: new tools.brush(),
       rectangle: new tools.rectangle()
    };
    
    var tool_current = 'rectangle';
    
    // The event handler for any changes made to the tool selector.
    function setTool(tool_type) {
        if(activeTools[tool_type]) {
           tool_current = tool_type;
        }
    }
    
	  
	function drawImage(imgUrl) {
    var image = loadedImages[imgUrl];
    if(image) {
       contexto.drawImage(image, imageInfo.pos.x, imageInfo.pos.y);
    } else {
      image = new Image();
      loadedImages[imgUrl] = image;
      image.src = imgUrl;
      imageInfo.url = imgUrl;
      image.onload = function() {
        if(image.width == canvaso.width) {
            var deltaH = canvaso.height - image.height;
            imageInfo.pos.y = Math.floor(deltaH/2);
        } else {
            var deltaW = canvaso.width - image.width;
                imageInfo.pos.x = Math.floor(deltaW/2);
        }
        contexto.drawImage(image, imageInfo.pos.x, imageInfo.pos.y);
        imageInfo.width = image.width;
        imageInfo.height = image.height;
      };
    }
	}
    
	// The general-purpose event handler. This function just determines the mouse 
	// position relative to the canvas element.
	function ev_canvas (ev) {
	    if (ev.layerX || ev.layerX == 0) { // Firefox
	      ev._x = ev.layerX;
	      ev._y = ev.layerY;
	    } else if (ev.offsetX || ev.offsetX == 0) { // Opera
	      ev._x = ev.offsetX;
	      ev._y = ev.offsetY;
	    }
	    
	    // Call the event handler of the tool.
	    var tool = activeTools[tool_current];
	    var func = tool[ev.type];
	    if (func) func(ev);
	}
	
	// Attach the mousedown, mousemove and mouseup event listeners.
	canvaso.addEventListener('mousedown', ev_canvas, false);
	canvaso.addEventListener('mousemove', ev_canvas, false);
	canvaso.addEventListener('mouseup',   ev_canvas, false);
  
  function applyMask(imageData, maskData) {
      var imgPixels = imageData.data;
      var maskPixels = maskData.data;
      var width = Math.min(imageData.width, maskData.width);
      var height = Math.min(imageData.height, maskData.height);
      var w4 = 4 * width;
      var h4 = 4 * height;
      var foregroundBak = false;
      for(var y = 0; y < h4; y+=4) {
          var imgOffset = y * imageData.width;
          var maskOffset = y * maskData.width;
          for(var x = 0; x < w4; x+=4) {
              var foreground = maskPixels[maskOffset + x] < 200;
              if(foreground != foregroundBak) {
                  imgPixels[imgOffset + x ] = 0;
                  imgPixels[imgOffset + x + 1] = 0;
                  imgPixels[imgOffset + x + 2] = 0;
              } else if(foreground) {
                imgPixels[imgOffset + x + 3] = 0x50;
            }
              foregroundBak = foreground;
          }
      }
  }
  
  function resetCanvas() {
      contexto.clearRect(0, 0, canvaso.width, canvaso.height); 
      if(imageInfo.url) drawImage(imageInfo.url);
  }
  
  function resetTools() {
      for(tool_name in activeTools) {
          var tool = activeTools[tool_name];
          if(tool.reset) tool.reset();
      }
  }

  $("#resetButton").click(function(e) {
      loading();
      reset(function() {
          doneLoading();
      });
  });
  
  function reset(callback) {
      $.ajax({
          type: "POST",
          beforeSend: function(request) {
              request.setRequestHeader("X-CSRFToken", $("#csrfmiddlewaretoken").val());
          },
          url: "segmentation/reset",
          success: function() {
             resetCanvas();
             resetTools();
             if(callback) callback();
          }
      });
  }
  
  $("#runSegmentation").click(function(e) {
    e.preventDefault();
    //var imgData = canvaso.toDataURL("image/png");
    if(imageInfo.url == null) return;
    var algo = $("#algo").val();
    var data = {};
    //data.img = imgData;
    data.width = canvaso.width;
    data.height = canvaso.height;
    data.originalImg = imageInfo.url;
    if(activeTools.rectangle && activeTools.rectangle.rectangle != null) {
        var rect = activeTools.rectangle.rectangle;
        rect.x -= imageInfo.pos.x;
        rect.y -= imageInfo.pos.y;
        data.rectangle = rect;
    }
    if((algo == "grabcut" || algo == "watershed") && !activeTools.brush.maskempty) {
        var scaledMaskCanvas = getSubCanvas(activeTools.brush.context, imageInfo.pos.x, imageInfo.pos.y, imageInfo.width, imageInfo.height);
        data.mask = scaledMaskCanvas.toDataURL("image/png");
    }
    if(algo == "watershed" && activeTools.brush.maskempty) {
        alert("Watershed algorithm needs your help, please mark the flower using the brush tool.");
        return;
    }
    loading();
    $.ajax({
        type: "POST",
        //beforeSend: function(request) {
        //    request.setRequestHeader("X-CSRFToken", $("#csrfmiddlewaretoken").val());
        //},
        url: "segmentation/"+algo,
        data: data,
        success: function(data) {
	        var mask = new Image();
	        mask.src = data.img;
	        mask.onload = function() {
	           var dx = imageInfo.pos.x;
	           var dy = imageInfo.pos.y;
	           resetCanvas();
	           resetTools();
               var imageData = contexto.getImageData(dx, dy, imageInfo.width, imageInfo.height);
               var maskCanvas = document.createElement('canvas');
               maskCanvas.width  = mask.width;
               maskCanvas.height = mask.height;
               var maskContext = maskCanvas.getContext('2d');
               maskContext.drawImage(mask, 0, 0);
               var maskData = maskContext.getImageData(0, 0, maskCanvas.width, maskCanvas.height);
               applyMask(imageData, maskData);
               contexto.putImageData(imageData, dx, dy);
               doneLoading();
	        }
        },
        error: function(xhr, textStatus, errorThrown) {
            doneLoading();
            error(xhr.responseText);
        }
    });
  });
  
  $("#runIdentification").click(function(e) {
    e.preventDefault();
    loading();
    $.ajax({
        type: "POST",
        //beforeSend: function(request) {
        //    request.setRequestHeader("X-CSRFToken", $("#csrfmiddlewaretoken").val());
        //},
        url: "learning/predict/"+defaultClassifier,
        success: function(data) {
            doneLoading();
            $('#resultDialogContent').html(data);
        },
        error: function(xhr, textStatus, errorThrown) {
            doneLoading();
            error(xhr.responseText);
        }
    });
  });
  
  $("#submitLearning").click(function(e) {
    e.preventDefault();
    var name = $('#name').val();
    if(name === null || name == "") {
        alert("Enter a name for this flower");
        return;
    }
    loading();
    $.ajax({
        type: "POST",
        //beforeSend: function(request) {
        //    request.setRequestHeader("X-CSRFToken", $("#csrfmiddlewaretoken").val());
        //},
        data: { name: name },
        url: "learning/learn/"+defaultClassifier,
        success: function(data) {
            doneLoading();
            alert("Learning successful !");
        },
        error: function(xhr, textStatus, errorThrown) {
            doneLoading();
            error(xhr.responseText);
        }
    });
  });
  
  $("#brushButton").click(function(e) {
    setTool("brush");
  });
  
  $("#rectangleButton").click(function(e) {
    setTool("rectangle");
  });
  
  $("#backgroundButton").click(function(e) {
    activeTools.brush.color = "black";
    activeTools.brush.maskcolor = "black";
  });
  
  $("#foregroundButton").click(function(e) {
    activeTools.brush.color = "gray";
    activeTools.brush.maskcolor = "gray";
  });
  
  $("#algo").change(function(e) {
    console.log($(this).val());
    $('#'+$(this).val()+'Dialog').modal();
  });

  function loading() {
    $("#canvas_loading").show();
  }

  function doneLoading() {
    $("#canvas_loading").hide();
  }

  function error(errMessage) {
    $('#errorDialogContent').html(errMessage);
    $('#errorDialog').modal();
  }
  
  var uploader = new plupload.Uploader({
		runtimes : 'gears,html5,flash,silverlight,browserplus',
		browse_button : 'uploadButton',
		max_file_size : '7mb',
		url :  '/upload',
		flash_swf_url : 'static/js/plupload/plupload.flash.swf',
		silverlight_xap_url : 'static/js/plupload/plupload.silverlight.xap',
		filters : [
			{title : "Image files", extensions : "jpg,jpeg,gif,png"}
		],
		resize : {width : 640, height : 480, quality : 95},
    multipart_params: {
       "canvas-size[width]": $('#imageView').width(),
       "canvas-size[height]": $('#imageView').height()
    },
	});

	uploader.init();

	uploader.bind('FilesAdded', function(up, files) {
		up.refresh();
    up.start();
    loading();
	});

	uploader.bind('Error', function(up, err) {
		alert("Error: "+err.code+", Message: "+err.message);
		up.refresh(); // Reposition Flash/Silverlight
	});

	uploader.bind('FileUploaded', function(up, file, res) {
    if(res.status == 200) {
      var response = JSON.parse(res.response);
      if(response.imgUrl) {
        drawImage(response.imgUrl);
      }
    } else {
      error((res.response && JSON.stringify(res.response)) || "Error "+res.status);
    }
    doneLoading();
	});
  
});

