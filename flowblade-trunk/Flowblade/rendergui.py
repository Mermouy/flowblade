import gtk
import os

import dialogutils
import gui
import guiutils
from editorstate import current_sequence
import mltprofiles
import renderconsumer
import respaths

FFMPEG_VIEW_SIZE = (200, 210) # Text edit area height for render opts. Width 200 seems to be ignored in current layout?

# ------------------------------------------------------------ panels
def get_render_panel_left(render_widgets, add_audio_panel, normal_height):
    file_opts_panel = guiutils.get_named_frame(_("File"), render_widgets.file_panel.vbox, 4)
    render_type_panel = guiutils.get_named_frame(_("Render Type"), render_widgets.render_type_panel.vbox, 4)
    profile_panel = guiutils.get_named_frame(_("Render Profile"), render_widgets.profile_panel.vbox, 4)
    encoding_panel = guiutils.get_named_frame(_("Encoding Format"), render_widgets.encoding_panel.vbox, 4)

    render_panel = gtk.VBox()
    render_panel.pack_start(file_opts_panel, False, False, 0)
    render_panel.pack_start(render_type_panel, False, False, 0)
    render_panel.pack_start(profile_panel, False, False, 0)
    render_panel.pack_start(encoding_panel, False, False, 0)
    render_panel.pack_start(gtk.Label(), True, True, 0)
    return render_panel

def get_render_panel_right(render_widgets, render_clicked_cb, to_queue_clicked_cb):
    opts_panel = guiutils.get_named_frame(_("Render Args"), render_widgets.args_panel.vbox, 4)
    
    bin_row = gtk.HBox()
    bin_row.pack_start(guiutils.get_pad_label(10, 8),  False, False, 0)
    bin_row.pack_start(gtk.Label(_("Open File in Bin:")),  False, False, 0)
    bin_row.pack_start(guiutils.get_pad_label(10, 2),  False, False, 0)
    bin_row.pack_start(render_widgets.open_in_bin,  False, False, 0)
    bin_row.pack_start(gtk.Label(), True, True, 0)

    range_row = gtk.HBox()
    range_row.pack_start(guiutils.get_pad_label(10, 8),  False, False, 0)
    range_row.pack_start(gtk.Label(_("Render Range:")),  False, False, 0)
    range_row.pack_start(guiutils.get_pad_label(10, 2),  False, False, 0)
    range_row.pack_start(render_widgets.range_cb,  True, True, 0)

    buttons_panel = gtk.HBox()
    buttons_panel.pack_start(guiutils.get_pad_label(10, 8), False, False, 0)
    buttons_panel.pack_start(render_widgets.reset_button, False, False, 0)
    buttons_panel.pack_start(gtk.Label(), True, True, 0)
    buttons_panel.pack_start(render_widgets.queue_button, False, False, 0)
    buttons_panel.pack_start(gtk.Label(), True, True, 0)
    buttons_panel.pack_start(render_widgets.render_button, False, False, 0)

    render_widgets.queue_button.connect("clicked", 
                                         to_queue_clicked_cb, 
                                         None)

    render_widgets.render_button.connect("clicked", 
                                         render_clicked_cb, 
                                         None)

    render_panel = gtk.VBox()
    render_panel.pack_start(opts_panel, True, True, 0)
    render_panel.pack_start(guiutils.get_pad_label(10, 22), False, False, 0)
    render_panel.pack_start(bin_row, False, False, 0)
    render_panel.pack_start(range_row, False, False, 0)
    render_panel.pack_start(guiutils.get_pad_label(10, 12), False, False, 0)
    render_panel.pack_start(buttons_panel, False, False, 0)

    return render_panel

