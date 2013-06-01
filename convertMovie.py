
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


# ffmpeg -i inputfile.avi -r 1 -f image2 image-%3d.jpeg
# ffmpeg -qscale 5 -r 20 -b 9600 -i img%04d.png movie.mp4

import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as numpy

from PIL import Image

def nir(imageInPath,imageOutPath):
	img=Image.open(imageInPath)
	imgN, imgG, imgB = img.split() #get channels
	arrR = numpy.asarray(imgN).astype('float64')
	#red=img[:,:,0]
	#arrR=numpy.asarray(red).astype('float64')

	arr_nir=arrR

	fig=plt.figure()
	fig.set_frameon(False)
	ax=fig.add_subplot(111)
	ax.set_axis_off()
	ax.patch.set_alpha(0.0)

	nir_plot = ax.imshow(arr_nir, cmap=plt.cm.gist_gray, interpolation="nearest")

	#fig.colorbar(nir_plot)
	fig.savefig(imageOutPath)

def ndvi(imageInPath,imageOutPath):
	img=Image.open(imageInPath)

	imgN, imgG, imgB = img.split() #get channels
	arrR = numpy.asarray(imgN).astype('float64')
	arrB = numpy.asarray(imgB).astype('float64')
	"""img = mpimg.imread(imageInPath)
	red=img[:,:,0]
	green=img[:,:,1]
	blue=img[:,:,2]

	arrR=np.asarray(red).astype('float64')
	arrG=np.asarray(green).astype('float64')
	arrB=np.asarray(blue).astype('float64')
	"""
	num=arrR - arrB
	num=(arrR - arrB)
	denom=(arrR + arrB)
	arr_ndvi=num/denom

	fig=plt.figure()
	fig.set_frameon(False)
	ax=fig.add_subplot(111)
	ax.set_axis_off()
	ax.patch.set_alpha(0.0)

	#custom_cmap=make_cmap_gaussianHSV(bandwidth=0.01,num_segs=1024)
	ndvi_plot = ax.imshow(arr_ndvi, cmap=plt.cm.spectral, interpolation="nearest")
	#ndvi_plot = ax.imshow(arr_ndvi, cmap=custom_cmap, interpolation="nearest")

	fig.colorbar(ndvi_plot)
	fig.savefig(imageOutPath)



outdir='./NDVIFolder'

import glob
files= sorted(glob.glob('./outFolder/*.png'))
for f in files:
	inFilePath=f
	inFileName= os.path.basename(f)
	outFileName='ndvi_'+inFileName
	outFilePath= os.path.join(outdir,outFileName)
	ndvi(inFilePath,outFilePath)
	print outFilePath
