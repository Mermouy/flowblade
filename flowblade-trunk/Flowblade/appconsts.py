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
Module contains constant values that are used by multiple modules in the application. 
"""

PROJECT_FILE_EXTENSION = ".flb"

# Media types for tracks or clips
UNKNOWN = 0
VIDEO = 1
AUDIO = 2
IMAGE = 3
RENDERED_VIDEO = 4 # not implemented
PATTERN_PRODUCER = 5
SYNC_AUDIO = 6
FILE_DOES_NOT_EXIST = 7
IMAGE_SEQUENCE = 8

# Sync states of sync child clips
SYNC_CORRECT = 0
SYNC_OFF = 1
SYNC_PARENT_GONE = 2

# Allowed editing operations on a track
FREE = 0        # All edits allowed
SYNC_LOCKED = 1 # No insert, splice out or one roll trim.
                # Allowed edits do not change positions of later clips 
LOCKED = 2      # No edits allowed

# Property types of mlt filters and mlt transitions in filters.xml
# and compositors.xml
PROP_INT = 0
PROP_FLOAT = 1
PROP_EXPRESSION = 2

# Display heights for tracks.
TRACK_HEIGHT_NORMAL = 50 # track height in canvas and column
TRACK_HEIGHT_SMALL = 25 # track height in canvas and column
TRACK_HEIGHT_SMALLEST = 20 # track height in canvas and column

# Notebook widths
NOTEBOOK_WIDTH = 600 # defines app min width with MONITOR_AREA_WIDTH
NOTEBOOK_WIDTH_WIDESCREEN = 500
TOP_ROW_HEIGHT = 500

# Property editing gui consts
PROPERTY_ROW_HEIGHT = 22
PROPERTY_NAME_WIDTH = 90

# Clip mute options
MUTE_NOTHING = 0
MUTE_AUDIO = 1
MUTE_VIDEO = 2
MUTE_ALL = 3

# Track mute options
TRACK_MUTE_NOTHING = 0
TRACK_MUTE_VIDEO = 1
TRACK_MUTE_AUDIO = 2
TRACK_MUTE_ALL = 3

# XML Attribute and element names used in multiple modules
NAME = "name"
ARGS = "args"
PROPERTY = "property"
MLT_SERVICE = "mlt_service"
EXTRA_EDITOR = "extraeditor"

# Available tracks configurations for flowblade
TRACK_CONFIGURATIONS = [(5,4),(4,3),(3,2),(2,1),(8,1),(1,8)]

# Thumbnail image dimensions
THUMB_WIDTH = 116
THUMB_HEIGHT = 87

# Magic value for no pan being applied for audio producer
NO_PAN = -99

# Copy of projectdata.SAVEFILE_VERSION is here to be available at savetime without importing projectdata
# This is set at application startup in app.main()
SAVEFILE_VERSION = -1

# This color is used in two modules
MIDBAR_COLOR = "#bdbdbd"

# Media log event types
MEDIA_LOG_ALL = -1 # no MediaLogEvent has this type, this used when filtering events for display
MEDIA_LOG_INSERT = 0
MEDIA_LOG_MARKS_SET = 1

# Rendered clip types
RENDERED_DISSOLVE = 0
RENDERED_WIPE = 1
RENDERED_COLOR_DIP = 2
RENDERED_FADE_IN = 3
RENDERED_FADE_OUT = 4

# Project proxt modes
USE_ORIGINAL_MEDIA = 0
USE_PROXY_MEDIA = 1
CONVERTING_TO_USE_PROXY_MEDIA = 2
CONVERTING_TO_USE_ORIGINAL_MEDIA = 3

# Autosave directory relative path
AUTOSAVE_DIR = "autosave/"