# ----------------------------------------------------------- dialogs
def render_progress_dialog(callback, parent_window):
    dialog = gtk.Dialog(_("Render Progress"),
                         parent_window,
                         gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                         (_("Cancel").encode('utf-8'), gtk.RESPONSE_REJECT))

    dialog.status_label = gtk.Label()
    dialog.remaining_time_label = gtk.Label()
    dialog.passed_time_label = gtk.Label()
    dialog.progress_bar = gtk.ProgressBar()

    status_box = gtk.HBox(False, 2)
    status_box.pack_start(dialog.status_label,False, False, 0)
    status_box.pack_start(gtk.Label(), True, True, 0)
    
    remaining_box = gtk.HBox(False, 2)
    remaining_box.pack_start(dialog.remaining_time_label,False, False, 0)
    remaining_box.pack_start(gtk.Label(), True, True, 0)

    passed_box = gtk.HBox(False, 2)
    passed_box.pack_start(dialog.passed_time_label,False, False, 0)
    passed_box.pack_start(gtk.Label(), True, True, 0)

    progress_vbox = gtk.VBox(False, 2)
    progress_vbox.pack_start(status_box, False, False, 0)
    progress_vbox.pack_start(remaining_box, False, False, 0)
    progress_vbox.pack_start(passed_box, False, False, 0)
    progress_vbox.pack_start(guiutils.get_pad_label(10, 10), False, False, 0)
    progress_vbox.pack_start(dialog.progress_bar, False, False, 0)
    
    alignment = gtk.Alignment(0.5, 0.5, 1.0, 1.0)
    alignment.set_padding(12, 12, 12, 12)
    alignment.add(progress_vbox)

    dialog.vbox.pack_start(alignment, True, True, 0)
    dialog.set_default_size(500, 125)
    alignment.show_all()
    dialog.set_has_separator(False)
    dialog.connect('response', callback)
    dialog.show()
    return dialog

def no_good_rander_range_info():
    primary_txt = _("Render range not defined!")
    secondary_txt = _("Define render range using Mark In and Mark Out points\nor select range option 'Sequence length' to start rendering.")
    dialogutils.warning_message(primary_txt, secondary_txt, gui.editor_window.window)

def load_ffmpeg_opts_dialog(callback, opts_extension):
    dialog = gtk.FileChooserDialog(_("Load Render Args File"), None, 
                                   gtk.FILE_CHOOSER_ACTION_OPEN, 
                                   (_("Cancel").encode('utf-8'), gtk.RESPONSE_REJECT,
                                    _("OK").encode('utf-8'), gtk.RESPONSE_ACCEPT), None)
    dialog.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
    dialog.set_select_multiple(False)
    file_filter = gtk.FileFilter()
    file_filter.set_name(opts_extension + " files")
    file_filter.add_pattern("*" + opts_extension)
    dialog.add_filter(file_filter)
    dialog.connect('response', callback)
    dialog.show()

def save_ffmpeg_opts_dialog(callback, opts_extension):
    dialog = gtk.FileChooserDialog(_("Save Render Args As"), None, 
                                   gtk.FILE_CHOOSER_ACTION_SAVE, 
                                   (_("Cancel").encode('utf-8'), gtk.RESPONSE_REJECT,
                                   _("Save").encode('utf-8'), gtk.RESPONSE_ACCEPT), None)
    dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
    dialog.set_current_name("untitled" + opts_extension)
    dialog.set_do_overwrite_confirmation(True)
    dialog.set_select_multiple(False)
    file_filter = gtk.FileFilter()
    file_filter.set_name(opts_extension + " files")
    file_filter.add_pattern("*" + opts_extension)
    dialog.add_filter(file_filter)
    dialog.connect('response', callback)
    dialog.show()

def clip_render_progress_dialog(callback, title, text, progress_bar, parent_window):
    dialog = gtk.Dialog(title,
                         parent_window,
                         gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                         (_("Cancel").encode('utf-8'), gtk.RESPONSE_REJECT))
    
    dialog.text_label = gtk.Label(text)
    
    status_box = gtk.HBox(False, 2)
    status_box.pack_start(dialog.text_label, False, False, 0)
    status_box.pack_start(gtk.Label(), True, True, 0)
    
    progress_vbox = gtk.VBox(False, 2)
    progress_vbox.pack_start(status_box, False, False, 0)
    progress_vbox.pack_start(guiutils.get_pad_label(10, 10), False, False, 0)
    progress_vbox.pack_start(progress_bar, False, False, 0)
    
    alignment = gtk.Alignment(0.5, 0.5, 1.0, 1.0)
    alignment.set_padding(12, 12, 12, 12)
    alignment.add(progress_vbox)
    
    dialog.vbox.pack_start(alignment, True, True, 0)
    dialog.set_default_size(500, 125)
    alignment.show_all()
    dialog.set_has_separator(False)
    dialog.connect('response', callback)
    dialog.show()
    return dialog

