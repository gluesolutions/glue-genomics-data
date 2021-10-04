from glue.config import data_factory
from glue.core import Data
from pathlib import Path
import stl
from stl import mesh
import numpy as np

__all__ = ['is_3dgnome', 'read_3dgnome']


def is_3dgnome(filename, **kwargs):
    return filename.endswith('.stl')

def fix_file(filename):
    """
    By ASCII STL file from 3D GNOME have a broken first line
    """
    new_filename = filename.replace('.stl','_fix.stl') # Kludgy
    
    with open(filename,'r') as f:
        first_line = f.readline()
        if 'pixelfacet' in first_line:
            new_line = first_line.replace('pixelfacet','pixel facet')
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

    3D GNOME STL files must be downloaded with the following settings:
    Line Segments = 10000
    Tube Radius = 0
    Radial Segments = 3
    Save ASCII STL

    """
    chromosome_length = 198_022_430 #This is human chr3, we need to know this when we load
                                    #this file to set up the coordinates properly, but it
                                    #is not generally provided in the datafile. Query user?
    new_filename = fix_file(file_name)
    tube = mesh.Mesh.from_file(new_filename, calculate_normals=False, mode=stl.Mode.ASCII)
    genome_position = np.linspace(0,chromosome_length,num=tube.v0.shape[0]//3) #3 because tube is defined with triangles at smallest radius
    tubedata = Data(x=tube.v0[:,0][::3],y=tube.v0[:,1][::3],z=tube.v0[:,2][::3],pos=genome_position,label=Path(new_filename).stem)

    return tubedata