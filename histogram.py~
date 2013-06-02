
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
#matplotlib.use('Agg')

from matplotlib import pyplot
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as numpy

from PIL import Image

import gc

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

	#needed to clear memory if used to process many frames ...
	fig.clf()
	plt.close()
	gc.collect()

def ndvi(imageInPath,imageOutPath):

	#img = mpimg.imread(imageInPath)
	#imgN=img[:,:,0]
	#imgB=img[:,:,2]

	img=Image.open(imageInPath)
	#imgR, imgG, imgB = img.split() #get channels
	imgR, imgG, imgB = img.split() #get channels

	#print imgR

	arrR = numpy.asarray(imgR).astype('float64')
	arrG = numpy.asarray(imgG).astype('float64')
	arrB = numpy.asarray(imgB).astype('float64')
	
	print arrR

	num=(arrR - arrB)
	denom=(arrR + arrB)

	arr_ndvi=num/denom

	fig=plt.figure()
	ax=fig.add_subplot(111)

	x=arrR[500]
	n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
	
	#print arrR
	#n,bins,patches=ax.hist(arrR,50)
	plt.show()
	
	fig.clf()
	plt.close()
	gc.collect()
	

	

ndvi('./river.jpg','./out.png')