# ----------------------------------------------------------- widgets
class RenderQualitySelector():
    """
    Component displays quality option relevant for encoding slection.
    """
    def __init__(self):
        self.widget = gtk.combo_box_new_text()
        self.widget.set_tooltip_text(_("Select Render quality"))

    def update_quality_selection(self, enc_index):
        encoding = renderconsumer.encoding_options[enc_index]
        
        self.widget.get_model().clear()
        for quality_option in encoding.quality_options:
            self.widget.append_text(quality_option.name)

        if encoding.quality_default_index != None:
            self.widget.set_active(encoding.quality_default_index)
        else:
            self.widget.set_active(0)


class RenderEncodingSelector():

    def __init__(self, quality_selector, extension_label, audio_desc_label):
        self.widget = gtk.combo_box_new_text()
        for encoding in renderconsumer.encoding_options:
            self.widget.append_text(encoding.name)
            
        self.widget.set_active(0)
        self.widget.connect("changed", 
                            lambda w,e: self.encoding_selection_changed(), 
                            None)
        self.widget.set_tooltip_text(_("Select Render encoding"))
    
        self.quality_selector = quality_selector
        self.extension_label = extension_label
        self.audio_desc_label = audio_desc_label
        
    def encoding_selection_changed(self):
        enc_index = self.widget.get_active()
        
        self.quality_selector.update_quality_selection(enc_index)
        
        encoding = renderconsumer.encoding_options[enc_index]
        self.extension_label.set_text("." + encoding.extension)

        if self.audio_desc_label != None:
            self.audio_desc_label.set_markup(encoding.get_audio_description())


class PresetEncodingsSelector():
    
     def __init__(self, selection_changed_callback):
        self.widget = gtk.combo_box_new_text()
        for encoding in renderconsumer.non_user_encodings:
            self.widget.append_text(encoding.name)
        
        self.widget.set_active(0)
        self.widget.set_sensitive(False)
        self.widget.connect("changed", 
                             lambda w,e: selection_changed_callback(), 
                             None)

class ProfileSelector():
    def __init__(self, out_profile_changed_callback=None):
        self.widget = gtk.combo_box_new_text() # filled later when current sequence known
        if out_profile_changed_callback != None:
            self.widget.connect('changed', lambda w:  out_profile_changed_callback())
        self.widget.set_sensitive(False)
        self.widget.set_tooltip_text(_("Select render profile"))
        
    def fill_options(self):
        self.widget.get_model().clear()
        self.widget.append_text(current_sequence().profile.description())
        profiles = mltprofiles.get_profiles()
        for profile in profiles:
            self.widget.append_text(profile[0])
        self.widget.set_active(0)


class ProfileInfoBox(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False, 2)
        self.add(gtk.Label()) # This is removed when we have data to fill this
        
    def display_info(self, info_panel):
        info_box_children = self.get_children()
        for child in info_box_children:
            self.remove(child)
    
        self.add(info_panel)
        self.show_all()

    
# --------------------------------------------------------------- panel
class RenderFilePanel():

    def __init__(self):

        self.out_folder = gtk.FileChooserButton(_("Select Folder"))
        self.out_folder.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.out_folder.set_current_folder(os.path.expanduser("~") + "/")

        out_folder_row = guiutils.get_two_column_box(gtk.Label(_("Folder:")), self.out_folder, 60)
                              
        self.movie_name = gtk.Entry()
        self.movie_name.set_text("movie")
        self.extension_label = gtk.Label()
            
        name_box = gtk.HBox(False, 8)
        name_box.pack_start(self.movie_name, True, True, 0)
        name_box.pack_start(self.extension_label, False, False, 0)
          
        movie_name_row = guiutils.get_two_column_box(gtk.Label(_("Name:")), name_box, 60)

        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(out_folder_row, False, False, 0)
        self.vbox.pack_start(movie_name_row, False, False, 0)

        self.out_folder.set_tooltip_text(_("Select folder to place rendered file in"))
        self.movie_name.set_tooltip_text(_("Give name for rendered file"))


