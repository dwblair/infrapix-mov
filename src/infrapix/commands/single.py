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
################################################################################
def run_cmd(cmd):
    return subprocess.call(cmd, shell=True)
################################################################################
class Application:
    def __init__(self,
                 input_file,
                 output_file,
                 verbose = False,
                 ):
        self.input_file  = input_file
        self.output_file = output_file
        self.verbose = verbose
        self.ndvi_args = {}
        

    def set_ndvi_args(self, **kwargs):
        self.ndvi_kwargs = kwargs
        
    def render(self, **kwargs):
        cleanup = kwargs.pop('cleanup', False)
        try:
            if self.verbose:
                print "Rendering infrablue input image '%s' to NDVI output image '%s'" % (self.input_file, self.output_file)
            self.render_single(**kwargs)
        except KeyboardInterrupt:
            pass

    def render_single(self):
        if not self.input_file is None and not (self.output_file is None):
            print self.input_file, self.output_file
            if self.verbose:
                print "Converting to NDVI..."
            try:
                ndvi(self.input_file,self.output_file,**self.ndvi_kwargs)
            except KeyboardInterrupt:
                pass

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
    parser.add_argument("--vmin",
                        help    = "minimum NDVI value",
                        default = None,
                       )
    parser.add_argument("--vmax",
                        help    = "maximum NDVI value",
                        default = None,
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
    parser.add_argument("-v", "--verbose",
                        help    = "increase output verbosity",
                        action  ="store_true",
                        default = DEFAULT_VERBOSE,
                       )
    args = parser.parse_args()
    
    #check input file argument
    input_file = args.input_file
    if input_file is None:
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
            output_file = "output_NDVI.png"
    if os.path.isfile(output_file): #handle name collision
        print "-"*20
        res = ""
        while not res in ['O','o','Q','q']:
            res = raw_input("Output file '%s' already exists, (O)verwrite/(Q)uit?: " % output_file)
            if res in ['O','o']:
                pass #the file will be overwritten later
            elif res in ['Q','q']:
                sys.exit(0)
    #configure the application
    app = Application(input_file  = input_file,
                      output_file = output_file,
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
                      show_colorbar  = not args.hide_colorbar,
                      show_histogram = args.show_histogram,
                      )
    #run the rendering process
    app.render()
    
    
###### testing the code #######
if __name__ == "__main__":
    main()

