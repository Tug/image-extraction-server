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
    
	  
	function drawImage() {
	    var image = loadedImages[imageInfo.url];
	    if(image) {
	       contexto.drawImage(image, imageInfo.pos.x, imageInfo.pos.y);
	    } else {
		    image = new Image();
		    loadedImages[imageInfo.url] = image;
		    image.src = imageInfo.url;
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
        $('#loadingDialog').dialog(getCanvasCenteredDialogParams(300, 100));
        reset(function() {
            $('#loadingDialog').dialog('close');
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
  
    function getCanvasCenteredDialogParams(dialogWidth, dialogHeight) {
        var canvasOffset = $('#imageView').offset();
        var srollLeft = $(document).scrollLeft();
        var scrollTop = $(document).scrollTop();
        var loadingDialogX = canvasOffset.left + canvaso.width/2 - dialogWidth/2 - srollLeft;
        var loadingDialogY = canvasOffset.top + canvaso.height/2 - dialogHeight/2 - scrollTop;
        return { width: dialogWidth, height: dialogHeight, position: [loadingDialogX, loadingDialogY] };
    }
    
    function showErrorDialog(content) {
        var backup = $('#errorDialog').html();
        var params = {};
        if(content) {
            $('#errorDialog').append(content);
            params = getCanvasCenteredDialogParams(800, 600);
        } else {
            params = getCanvasCenteredDialogParams(200, 200);
        }
        params.buttons = {
            "Close": function() {
                $('#errorDialog').html(backup);
                $(this).dialog("close");
            }
        };
        $('#errorDialog').dialog(params);
        $('#errorDialog').scrollTop();
    }
    
	var uploader = new qq.FileUploader({
	    element: document.getElementById('fileUploader'),
	    action: '/upload-raw',
	    sizeLimit: 7340032, // 7MB
	    allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
	    //header: {"X-CSRFToken": $("#csrfmiddlewaretoken").val() },
	    params: {
	       //"X-CSRFToken": $("#csrfmiddlewaretoken").val(),
	       "canvas-size": { width: canvaso.width, height: canvaso.height}
	    },
	    onSubmit: function(id, fileName){
	       $('#loadingDialog').dialog(getCanvasCenteredDialogParams(300, 100));
	    },
	    onComplete: function(id, fileName, response, status) {
	       reset(function() {
               $('#loadingDialog').dialog('close');
           });
	       if(status == 200 && response && response.imgUrl) {
	           imageInfo.url = response.imgUrl;
	       } else if(response) {
	           showErrorDialog(response);
	       }
	    }
	});
  
  $("#submitSegmentation").click(function(e) {
    e.preventDefault();
    //var imgData = canvaso.toDataURL("image/png");
    if(imageInfo.url == null) return;
    $('#loadingDialog').dialog(getCanvasCenteredDialogParams(300, 100));
    var algo = $("input[name='algo']:checked").val();
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
               $('#loadingDialog').dialog('close');
	        }
        },
        error: function(xhr, textStatus, errorThrown) {
            $('#loadingDialog').dialog('close');
            showErrorDialog(xhr.responseText);
        }
    });
  });
  
  $("#submitIdentification").click(function(e) {
    e.preventDefault();
    $('#loadingDialog').dialog(getCanvasCenteredDialogParams(300, 100));
    $.ajax({
        type: "POST",
        //beforeSend: function(request) {
        //    request.setRequestHeader("X-CSRFToken", $("#csrfmiddlewaretoken").val());
        //},
        url: "learning/predict/"+defaultClassifier,
        success: function(data) {
            $('#loadingDialog').dialog('close');
            $('#resultDialog').dialog(getCanvasCenteredDialogParams(300, 500));
            $('#resultDialogContent').html(data);
        },
        error: function(xhr, textStatus, errorThrown) {
            $('#loadingDialog').dialog('close');
            showErrorDialog(xhr.responseText);
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
    $('#loadingDialog').dialog(getCanvasCenteredDialogParams(300, 100));
    $.ajax({
        type: "POST",
        //beforeSend: function(request) {
        //    request.setRequestHeader("X-CSRFToken", $("#csrfmiddlewaretoken").val());
        //},
        data: { name: name },
        url: "learning/learn/"+defaultClassifier,
        success: function(data) {
            $('#loadingDialog').dialog('close');
            alert("Learning successful !");
        },
        error: function(xhr, textStatus, errorThrown) {
            $('#loadingDialog').dialog('close');
            showErrorDialog(xhr.responseText);
        }
    });
  });
  
  $("input[name='tool']").click(function(e) {
    setTool(this.value);
    if(this.value == "brush") {
        $( "#brushTypeSelector" ).show();
    } else {
        $( "#brushTypeSelector" ).hide();
    }
  });
  
  $("input[name='brushType']").click(function(e) {
    if(this.value == "foreground") {
        activeTools.brush.color = "black";
        activeTools.brush.maskcolor = "black";
    } else if(this.value == "background") {
        activeTools.brush.color = "gray";
        activeTools.brush.maskcolor = "gray";
    }
  });
  
  $("input[name='algo']").click(function(e) {
    params = getCanvasCenteredDialogParams(350, 250);
    params.buttons = {
        "Ok": function() {
            $(this).dialog("close"); 
        }
    };
    $('#'+this.value+'Dialog').dialog(params);
  });
  
  $( "#resetButton" ).button();
  $( "#submitSegmentation" ).button();
  $( "#submitIdentification" ).button();
  $( "#submitLearning" ).button();
  $( "#toolSelector" ).buttonset();
  $( "#brushTypeSelector" ).buttonset();
  $( "#algoSelector" ).buttonset();

  /* disable submiting form with enter */
  document.onkeypress = function(evt) { 
	  var evt = (evt) ? evt : ((event) ? event : null);
	  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null); 
	  if ((evt.keyCode == 13) && (node.type=="text"))  {return false;} 
  }
  
});

