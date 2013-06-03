infrapix-mov
============

The included script, "processNGB.py", will take one or more NGB images from a user-specified input directory and generate NDVI imagery in the user-specified output directory.

Note, if you'd like to process NGB files instead, you can comment out the line that reads: 

```
imgR, imgB, imgG = img.split() #get channels from NGB
```

and uncomment the line that reads:

```
imgR, imgG, imgB = img.split() #get channels from NBG
```

In order to process video files, first, extract all the frames into a folder:

``` 
ffmpeg -i inputMovie.avi  -f image2 ./outFolder/image-%04d.png
```

- then, run the python script to convert to NDVI.  The script has the folllowing options:

```
python processNGB.py inputdir outputdir vmin vmax histogramOption
```

- INPUTDIR: the input directory of images -- only the images you want to process.

- OUTPUTDIR: where you'd like the output images.

- VMIN, VMAX: the min/max values to display in the colormap of the NDVI output. 
 
- histogramOption:  1=show, 0=don't show histograms of R, B, and NDVI overlaid on the result image.  For example,

``` 
python processNGB.py ../infpx-mov/vidfolder/ ./out6/ .1 .8 1
```

has VMIN=.1, VMAX=.8, and includes the histogram option.

- then, recombine the extracted frames into a movie:

``` 
ffmpeg -qscale 5 -i ./NDVIFolder/ndvi_image-%04d.png movie.mp4
```
