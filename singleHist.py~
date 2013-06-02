
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
	imgR, imgB, imgG = img.split() #get channels
	#imgR, imgG, imgB = img.split() #get channels

	arrR = numpy.asarray(imgR).astype('float64')
	arrG = numpy.asarray(imgG).astype('float64')
	arrB = numpy.asarray(imgB).astype('float64')
	

	#print arrR.max()

	num=(arrR - arrB)
	denom=(arrR + arrB)

	arr_ndvi=num/denom

	if arr_ndvi.max()>0:
		#plt.histogram(arrR)
		#plt.show()

		img_w,img_h=img.size
		vmin = -.1
		vmax = .4
	
		dpi=600. #need this to be floating point!
		fig_w=img_w/dpi
		fig_h=img_h/dpi
		#print fig_w,fig_h





		fig=plt.figure(figsize=(fig_w,fig_h),dpi=dpi)

		fig.set_frameon(False)

		ax_rect = [0.0, #left
		       0.0, #bottom
		       1.0, #width
		       1.0] #height
		ax = fig.add_axes(ax_rect)
		ax.yaxis.set_ticklabels([])
		ax.xaxis.set_ticklabels([])   
		ax.set_axis_off()
		ax.axes.get_yaxis().set_visible(False)
		ax.patch.set_alpha(0.0)

		axes_img = ax.imshow(arr_ndvi,
				          cmap=plt.cm.spectral, 
				          vmin = vmin,
				          vmax = vmax,
				          aspect = 'equal',
				          interpolation="nearest"
				         )


		x=arr_ndvi.ravel()
		a = plt.axes([.05,.1,.18,.18], axisbg='y')
		bins=numpy.arange(-1,1.1,.1)
		n, bins, patches = plt.hist(x, bins, normed=1,linewidth=.2)
		plt.setp(patches, 'facecolor', 'w', 'alpha', 0.75)
		plt.setp(a,xticks=[-1,0,1],yticks=[])
		plt.setp(a,xticks=[],yticks=[])
		plt.xticks(fontsize=2)

		x=arrR.ravel()
		a = plt.axes([.05,.7,.18,.18], axisbg='y')
		bins=numpy.arange(0,255,10)
		n, bins, patches = plt.hist(x, bins, normed=1,linewidth=.2)
		plt.setp(patches, 'facecolor', 'r', 'alpha', 0.75)
		plt.setp(a,xticks=[0,120,255],yticks=[])
		plt.setp(a,xticks=[],yticks=[])
		plt.xticks(fontsize=2)

		x=arrB.ravel()
		a = plt.axes([.05,.4,.18,.18], axisbg='y')
		bins=numpy.arange(0,255,10)
		n, bins, patches = plt.hist(x, bins, normed=1,linewidth=.2)
		plt.setp(patches, 'facecolor', 'b', 'alpha', 0.75)
		plt.setp(a,xticks=[0,120,255],yticks=[])
		plt.setp(a,xticks=[],yticks=[])
		plt.xticks(fontsize=2)

	#	axes_img = ax.imshow(arr_ndvi,
	#		              cmap=plt.cm.spectral, 
	#		              aspect = 'equal',
	#		              interpolation="nearest"
	#		             )

		# Add colorbar 
		#make an axis for colorbar
		cax = fig.add_axes([0.8,0.05,0.05,0.85]) #left, bottom, width, height
	
		cbar = fig.colorbar(axes_img, cax=cax)  #this resizes the axis


		#cbytick_obj = plt.getp(cbar.ax.axes, 'yticklabels')                #tricky
		cbar.ax.tick_params(labelsize=2) 

		#position of the colorbar
		#cbar.ax.yaxis.set_ticks_position('left')
	
		#color of the colorbar text
		#plt.setp(cbytick_obj, color='r')

		#diagnostic
		#print arr_ndvi


		fig.savefig(imageOutPath, 
		        dpi=dpi,
		        bbox_inches='tight',
		        pad_inches=0.0, 
		       )

		#plt.show()
		#needed to clear memory if used to process many frames ...
		#plt.show()
		fig.clf()
		plt.close()
		gc.collect()
	

	



outdir='./NDVIFolderBeePondFuschia5'

#indir='~/infpx-mov/videofolder/*.png'
indir='/home/dwblair/infpx-mov/beePondFuschiaPNG/*.png'
#indir='/home/dwblair/infrapix-mov/riverFolder/*.jpg'
import glob
files= sorted(glob.glob(indir))
#print files
for f in files:
	inFilePath=f
	inFileName= os.path.basename(f)
	outFileName='ndvi_'+inFileName
	outFilePath= os.path.join(outdir,outFileName)
	ndvi(inFilePath,outFilePath)
	print outFilePath
