import gi
import sys
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

class VideoPlayer(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Animaster")
        
        self.playbin = Gst.ElementFactory.make("playbin", "playbin")
        if not self.playbin:
            print("ERROR: Could not create playbin.")
            sys.exit(1)
            
        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)
        
        # Add playbin to the pipeline
        self.pipeline.add(self.playbin)
        
        self.build_ui()
        
    def build_ui(self):
        self.playButton = Gtk.Button(label="Play")
        self.playButton.connect("clicked", self.on_playButton_clicked)
            
        self.pauseButton = Gtk.Button(label="Pause")
        self.pauseButton.connect("clicked", self.on_pauseButton_clicked)
        
        self.stopButton = Gtk.Button(label="Stop")
        self.stopButton.connect("clicked", self.on_stopButton_clicked)
        
        self.main_box = Gtk.Box()
        self.add(self.main_box)
        self.main_box.pack_start(self.playButton, True, True, 0)
        self.main_box.pack_start(self.pauseButton, True, True, 0)
        self.main_box.pack_start(self.stopButton, True, True, 0)

    def set_url(self, url):
        self.playbin.set_property("uri", url)
        
    def on_playButton_clicked(self, widget):
        print("Play")
        
    def on_pauseButton_clicked(self, widget):
        print("Pause")
        
    def on_stopButton_clicked(self, widget):
        print("Stop")
        
    # this function is called when an error message is posted on the bus
    def on_error(self, bus, msg):
        err, dbg = msg.parse_error()
        print("ERROR:", msg.src.get_name(), ":", err.message)
        if dbg:
            print("Debug info:", dbg)

    # this function is called when an End-Of-Stream message is posted on the bus
    # we just set the pipeline to READY (which stops playback)
    def on_eos(self, bus, msg):
        print("End-Of-Stream reached")
        self.playbin.set_state(Gst.State.READY)

        
player = VideoPlayer()
player.connect("delete_event", Gtk.main_quit)
player.show_all()
Gtk.main()

#"https://chitoge.sovetromantica.com/anime/305_sin-nanatsu-no-taizai/episodes/dubbed/episode_7.mp4"