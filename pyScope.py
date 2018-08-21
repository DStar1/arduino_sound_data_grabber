#!/usr/bin/env python

from tkinter import *
import tkinter.messagebox as box
from threading import Thread
import serial
import serial.tools.list_ports
import pyaudio
import random
import queue
import time
import wave

# Setup the queues
plot_q = queue.Queue(maxsize=0)
audio_q = queue.Queue(maxsize=0)

class DataAq():
    def __init__(self, plot_q, audio_q, buff_size):
        self.plot_q = plot_q
        self.audio_q = audio_q
        self.buff_size = buff_size
        self.rand_bytes = [None]*self.buff_size
         
        # Check serial ports for Arduino
        self.con_err = False
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # print(p)
            if 'Arduino' in p[1] or 'Generic' in p[1]: com_port = p[0]
            else: com_port = ''
        print(com_port)
        # com_port = '/dev/cu.usbmodemFD1431'
        
        try:
            self.port = serial.Serial(com_port,230400,timeout = None)
        except:
            self.con_err = True
            box.showerror('Connection Error',"Can't find Arduino serial port")

        if not self.con_err:
            Gui.plotter.title('Data Acquisition Plotter  Arduino: ' + com_port)
        else:
            Gui.plotter.title('Data Acquisition Plotter  Arduino: Serial port not found')
            
        self.stopped = False    # Stop the data acquisition thread (at program termination)    
        self.paused = True      # Pause the thread during Run/Stop
        self.audio_stat = False # Enable audio monitor flag        
        
    def start(self):
        # Start the thread to read data from the serial port
        Thread(target=self.read_data, args=()).start()
        return self

    def read_data(self):
        # data = ''
        Recordframes = []
        # framerate = 2000
        audio = pyaudio.PyAudio()
        # Keep looping infinitely until the thread is stopped
        while self.stopped == False:
            # Get data from the serial port and add it to the buffer
            if self.paused == False:
                if self.con_err == False:
                    rec_bytes = self.port.read(self.buff_size)
                    self.plot_q.put(rec_bytes)
                    # print(rec_bytes)
                    # data = data+str(rec_bytes)[2:-1]
                    Recordframes.append(rec_bytes)
                    # framerate =+ 20000
                    # print(framerate)
                    # data = str(rec_bytes)[2:-1]
                    # print(data)
                    waveFile = wave.open('audio.wav', 'wb')
                    waveFile.setnchannels(1)#channels
                    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paUInt8))
                    waveFile.setframerate(20000)#self.sample_rate = 20000
                    waveFile.writeframes(b''.join(Recordframes))#b''.join(Recordframes))
                    waveFile.close()
                    # Store data in the audio monitor queue
                    if self.audio_stat:
                        audio_bytes = rec_bytes
                        self.audio_q.put(audio_bytes)
                        # print(audio_bytes)########################Added
                else:
                    # Generate simulated data
                    rand_bytes = []
                    for i in range(0, self.buff_size):
                        self.rand_bytes[i] = random.randint(0,255)
                    self.plot_q.put(self.rand_bytes)
                    # Wait so the thread doesn't monopolize the program 
                    time.sleep(0.1)     
            else:
                # Clear the serial port buffer when paused
                if not self.con_err:
                    self.port.flushInput()
                Recordframes = []
                # framerate = 0
                    
    def pause(self):
        # Temporarily stop action in the thread
        self.paused = True
        return self

    def stop(self):
        # Indicate that the thread should be stopped        
        self.stopped = True
        return self   
