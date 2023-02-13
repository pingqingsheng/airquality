import os
import sys

global package_directory
scr_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scr_directory)
package_directory = os.path.dirname(scr_directory)
sys.path.append(package_directory)