from glue.config import data_factory
from glue.core import Data
from pathlib import Path
import stl
from stl import mesh
import numpy as np
from scipy import interpolate

__all__ = ['is_3dgnome', 'read_3dgnome']


def is_3dgnome(filename, **kwargs):
    return filename.endswith('.stl')

def fix_file(filename):
    """
    ASCII STL file from 3D GNOME have a broken first line
    so we patch it into another file, leaving the original
    untouched
    """
    new_filename = filename.replace('.stl','_fix.stl') # Kludgy
    
    with open(filename,'r') as f:
        first_line = f.readline()
        if 'pixelfacet' in first_line:
            new_line = first_line.replace('pixelfacet','pixel\nfacet')
            with open(new_filename,'w') as g:
                g.write(new_line)
                for line in f:
                    g.write(line)
        else:
            return filename
    return new_filename

@data_factory('3D GNOME Reader', is_3dgnome, priority=999)
def read_3dgnome(file_name):
    """
    Read a 3D GNOME STL file from https://3dgnome.cent.uw.edu.pl into glue

    3D GNOME STL files should be downloaded with the following settings:
    Line Segments = 10000
    Tube Radius = 0
    Radial Segments = 3 <-- Critical
    Save as ASCII STL

    """
    chromosome = '3'
    if chromosome == '3':
        chromosome_length = 198_022_430 #This is human chr3, we need to know this when we load
                                         #this file to set up the coordinates properly, but it
                                         #is not generally provided in the datafile. Query user?
        chromosome_length = 15_988_916 #This is mouse chr3
    new_filename = fix_file(file_name)
    tube = mesh.Mesh.from_file(new_filename, calculate_normals=False, mode=stl.Mode.ASCII)
    num_genome_steps = tube.v0.shape[0]//6 #6 because this? tube is defined with 6 points for each section
    genome_position = np.linspace(0,chromosome_length,num=num_genome_steps) 
    
    x = tube.v0[:,0][::6]
    y = tube.v0[:,1][::6]
    z = tube.v0[:,2][::6]
    
    #This interpolation does not look good
    #fx = interpolate.interp1d(genome_position,x,kind='slinear')
    #fy = interpolate.interp1d(genome_position,y,kind='slinear')
    #fz = interpolate.interp1d(genome_position,z,kind='slinear')

    ## This runs, but the linear interpolation does not look good.
    #num_genome_steps = num_genome_steps*2
    new_genome = np.linspace(0,chromosome_length,num=num_genome_steps*2)

    #newx = fx(new_genome)
    #newy = fy(new_genome)
    #newz = fz(new_genome)

    tck, u = interpolate.splprep([x,y,z],s=0,u=genome_position)

    newx, newy, newz = interpolate.splev(new_genome, tck)
    #newx, newy, newz = x,y,z
    chr_comp = ['chr'+chromosome]*len(new_genome)

    tubedata = Data(chr=chr_comp, cx=newx,cy=newy,cz=newz,genome_position=new_genome,label=Path(new_filename).stem)
    
    genome_stepsize = chromosome_length/num_genome_steps

    tubedata.meta = {'genome_stepsize':genome_stepsize, 'interp_function':tck}

    return tubedata