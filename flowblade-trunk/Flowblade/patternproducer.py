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
Module is used to create pattern producer media objects for bins and 
corresponding mlt.Producers for timeline. 
"""
import copy
import gtk
import mlt

import appconsts
import dialogs
from editorstate import PROJECT
import gui
import respaths
import utils

# Pattern producer types
UNDEFINED = 0
COLOR_CLIP = 1
NOISE_CLIP = 2
EBUBARS_CLIP = 3

# ---------------------------------------------------- mene create callbacks
def create_color_clip():
    dialogs.color_clip_dialog(_create_color_clip_callback)

def _create_color_clip_callback(dialog, response_id, widgets):
    if response_id == gtk.RESPONSE_ACCEPT:
        entry, color_button = widgets
        name = entry.get_text()
        color_str = color_button.get_color().to_string()
        media_object = BinColorClip(PROJECT().next_media_file_id, name, color_str)
        PROJECT().add_patter_producer_media_object(media_object)
        _update_gui_for_patter_producer_media_object_add()

    dialog.destroy()

def create_noise_clip():
    media_object = BinNoiseClip(PROJECT().next_media_file_id, _("Noise"))
    PROJECT().add_patter_producer_media_object(media_object)
    _update_gui_for_patter_producer_media_object_add()

def create_bars_clip():
    media_object = BinColorBarsClip(PROJECT().next_media_file_id, _("EBU Bars"))
    PROJECT().add_patter_producer_media_object(media_object)
    _update_gui_for_patter_producer_media_object_add()

def _update_gui_for_patter_producer_media_object_add():
    gui.media_list_view.fill_data_model()
    gui.bin_list_view.fill_data_model()

# ---------------------------------------------------- interface
def create_pattern_producer(profile, pattern_producer_data):
    """
    pattern_producer_data is instance of projectdata.BinColorClip
    """
    if pattern_producer_data.patter_producer_type == COLOR_CLIP:
        clip = create_color_producer(profile, pattern_producer_data.gdk_color_str)
    elif pattern_producer_data.patter_producer_type == NOISE_CLIP:
        clip = _create_noise_clip(profile)
    elif pattern_producer_data.patter_producer_type == EBUBARS_CLIP:
        clip = _create_ebubars_clip(profile)
        
    clip.path = ""
    clip.filters = []
    clip.name = pattern_producer_data.name
    clip.media_type = appconsts.PATTERN_PRODUCER
    
    # Save creation data for cloning when editing or doing save/load 
    clip.create_data = copy.copy(pattern_producer_data)
    clip.create_data.icon = None # this is not pickleable, recreate when needed
    return clip

# --------------------------------------------------- producer create methods
def create_color_producer(profile, gdk_color_str):
    mlt_color = utils.gdk_color_str_to_mlt_color_str(gdk_color_str)

    producer = mlt.Producer(profile, "colour", mlt_color)
    producer.gdk_color_str = gdk_color_str

    return producer
        
def _create_noise_clip(profile):
    producer = mlt.Producer(profile, "frei0r.nois0r")
    return producer

def _create_ebubars_clip(profile):
    producer = mlt.Producer(profile, respaths.PATTERN_PRODUCER_PATH + "ebubars.png")
    return producer
    
# --------------------------------------------------- bin media objects
class AbstractBinClip:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.length = 15000
        self.type = appconsts.PATTERN_PRODUCER
        self.icon = None
        self.patter_producer_type = UNDEFINED # extending sets value

        self.mark_in = -1
        self.mark_out = -1

        self.create_icon()

    def create_icon(self):
        print "patter producer create_icon() not implemented"

class BinColorClip(AbstractBinClip):
    """
    Color Clip that can added to and edited in Sequence.
    """   
    def __init__(self, id, name, gdk_color_str):
        self.gdk_color_str = gdk_color_str
        AbstractBinClip.__init__(self, id, name)
        self.patter_producer_type = COLOR_CLIP

    def create_icon(self):
        icon = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, appconsts.THUMB_WIDTH, appconsts.THUMB_HEIGHT)
        pixel = utils.gdk_color_str_to_int(self.gdk_color_str)
        icon.fill(pixel)
        self.icon = icon

class BinNoiseClip(AbstractBinClip):
    def __init__(self, id, name):
        AbstractBinClip.__init__(self, id, name)
        self.patter_producer_type = NOISE_CLIP

    def create_icon(self):
        self.icon = gtk.gdk.pixbuf_new_from_file(respaths.PATTERN_PRODUCER_PATH + "noise_icon.png")

class BinColorBarsClip(AbstractBinClip):
    def __init__(self, id, name):
        AbstractBinClip.__init__(self, id, name)
        self.patter_producer_type = EBUBARS_CLIP

    def create_icon(self):
        self.icon = gtk.gdk.pixbuf_new_from_file(respaths.PATTERN_PRODUCER_PATH + "bars_icon.png")
        
