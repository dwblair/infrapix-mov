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
################################################################################
import os, sys, shutil, tempfile, errno, subprocess, glob

from infrapix.process_infrablue import ndvi
################################################################################
DEFAULT_VERBOSE = True
RENDER_METHODS = ['avconv','opencv']
################################################################################
def run_cmd(cmd):
    return subprocess.call(cmd, shell=True)
################################################################################
class Application:
    def __init__(self,
                 input_file,
                 output_file,
                 temp_dir = None,
                 verbose = False,
                 ):
        self.input_file  = input_file
        self.output_file = output_file
        self.temp_dir = temp_dir
        self.verbose = verbose
        self.ndvi_args = {}
        
    def set_ndvi_args(self, **kwargs):
        self.ndvi_kwargs = kwargs
        
    def render(self, **kwargs):
        method = kwargs.pop('method', 'avconv')
        cleanup = kwargs.pop('cleanup', False)
        try:
            if self.verbose:
                print "Rendering infrablue input movie '%s' to NDVI output movie '%s' usind the '%s' method" % (self.input_file, self.output_file, method)
            if method == 'avconv':
                self.render_avconv(**kwargs)
            if method == 'opencv':
                self.render_opencv(**kwargs)
        finally:
            if cleanup:
                if self.verbose:
                    print "Cleaning up; removing temp_dir: %s" % self.temp_dir
                shutil.rmtree(self.temp_dir)
            
    def render_avconv(self,
                      video_codec = 'libx264',
                      frame_rate  = 24.0,
                      vsync       = 'cfr',
                     ):
        #extract keyword arguments
        # Frame extraction
        #if input file is specified reduce it to frames, otherwise skip
        if not self.input_file is None:
            cmd = ["avconv"]
            cmd.append("-i %s" % self.input_file)
            cmd.append("-y") #overwrite files without prompting
            frame_file_format = os.sep.join((self.temp_dir,r"frame%09d.png")) #note that %d formatter is deliberately escaped for avconv's use
            cmd.append(frame_file_format) #output
            cmd = " ".join(cmd)
            if self.verbose:
                print "Extracting frames..."
                print "\tRunning command: %s" % cmd
            try:
                run_cmd(cmd)
            except KeyboardInterrupt:
                pass
        # NDVI conversion
        if self.verbose:
            print "Converting to all frames NDVI..."
        frame_file_pattern = os.sep.join((self.temp_dir,r"frame[0-9]*.png"))
        frame_filenames = sorted(glob.glob(frame_file_pattern))
        try:
            for frame_fn in frame_filenames:
                ndvi_fn = frame_fn.replace("frame","ndvi")
                if self.verbose:
                    print "generating ndvi plot: %s (press ctr-c to stop early)" % ndvi_fn
                ndvi(frame_fn,
                     imageOutPath   = ndvi_fn,
                     **self.ndvi_kwargs
                     )
        except KeyboardInterrupt:
            pass
        # Movie Encoding
        ndvi_file_format = os.sep.join((self.temp_dir,r"ndvi%09d.png"))
        cmd = ["avconv"]
        cmd.append("-y") #overwrite files without prompting
        cmd.append("-i %s" % ndvi_file_format)
        cmd.append("-c:v %s" % video_codec)
        cmd.append("-r %f" % frame_rate)
        cmd.append("-vsync %s" % vsync)
        cmd.append(self.output_file) #output
        cmd = " ".join(cmd)
        if self.verbose:
            print "Rendering movie..."
            print "\tRunning command: %s" % cmd
        try:
            run_cmd(cmd)
        except KeyboardInterrupt:
            pass
        
    def render_opencv(self):
        import warnings
        warnings.warn("This rendering method is experimental and may not work on\
                       your system, depending on codec availability and settings.")
        try:
            import cv, cv2
            video_in = cv2.VideoCapture(self.input_file)
            #extract properties from the video file
            fourcc  = int(video_in.get(cv.CV_CAP_PROP_FOURCC))       #video codec index
            fps     = video_in.get(cv.CV_CAP_PROP_FPS)
            frame_w = int(video_in.get(cv.CV_CAP_PROP_FRAME_WIDTH))
            frame_h = int(video_in.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
            
            video_out = cv2.VideoWriter(self.output_file,
                                        fourcc = fourcc,
                                        fps    = fps,
                                        frameSize = (frame_w,frame_h),
                                        isColor = 1,
                                        )
            #read in a frame
            success, img = video_in.read()
            while success:
                #convert the frame
                #write the frame
                video_out.write(img)
                #read in the next frame
                success, img = video_in.read()
        finally:
            video_in.release()
            #video_out.release()
################################################################################
# parse commandline arguments
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file",
                        help = "input movie filename (required)",
                       )
    parser.add_argument("-o", "--output_file",
                        help    = "ouput movie filename",
                        default = None,
                       )
    parser.add_argument("-t", "--temp_dir",
                        help    = "directory to store intermediate data",
                        default = None,
                       )
    parser.add_argument("--vmin",
                        help    = "minimum NDVI value OR dynamic lower quantile fraction",
                        default = None,
                       )
    parser.add_argument("--vmax",
                        help    = "maximum NDVI value OR dynamic upper quantile fraction",
                        default = None,
                       )
    parser.add_argument("-d", "--dynamic_range",
                        help    = "interpret vmin and vmax as fractional quantile boundaries for mapped values",
                        action  = "store_true",
                        default = False,
                       )
    parser.add_argument("--hide_colorbar",
                        help    = "do not overlay colorbar on video",
                        action  = "store_true",
                        default = False,
                       )
    parser.add_argument("--show_histogram",
                        help    = "overlay histograms on video",
                        action  = "store_true",
                        default = False,
                       )
    parser.add_argument("-r", "--framerate",
                        help    = "framerate of the rendered video",
                        default = 24.0,
                        type    = float,
                       )
    parser.add_argument("-m", "--method",
                        help    = "method of rendering ['avconv', 'opencv']",
                        default = 'avconv',
                       )
    parser.add_argument("-v", "--verbose",
                        help    = "increase output verbosity",
                        action  ="store_true",
                        default = DEFAULT_VERBOSE,
                       )
    args = parser.parse_args()
    
    #check input file argument
    input_file = args.input_file
    if input_file is None:
        if os.path.isdir(os.path.abspath(args.temp_dir)):
            print "Using input from temp_dir '%s'" % args.temp_dir
        else:
            print "No input was specified, use the '-i FILENAME' option. Exiting."
            sys.exit(errno.ENOENT)
    elif not os.path.isfile(input_file):
        print "Input file '%s' does not exist, exiting." % input_file
        sys.exit(errno.ENOENT)
    #check output file argument
    output_file = args.output_file
    if output_file is None:
        if not input_file is None:
            #construct the ouput name from the input with appended NDVI suffix
            base, ext = os.path.splitext(input_file)
            output_file = "%s_NDVI%s" % (base,ext)
        else:
            output_file = "output_NDVI.mp4"
    if os.path.isfile(output_file): #handle name collision
        print "-"*20
        res = ""
        while not res in ['O','o','Q','q']:
            res = raw_input("Output file '%s' already exists, (O)verwrite/(Q)uit?: " % output_file)
            if res in ['O','o']:
                pass #the file will be overwritten later
            elif res in ['Q','q']:
                sys.exit(0)
    #check the temp_dir argument
    cleanup  = False
    temp_dir = args.temp_dir
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="infrapix_")
        cleanup = True
        if args.verbose:
            print "Created temp_dir: %s" % temp_dir
    elif not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
    #check the method argument
    if not args.method in RENDER_METHODS:
        print "Method '%s' is not valid, use one of %r" % (args.method, RENDER_METHODS)
        sys.exit(errno.ENOENT)
        
    #configure the application
    app = Application(input_file  = input_file,
                      output_file = output_file,
                      temp_dir    = temp_dir,
                      verbose     = args.verbose,
                      )
    #setup the options of the NDVI plot
    vmin = args.vmin
    if not vmin is None:
        vmin = float(vmin)
    vmax = args.vmax
    if not vmin is None:
        vmax = float(vmax)
        
    app.set_ndvi_args(vmin = vmin,
                      vmax = vmax,
                      dynamic_range = args.dynamic_range,
                      show_colorbar  = not args.hide_colorbar,
                      show_histogram = args.show_histogram,
                      )
    #run the rendering process
    app.render(method = args.method,
               cleanup = True,
              )
    
    
###### testing the code #######
if __name__ == "__main__":
    main()