class RenderTypePanel():
    
    def __init__(self, render_type_changed_callback, preset_selection_changed_callback):
        self.type_label = gtk.Label(_("Type:"))
        self.presets_label = gtk.Label(_("Presets:")) 
        
        self.type_combo = gtk.combo_box_new_text() # filled later when current sequence known
        self.type_combo.append_text(_("User Defined"))
        self.type_combo.append_text(_("Preset File type"))
        self.type_combo.set_active(0)
        self.type_combo.connect('changed', lambda w: render_type_changed_callback())
    
        self.presets_selector = PresetEncodingsSelector(preset_selection_changed_callback)

        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(guiutils.get_two_column_box(self.type_label,
                                                         self.type_combo, 80), 
                                                         False, False, 0)
        self.vbox.pack_start(guiutils.get_two_column_box(self.presets_label,
                                                         self.presets_selector.widget, 80), 
                                                         False, False, 0)

class RenderProfilePanel():

    def __init__(self, out_profile_changed_callback):
        self.use_project_label = gtk.Label(_("Use Project Profile:"))
        self.use_args_label = gtk.Label(_("Render using args:"))

        self.use_project_profile_check = gtk.CheckButton()
        self.use_project_profile_check.set_active(True)
        self.use_project_profile_check.connect("toggled", self.use_project_check_toggled)

        self.out_profile_combo = ProfileSelector(out_profile_changed_callback)
        
        self.out_profile_info_box = ProfileInfoBox() # filled later when current sequence known
        
        use_project_profile_row = gtk.HBox()
        use_project_profile_row.pack_start(self.use_project_label,  False, False, 0)
        use_project_profile_row.pack_start(self.use_project_profile_check,  False, False, 0)
        use_project_profile_row.pack_start(gtk.Label(), True, True, 0)

        self.use_project_profile_check.set_tooltip_text(_("Select used project profile for rendering"))
        self.out_profile_info_box.set_tooltip_text(_("Render profile info"))
    
        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(use_project_profile_row, False, False, 0)
        self.vbox.pack_start(self.out_profile_combo.widget, False, False, 0)
        self.vbox.pack_start(self.out_profile_info_box, False, False, 0)

    def set_sensitive(self, value):
        self.use_project_profile_check.set_sensitive(value)
        self.use_project_label.set_sensitive(value)
        self.out_profile_combo.widget.set_sensitive(value)
        
    def use_project_check_toggled(self, checkbutton):
        self.out_profile_combo.widget.set_sensitive(checkbutton.get_active() == False)
        if checkbutton.get_active() == True:
            self.out_profile_combo.widget.set_active(0)
        

class RenderEncodingPanel():
    
    def __init__(self, extension_label):
        self.quality_selector = RenderQualitySelector()
        self.quality_selector.widget.set_size_request(110, 34)
        self.quality_selector.update_quality_selection(0)
        self.audio_desc = gtk.Label()
        self.encoding_selector = RenderEncodingSelector(self.quality_selector,
                                                        extension_label,
                                                        self.audio_desc)
        self.encoding_selector.encoding_selection_changed()
        
        speaker_image = gtk.image_new_from_file(respaths.IMAGE_PATH + "audio_desc_icon.png")

        quality_row  = gtk.HBox()
        quality_row.pack_start(self.quality_selector.widget, False, False, 0)
        quality_row.pack_start(gtk.Label(), True, False, 0)
        quality_row.pack_start(speaker_image, False, False, 0)
        quality_row.pack_start(self.audio_desc, False, False, 0)
        quality_row.pack_start(gtk.Label(), True, False, 0)
        
        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(self.encoding_selector.widget, False, False, 0)
        self.vbox.pack_start(quality_row, False, False, 0)

    def set_sensitive(self, value):
        self.quality_selector.widget.set_sensitive(value)
        self.audio_desc.set_sensitive(value)
        self.encoding_selector.widget.set_sensitive(value)


