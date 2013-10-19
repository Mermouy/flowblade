"""
    Flowblade Movie Editor is a nonlinear video editor.
    Copyright 2012 Janne Liljeblad.

    This file is part of Flowblade Movie Editor <http://code.google.com/p/flowblade>.

    Flowblade Movie Editor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Flowblade Movie Editor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Flowblade Movie Editor.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Module holds current editor state.

Accessor methods are there mainly to improve code readability elsewhere.

We're using BIG_METHOD_NAMES() for state objects. This is a bit unusual
but looks good when reading code.
"""
# Edit modes
INSERT_MOVE = 0
OVERWRITE_MOVE = 1
ONE_ROLL_TRIM = 2
TWO_ROLL_TRIM = 3
SELECT_PARENT_CLIP = 4
COMPOSITOR_EDIT = 5
ONE_ROLL_TRIM_NO_EDIT = 6
TWO_ROLL_TRIM_NO_EDIT = 7
SLIDE_TRIM = 8
SLIDE_TRIM_NO_EDIT = 9

# Project being edited
project = None

# Wrapped MLT framework producer->consumer media player 
player = None                 

# Current edit mode
edit_mode = INSERT_MOVE

# Media file displayed in monitor when 'Clip' is pressed 
_monitor_media_file = None

# Flag for timeline/clip display in monitor
_timeline_displayed = True

# Used to alter gui layout and tracks configuration, set at startup
SCREEN_HEIGHT = -1
SCREEN_WIDTH = -1

# Runtime environment data
gtk_version = None
mlt_version = None
appversion = "0.10"
RUNNING_FROM_INSTALLATION = 0
RUNNING_FROM_DEV_VERSION = 1
app_running_from = RUNNING_FROM_INSTALLATION

# Cursor pos
cursor_on_tline = False

def current_is_move_mode():
    if ((edit_mode == INSERT_MOVE) or (edit_mode == OVERWRITE_MOVE)):
        return True
    return False

def current_is_active_trim_mode():
    if ((edit_mode == ONE_ROLL_TRIM) or (edit_mode == TWO_ROLL_TRIM) or (edit_mode == SLIDE_TRIM)):
        return True
    return False
    
def current_sequence():
    return project.c_seq

def current_bin():
    return project.c_bin
    
def PROJECT():
    return project
    
def PLAYER():
    return player
    
def EDIT_MODE():
    return edit_mode
    
def MONITOR_MEDIA_FILE():
    return _monitor_media_file

def get_track(index):
    return project.c_seq.tracks[index]

def timeline_visible():
    return _timeline_displayed

def mlt_version_is_equal_or_greater(test_version):
    mlt_parts = mlt_version.split(".")
    test_parts = test_version.split(".")
    if test_parts[0] >= mlt_parts[0] and test_parts[1] >= mlt_parts[1] and test_parts[2] >= mlt_parts[2]:
        return True
    
    return False
    
