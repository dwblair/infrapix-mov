import os
from PIL import Image

THIS_DIR, _ = os.path.split(os.path.realpath(__file__))

test_img0 = Image.open(os.sep.join((THIS_DIR,"commode.jpg")))