"""
    GUI Variables and initialization
"""
class GUI():
    def __init__(self, plot_q, audio_q):
        # GUI variables
        self.plotter = Tk()        
        self.plotter.minsize(640,400)
        self.plotter.resizable(0,0)
        self.plotter.title('Data Acquisition Plotter')
        self.scrn_width = 350
        self.scrn_height = 300
        self.horiz_offset = 3
        self.vert_offset = 3
        
        self.plot_q = plot_q
        self.audio_q  = audio_q

        # Trigger variables        
        self.trig_stat = False  # Flag to enable triggering
        self.trig_level = 128
        self.last_byte = 127
        self.trig = False       # Flag to indicate triggered data
        
        self.audio_stat = False
        self.sample_rate = 20000
        
        # Initialize audio
        self.pa = pyaudio.PyAudio() # Instantiate PyAudio 
        self.chunk = 2048
        format = pyaudio.paUInt8
        channels = 1

        # PyAudio callback function to play the audio data
        def audio_callback(in_data, frame_count, time_info, status):
            audio_buff = self.audio_q.get()
            # print()
            # print(audio_buff)########################Added
            # print()
            return (audio_buff, pyaudio.paContinue)
                    
        # Open playback audio data stream
        self.playStream = self.pa.open( format = format,
                                        channels = channels,
                                        rate = self.sample_rate,
                                        input = False,
                                        output = True,
                                        start = False,
                                        frames_per_buffer = self.chunk,
                                        stream_callback = audio_callback)

        # Sweep time listbox label
        self.SweepLabel = Label(self.plotter, text = 'Sweep Time')
        self.SweepLabel.grid(row=19,column=1,sticky=N+S)

        # Sweep time list box
        # Add vertical srcollbar
        scrollbar = Scrollbar(self.plotter, orient=VERTICAL)
        self.sweep_listbox = Listbox(self.plotter,
                                     yscrollcommand=scrollbar.set,
                                     height=3,width=11)
        scrollbar.config(command=self.sweep_listbox.yview)
        scrollbar.grid(row=20,column=2,sticky=NE)
        
        self.sweep_listbox.insert(0,'1mS')
        self.sweep_listbox.insert(0,'2mS')
        self.sweep_listbox.insert(0,'5mS')
        self.sweep_listbox.insert(0,'10mS')
        self.sweep_listbox.insert(0,'20mS')
        self.sweep_listbox.insert(0,'50mS')
        self.sweep_listbox.insert(0,'100mS')
        
        self.sweep_listbox.select_set(2)
        self.sweep_listbox.bind('<<ListboxSelect>>', self.onselect)
        self.sweep_listbox.grid(row=20,column=1,sticky=NW)
        # Scale the samples at the sample rate for a given sweep time
        # to the width in pixels of the screen
        self.sweep_time = 10e-3     # Initial value
        # Get the number of samples for a given sweep time
        self.samp_size = int(self.sample_rate * self.sweep_time)
        # Scale the number of samples to the screen width
        self.samp_per_pix = float((self.samp_size)/self.scrn_width)
        
        # Button to turn on triggering
        self.trigBtn = Button(self.plotter)
        self.trigBtn.configure(text='Trig On', width=8, command=self.trig_check)
        self.trigBtn.grid(row=25,column=1,sticky=NW)
        
        # Button to turn on audio monitor
        self.audioBtn = Button(self.plotter)
        self.audioBtn.configure(text='Audio On', width=8, command=self.audio_check)
        self.audioBtn.grid(row=26,column=1,sticky=NW)

        # Button to start acquisition
        self.runBtn = Button(self.plotter)
        self.runBtn.configure(text='Run', width=5, command=self.start_stop)
        self.runBtn.grid(row=35,column=1,sticky=NW)
        
        # Button to terminate the script
        self.exitBtn = Button(self.plotter)
        self.exitBtn.configure(text='Exit', width=5, command=self.exit)
        self.exitBtn.grid(row=36,column=1, sticky=NW)
        # Allow for termination from the upper right 'Close' button
        self.plotter.wm_protocol('WM_DELETE_WINDOW', self.exit)

        # Configure a TkInter canvas to display the received data
        self.scrn = Canvas(self.plotter, width=self.scrn_width, height=self.scrn_height,borderwidth=1,relief=SUNKEN,background="white")
        self.scrn.grid(padx=50,pady=20,row=0, column=0, rowspan=40)
        
        # Setup the screen grid
        # Add horizontal line
        self.scrn.create_line(self.horiz_offset,self.scrn_height/2,
                              self.scrn_width+self.horiz_offset,self.scrn_height/2,
                              width=2,fill='green')
        # Add horizontal pips
        spacing = int(self.scrn_width/10)
        for i in range(0,self.scrn_width,spacing):
            self.scrn.create_line(i, self.scrn_height/2 - 5,
                                  i, self.scrn_height/2 + 5,
                                  width=2, fill='green')
        # Add vertical line
        self.scrn.create_line(self.scrn_width/2,self.vert_offset,
                              self.scrn_width/2,self.scrn_height+self.vert_offset,
                              width=2,fill='green')
        #Add vertical pips
        spacing = int(self.scrn_height/10)
        for i in range(0,self.scrn_height,spacing):
            self.scrn.create_line(self.scrn_width/2 - 5, i,
                                  self.scrn_width/2 + 5, i,
                                  width=2, fill='green')

        # Initialize a buffer for plot points co-ords    
        self.data_pts = []  
        for i in range(self.samp_size+1):
            x_pos = int(i/self.samp_per_pix) + self.horiz_offset
            y_pos = self.scrn_height/2
            self.data_pts.append(x_pos)
            self.data_pts.append(y_pos)
            
        # Draw the initial data points line
        self.data = self.scrn.create_line(self.data_pts,fill="red")
        
        # Timebase label
        self.timebase_str = StringVar()
        self.TimebaseLabel = Label(self.plotter, textvariable=self.timebase_str )
        self.timebase_str.set('Time Base: 1mS/div')
        self.TimebaseLabel.grid(row=40,padx=150,column=0,sticky=NW)

    # Calculate the timebase, sweep time and samples per pixel
    # from the Sweep time list box
    def onselect(self, evt):        
        i = self.sweep_listbox.curselection()[0]
        sweep_str = self.sweep_listbox.get(i)
        if sweep_str == '100mS':
            self.sweep_time = 100e-3
            self.timebase_str.set('Time Base: 50mS/div')
        if sweep_str == '50mS':
            self.sweep_time = 50e-3
            self.timebase_str.set('Time Base: 5mS/div')
        if sweep_str == '20mS':
            self.sweep_time = 20e-3
            self.timebase_str.set('Time Base: 2mS/div')
        if sweep_str == '10mS':
            self.sweep_time = 10e-3
            self.timebase_str.set('Time Base: 1mS/div')
        if sweep_str == '5mS':
            self.sweep_time = 5e-3
            self.timebase_str.set('Time Base: 0.5mS/div')
        if sweep_str == '2mS':
            self.sweep_time = 2e-3
            self.timebase_str.set('Time Base: 0.2mS/div')
        if sweep_str == '1mS':
            self.sweep_time = 1e-3
            self.timebase_str.set('Time Base: 0.1mS/div')
        # Recalculate the sweep time and sample width
        self.samp_size = int(self.sample_rate * self.sweep_time)
        self.samp_per_pix = float((self.samp_size)/self.scrn_width)
        
        # Clear and re-initialize the data_pts list
        # The data_pts is a list where even numbered entries (x_pos)
        # contain the time co-ordinate of a sample scaled to the screen
        # width and the odd entries contain the amplitude of the
        # data scaled to the screen height.
        self.data_pts.clear()
        for i in range(self.samp_size+1):
            x_pos = int(i/self.samp_per_pix) + self.horiz_offset
            y_pos = self.scrn_height/2
            self.data_pts.append(x_pos)
            self.data_pts.append(y_pos)
        
    # Turn on/off triggering
    def trig_check(self):
        if self.trigBtn['text'] == 'Trig On':            
            self.trig_stat = True
            self.trigBtn['text'] = 'Trig Off'
        elif self.trigBtn['text'] == 'Trig Off':
            self.trig_stat = False
            self.trigBtn['text'] = 'Trig On'
            
    # Turn on/off audio monitor
    def audio_check(self):
        if self.audioBtn['text'] == 'Audio On':
            self.playStream.start_stream()
            # Set audio flags for GUI and data acquisition threads
            self.audio_stat = True
            data_aq.audio_stat = True
            self.audioBtn['text'] = 'Audio Off'
        elif self.audioBtn['text'] == 'Audio Off':
            self.playStream.stop_stream()
            self.audio_stat = False
            data_aq.audio_stat = False
            self.audioBtn['text'] = 'Audio On'
            
    # Run/Stop acquisition button
    def start_stop(self):
        if self.runBtn['text'] == 'Run':
            # Clear out plot and audio queues
            while not self.audio_q.empty(): temp = self.audio_q.get()
            while not self.plot_q.empty(): temp = self.plot_q.get()
            # Enable the data acquisition thread
            data_aq.paused = False
            # Clear the serial port buffer 
            if not data_aq.con_err:
                data_aq.port.flushInput()   
            if self.audio_stat:
                self.playStream.start_stream()
            self.runBtn['text'] = 'Stop'
        elif self.runBtn['text'] == 'Stop':
            if self.audio_stat:
                self.playStream.stop_stream()
                print(self.playStream)
                ################## Added ####################
                # waveFile = wave.open('audio.wav', 'wb')
                # waveFile.setnchannels(1)#channels
                # waveFile.setsampwidth(self.pa.get_sample_size(pyaudio.paUInt8))
                # waveFile.setframerate(2000)#self.sample_rate = 20000
                # waveFile.writeframes()#b''.join(Recordframes))
                # waveFile.close()
            # Suspend the data acquisition thread
            data_aq.pause()
            self.runBtn['text'] = 'Run'
            
    # Exit button
    def exit(self):
        # Stop the data acquisition thread               
        data_aq.stop()        
        while data_aq_thread.is_alive(): pass
        # Terminate the audio monitor stream
        if self.playStream.is_active():
            # Terminate the audio stream
            self.playStream.stop_stream()
            self.playStream.close()
        self.pa.terminate()
        
        # Terminate the GUI
        self.plotter.destroy()                                        
    
    def updateGUI(self):
        if self.runBtn['text'] == 'Stop':            
            # Plot data points
            while not self.plot_q.empty():
                # Get a block of data from the plot queue
                rec_data = self.plot_q.get()
                index = 0
                while len(rec_data) - index >= self.samp_size:
                    # Wait for data to be triggered if necessary
                    # If the trigger flag is False, assume all bytes are triggered
                    if self.trig_stat == False: self.trig = True
                    # Condition for triggering is that the value equals the
                    # threshold and is greater than the last byte (positive slope)
                    if self.trig == False:
                        if (rec_data[index] == self.trig_level) and (rec_data[index] > self.last_byte):
                            self.last_byte = rec_data[index]
                            self.trig = True
                        else:
                            self.last_byte = rec_data[index]
                            index += 1                    
                    if self.trig == True:
                        # If there's enough data in the rec_data buffer for
                        # a sweep, then process it.
                        if len(rec_data) - index > self.samp_size:
                            y = 1   # y coordinate values
                            for count in range(0, self.samp_size + 1):                        
                                plot_data = self.scrn_height/2 + 127 - rec_data[index]
                                # Add plot data to data_pts buffer
                                # Note that the x coordinate values have already been calculated either
                                # on initialization or when the sweep time changed
                                self.data_pts[y] = int(plot_data)
                                self.last_byte = rec_data[index]
                                index += 1
                                y += 2
                            self.trig = False
                            # Update the plot trace
                            # Note use '*' operator to unpack self.data_pts list
                            self.scrn.coords(self.data,*self.data_pts)
                            self.scrn.itemconfig(self.data,fill='red')
                        # Otherwise wait for another buffer (the remaining data bytes
                        # in this one will be discarded)
                        else: self.trig = False
                                        
        self.plotter.after(1,self.updateGUI)

if  __name__ == '__main__': 
    Gui = GUI(plot_q, audio_q) # Instantiate the GUI
    # Instantiate the DataAq class and thread 
    data_aq = DataAq(plot_q, audio_q, Gui.chunk)
    data_aq_thread = Thread(target=data_aq.read_data, args=())    
    data_aq.start()         # Start the data acquisition thread    
    Gui.updateGUI()         # Start the GUI
    Gui.plotter.mainloop()                                               