class RenderArgsPanel():

    def __init__(self, normal_height, save_args_callback, 
                 load_args_callback, display_selection_callback):
        self.display_selection_callback = display_selection_callback
        
        self.use_project_label = gtk.Label(_("Use Project Profile:"))
        self.use_args_label = gtk.Label(_("Render using args:"))
    
        self.use_args_check = gtk.CheckButton()
        self.use_args_check.connect("toggled", self.use_args_toggled)

        self.opts_save_button = gtk.Button()
        icon = gtk.image_new_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_MENU)
        self.opts_save_button.set_image(icon)
        self.opts_save_button.connect("clicked", lambda w: save_args_callback())
        self.opts_save_button.set_sensitive(False)
    
        self.opts_load_button = gtk.Button()
        icon = gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
        self.opts_load_button.set_image(icon)
        self.opts_load_button.connect("clicked", lambda w: load_args_callback())
                
        self.load_selection_button = gtk.Button(_("Load Selection"))
        self.load_selection_button.set_sensitive(False)
        self.load_selection_button.connect("clicked", lambda w: self.display_selection_callback())
        self.opts_load_button.set_sensitive(False)

        self.ext_label = gtk.Label(_("Ext.:"))
        self.ext_label.set_sensitive(False)

        self.ext_entry = gtk.Entry()
        self.ext_entry.set_width_chars(5)    
        self.ext_entry.set_sensitive(False)

        self.opts_view = gtk.TextView()
        self.opts_view.set_sensitive(False)
        self.opts_view.set_pixels_above_lines(2)
        self.opts_view.set_left_margin(2)

        self.open_in_bin = gtk.CheckButton()

        use_opts_row = gtk.HBox()
        use_opts_row.pack_start(self.use_args_label,  False, False, 0)
        use_opts_row.pack_start(self.use_args_check,  False, False, 0)
        use_opts_row.pack_start(gtk.Label(), True, True, 0)
        use_opts_row.pack_start(self.opts_load_button,  False, False, 0)
        use_opts_row.pack_start(self.opts_save_button,  False, False, 0)

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.opts_view)
        if normal_height:
            sw.set_size_request(*FFMPEG_VIEW_SIZE)
        else:
            w, h = FFMPEG_VIEW_SIZE
            h = h - 30
            sw.set_size_request(w, h)

        scroll_frame = gtk.Frame()
        scroll_frame.add(sw)

        opts_buttons_row = gtk.HBox(False)
        opts_buttons_row.pack_start(self.load_selection_button, False, False, 0)
        opts_buttons_row.pack_start(gtk.Label(), True, True, 0)
        opts_buttons_row.pack_start(self.ext_label, False, False, 0)
        opts_buttons_row.pack_start(self.ext_entry, False, False, 0)

        self.use_args_check.set_tooltip_text(_("Render using key=value rendering options"))
        self.load_selection_button.set_tooltip_text(_("Load render options from currently selected encoding"))
        self.opts_view.set_tooltip_text(_("Edit render options"))
        self.opts_save_button.set_tooltip_text(_("Save Render Args into a text file"))
        self.opts_load_button.set_tooltip_text(_("Load Render Args from a text file"))
    
        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(use_opts_row , False, False, 0)
        self.vbox.pack_start(scroll_frame, True, True, 0)
        self.vbox.pack_start(opts_buttons_row, False, False, 0)

    def set_sensitive(self, value):
        self.use_args_check.set_sensitive(value)
        self.use_args_label.set_sensitive(value)
    
    def display_encoding_args(self, profile, enc_index, qual_index):
        encoding_option = renderconsumer.encoding_options[enc_index]
        quality_option = encoding_option.quality_options[qual_index]
        args_vals_list = encoding_option.get_args_vals_tuples_list(profile, quality_option)
        text = ""
        for arg_val in args_vals_list:
            k, v = arg_val
            line = str(k) + "=" + str(v) + "\n"
            text = text + line

        text_buffer = gtk.TextBuffer()
        text_buffer.set_text(text)
        self.opts_view.set_buffer(text_buffer)

        self.ext_entry.set_text(encoding_option.extension)

    def use_args_toggled(self, checkbutton):
        active = checkbutton.get_active()
        self.opts_view.set_sensitive(active)
        self.load_selection_button.set_sensitive(active)
        self.opts_save_button.set_sensitive(active)
        self.opts_load_button.set_sensitive(active)

        self.ext_label.set_sensitive(active)
        self.ext_entry.set_sensitive(active)
        
        if active == True:
            self.display_selection_callback()
        else:
            self.opts_view.set_buffer(gtk.TextBuffer())
            self.ext_entry.set_text("")
