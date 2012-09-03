import StringIO
import Image
import re
import base64
import numpy as np
from scipy.misc import fromimage, toimage

def base64_2_PIL(imgData64):
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    imgb64 = dataUrlPattern.match(imgData64).group(2)
    return binary_2_PIL(base64.decodestring(imgb64))

def PIL_2_base64(pilImg, format='JPEG'):
    buf = StringIO.StringIO()
    pilImg.save(buf, format=format)
    return 'data:image/jpeg;base64,' + base64.encodestring(buf.getvalue())

def base64_2_array(imgData64):
    return fromimage(base64_2_PIL(imgData64))

def PIL_2_array(imgPIL):
    return fromimage(imgPIL)

def array_2_base64(imgArray):
    return PIL_2_base64(toimage(imgArray))

def binary_2_PIL(binaryImg):
    return Image.open(StringIO.StringIO(binaryImg))

