Infrapix
============

Python library and command line tools for processing 
[publiclab.org's Infragram](http://www.kickstarter.com/projects/publiclab/infragram-the-infrared-photography-project)
images and movies.  Here are two sample movies remixed from Chris Fastie's 
["Bee Pond Fuschia" Infrablue movie](http://publiclab.org/notes/cfastie/06-01-2013/bee-movie):

1. NDVI with fixed value range (-1.0 to 1.0) and overlayed R,G,B,NDVI histograms: http://youtu.be/39gmZC9B-jg

2. NDVI with dynamic range (vmin to  vmax in each frame ) and overlayed R,G,B,NDVI histograms:
http://youtu.be/3NEXxGdrEFc


### Installation

Debian Linux system (though Windows and OS X should also be possible with slightly different initial steps):

1. Install dependencies:
```sudo apt-get install git python-numpy python-matplotlib libav-tools ubuntu-restricted-extras```

2. Download lastest package from github:
```
    cd ~
    mkdir src
    cd src
    git clone https://github.com/Pioneer-Valley-Open-Science/infrapix.git
```

3. Run the setup script:
```
    cd infrapix
    sudo python setup.py install
```

### Converting an infrablue image to NDVI

- Go to a directory with an infrablue movie and run, e.g.:

```infrapix_single -i river.jpg --show_histogram -o ndvi_river.jpg```

For a sample infrablue image as input, grab "river.jpg" [here](http://i.publiclab.org/system/images/photos/000/000/476/medium/river.jpg), or below (get it via 'right-click save-as'):

![river.jpg](http://i.publiclab.org/system/images/photos/000/000/476/medium/river.jpg)

Running the above command should result in an image similar to the following:

![river_NDVI.jpg](http://i.publiclab.org/system/images/photos/000/000/477/medium/river_NDVI.jpg)

### Converting an infrablue movie to NDVI

1. Go to a directory with an infrablue movie and run, for example to get dynamic range:
```infrapix_render -i BeePondFuschia.mp4 --show_histogram -o BeePondFuschia_NDVI_hist_dynamic-range.mp4```
    
   to get fixed range:
```infrapix_render -i BeePondFuschia.mp4 --vmin -1.0 --vmax 1.0 --show_histogram -o BeePondFuschia_NDVI_hist_fixed-range.mp4```

2. Wait a really long time... enjoy.  Hint, run
```infrapix_render -h``` for help.
