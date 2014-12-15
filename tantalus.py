#!/usr/bin/python

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#	https://github.com/AGenews/tantalus




from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog, time  
import ConfigParser
global version_info
version_info="v0.5 'Recondite Reindeer'"

config = ConfigParser.RawConfigParser()
global sessionlength, sampleinterval, timebin, locale_var
global freezingon
global diggingon
global anythingon
global startbutton
global resetbutton


if config.read('tantalus_config.cfg'):
	sessionlength = config.getint('Settings', 'sessionlength')
	sampleinterval = config.getint('Settings', 'sampleinterval')
	timebin = config.getint('Settings', 'timebin')
	locale_var = config.get('Settings', 'locale_var')
	freezingon = config.getint('Settings', 'freezingon')
	diggingon = config.getint('Settings', 'diggingon')
	anythingon = config.getint('Settings', 'anythingon')
	
else:
	#print "Using Default Values"  
	sessionlength=180
	sampleinterval=10  
	timebin=20
	locale_var="Point"
	freezingon=1
	diggingon=0
	anythingon=0
	
class logger(Tkinter.Frame):
	
	#TIMING VARS
	global sessionlength
	global sampleinterval
	global number_of_samples
	number_of_samples=(sessionlength*1000)/sampleinterval
	global samplecount
	samplecount=0
	global timebin
	
	#EVENT VARS
	global freeze_var
	freeze_var=0
	global old_freeze_var
	old_freeze_var=0
	global dig_var
	dig_var=0
	global old_dig_var
	old_dig_var=0
	global any_var
	any_var=0
	global old_any_var
	old_any_var=0
	global freeze_latency_toggle
	freeze_latency_toggle=0
	global dig_latency_toggle
	dig_latency_toggle=0
	global any_latency_toggle
	any_latency_toggle=0
	
	#DATA VARS
	global timestamps
	timestamps = [] 
	global cumulative_freeze_data
	cumulative_freeze_data=0
	global cumulative_dig_data
	cumulative_dig_data=0
	global cumulative_any_data
	cumulative_any_data=0
	global counter
	counter=0
	global percentage_freeze
	percentage_freeze = []
	global percentage_dig
	percentage_dig = []
	global percentage_any
	percentage_any = []
	global percentage_time
	percentage_time = []
	global freeze_latency
	freeze_latency=float(sessionlength)
	global dig_latency
	dig_latency=float(sessionlength)
	global any_latency
	any_latency=float(sessionlength)

	
	#CONFIG VARS

	global startbutton
	global resetbutton
	global locale_var, freezingon, diggingon, anythingon
	global var1, var2, var3
	var1 = 1
	var2 = 1
	var3 = 1
	
	def __init__(self, parent,*args, **kwargs):        #some definitions
		Tkinter.Frame.__init__(self, parent, kwargs)
		self.parent = parent
		global defaultbg
		defaultbg = parent.cget('bg')
		self._start = 0.0        
		self._elapsedtime = 0.0
		self._running = 0
		self._time = 0 
		self.timestr = StringVar()               
		self.makeWidgets()
		self.file_opt = options = {}
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialfile'] = 'myfile.txt'
		
		global butts, sessleng, sampinter, timbi, separator
		butts="To score FREEZING press <f>"
		digg="To score DIGGING press <d>"
		anythingelse="To score ANYTHINGELSE press <a>"
		sessleng = "Session length is set to "
		sampinter = "Sample interval is set to "
		timbi = "Time bin is set to "
		separator = "Decimal separator is set to "
		self.msg = Message(parent, text = sessleng + str(sessionlength) + " s", width=300 )
		self.msg2 = Message(parent, text = sampinter + str(sampleinterval) + " ms", width=300 )
		self.msg3 = Message(parent, text = timbi + str(timebin) + " s", width=300 )
		self.msg4 = Message(parent, text = butts, width=300 )
		self.msg5 = Message(parent, text = digg, width=300 )
		self.msg6 = Message(parent, text = anythingelse, width=300 )
		self.msg7 = Message(parent, text = separator + locale_var, width=300 )
		self.msg4.config(font=('arial', 10, 'bold'))
		self.msg4.pack( )
		self.msg5.config(font=('arial', 10, 'bold'))
		self.msg5.pack( )
		self.msg6.config(font=('arial', 10, 'bold'))
		self.msg6.pack( )
		self.msg.config(font=('arial', 10, 'normal'))
		self.msg.pack( )
		self.msg2.config(font=('arial', 10, 'normal'))
		self.msg2.pack( )
		self.msg3.config(font=('arial', 10, 'normal'))
		self.msg3.pack( )
		self.msg7.config(font=('arial', 10, 'normal'))
		self.msg7.pack( )
		self.frame2 = Frame(parent, width=100, height=50)
		global b
		b = Button(self.frame2, text="EVENT DETECTED", font=('arial', 10, 'bold'))
		b.config(state=DISABLED,relief=RAISED,activebackground="white",activeforeground="black",disabledforeground="black",bg="white",foreground="black")
		b.pack()
		self.frame2.pack()
		
		
		global var1, var2, var3
		var1 = IntVar()
		var2 = IntVar()
		var3 = IntVar()
		c1=Checkbutton(self.frame2, text="Freezing", variable=var1).pack(side=LEFT)
		c2=Checkbutton(self.frame2, text="Digging", variable=var2).pack(side=LEFT)
		c3=Checkbutton(self.frame2, text="Anything", variable=var3).pack(side=LEFT)
		
		if freezingon==1:
			var1.set(1)
		elif freezingon==0:
			var1.set(0)
		if diggingon==1:
			var2.set(1)
		elif diggingon==0:
			var2.set(0)
		if anythingon==1:
			var3.set(1)
		elif anythingon==0:
			var3.set(0)
	
			
	def makeWidgets(self):                        
		""" Make the time label. """
		l = Label(self, textvariable=self.timestr)
		self._setTime(self._elapsedtime)
		l.pack(fill=X, expand=NO, pady=2, padx=2)    
	
			
	def _update(self): #most of the work is done here
		
		import tkMessageBox
		""" Update the label with elapsed time. """
		global freeze_var
		global old_freeze_var
		global dig_var
		global old_dig_var
		global any_var
		global old_any_var
		global timestamps
		global data
		global cumulative_freeze_data
		global cumulative_dig_data
		global cumulative_any_data
		global timebin
		global percentage_freeze
		global percentage_dig
		global percentage_any
		global percentage_time
		global samples_per_bin
		global counter
		global sessionlength
		global number_of_samples
		global samplecount
		global freeze_latency_toggle
		global dig_latency_toggle
		global any_latency_toggle
		global freeze_latency
		global dig_latency
		global any_latency
		global locale_var
		global resetbutton
				
		sessionlength=int(sessionlength)
		samplecount=float(samplecount)
		
		if self._elapsedtime<sessionlength:
			self._elapsedtime = time.time() - self._start
			self._setTime(self._elapsedtime)
			self._timer = self.after(sampleinterval, self._update)
			samplecount += 1
			step=round( (float(sampleinterval)/1000),3)	
			timestep=round( (round((round(self._elapsedtime,3)/step),0)*step),3)
			
			samples_per_bin=float(timebin/step)
			timestamps.append(timestep)
			freeze_var=int(freeze_var)
						
			
			if (old_freeze_var==1) and (freeze_var==1):
				cumulative_freeze_data=cumulative_freeze_data+1

			elif (old_freeze_var==0) and (freeze_var==0):
				cumulative_freeze_data=cumulative_freeze_data+0
			else: 
				cumulative_freeze_data=cumulative_freeze_data+old_freeze_var
			
			if (old_dig_var==1) and (dig_var==1):
				cumulative_dig_data=cumulative_dig_data+1
			elif (old_dig_var==0) and (dig_var==0):
				cumulative_dig_data=cumulative_dig_data+0
			else: 
				cumulative_dig_data=cumulative_dig_data+old_dig_var
			
			if (old_any_var==1) and (any_var==1):
				cumulative_any_data=cumulative_any_data+1
			elif (old_any_var==0) and (any_var==0):
				cumulative_any_data=cumulative_any_data+0
			else: 
				cumulative_any_data=cumulative_any_data+old_any_var
			
			
			if (cumulative_freeze_data==0 and sum(percentage_freeze)==0 and old_freeze_var==0 and freeze_var==1 and freeze_latency_toggle==0):
				freeze_latency=timestep
				freeze_latency_toggle=1
			if (cumulative_dig_data==0 and sum(percentage_dig)==0 and old_dig_var==0 and dig_var==1 and dig_latency_toggle==0):
				dig_latency=timestep
				dig_latency_toggle=1
			if (cumulative_any_data==0 and sum(percentage_any)==0 and old_any_var==0 and any_var==1 and any_latency_toggle==0):
				any_latency=timestep
				any_latency_toggle=1
			
			################
			##DEBUGGING LINE
			################
				
			##print str(timestep)+"\t"+str(samplecount)+"\t"+str(cumulative_any_data)+"\t"+str(cumulative_dig_data)+"\t"+str(cumulative_freeze_data)+"\t"+str(any_var)+"\t"+str(dig_var)+"\t"+str(freeze_var)
			
			################
			
			old_freeze_var=freeze_var
			old_dig_var=dig_var
			old_any_var=any_var
			
						
			if timestep>=timebin+counter*timebin:	
				freeze_data=round( (cumulative_freeze_data/samplecount)*100 ,2)
				dig_data=round( (cumulative_dig_data/samplecount)*100 ,2)
				any_data=round( (cumulative_any_data/samplecount)*100 ,2)
				time_data=(timebin+counter*timebin)
				percentage_freeze.append(freeze_data)
				percentage_dig.append(dig_data)
				percentage_any.append(any_data)
				percentage_time.append(time_data)
				cumulative_freeze_data=0
				cumulative_dig_data=0
				cumulative_any_data=0
				counter += 1
				samplecount=0
				
		else:
			logger.Stop(self)
			tkMessageBox.showinfo("", "\nFinish!", parent = self)
			self._start = time.time()         
			self._elapsedtime = 0.0    
			self._setTime(self._elapsedtime)
		
		if (sum(percentage_dig)+sum(percentage_freeze)+cumulative_any_data+cumulative_dig_data+cumulative_freeze_data)!=0:
			resetbutton.configure(activebackground="yellow", bg='yellow')
			
					
			
	def Start(self): #We start the whole thing and display some errors
		import tkMessageBox
		global sessionlength,sampleinterval,startbutton,timebin
		startbutton.configure(activebackground="red", bg='red')
		sessionlength=int(sessionlength)
		timebin=int(timebin)
		sampleinterval=int(sampleinterval)
		self.msg.config(text = sessleng + str(sessionlength) + " s", width=300)
		self.msg2.config(text = sampinter + str(sampleinterval) + " ms", width=300)
		self.msg3.config(text = timbi + str(timebin) + " s", width=300)
		self.msg7.config(text = separator + locale_var, width=300)
	
		if timebin>sessionlength:
			tkMessageBox.showerror("Horrible Error", "\nSession length is \nshorter than Time Bin!", parent = self)
			logger.Stop(self)
			logger.Reset(self)
			startbutton.configure(activebackground=defaultbg, bg=defaultbg)
			return 0
                                                  
		""" Start the stopwatch, ignore if running. """
		if not self._running:            
			self._start = time.time() - self._elapsedtime
			self._update()
			self._running = 1 
	
	def Stop(self):        #Self explaining stop event                            
		""" Stop the stopwatch, ignore if stopped. """
		if self._running:
			self.after_cancel(self._timer)            
			self._elapsedtime = time.time() - self._start    
			self._setTime(self._elapsedtime)
			self._running = 0
			b.config(state=DISABLED,relief=RAISED,activebackground="white",activeforeground="black" \
			,disabledforeground="black",bg="white",foreground="black")
			startbutton.configure(activebackground=defaultbg, bg=defaultbg)
			
    
	def Reset(self):    #A Reset is done, hopefully the data is also resetted?   
		#TIMING VARS
		global sessionlength
		global sampleinterval
		global number_of_samples
		number_of_samples=(sessionlength*1000)/sampleinterval
		global samplecount
		samplecount=0
		global timebin
		
		#EVENT VARS
		global freeze_var
		freeze_var=0
		global old_freeze_var
		old_freeze_var=0
		global dig_var
		dig_var=0
		global old_dig_var
		old_dig_var=0
		global any_var
		any_var=0
		global old_any_var
		old_any_var=0
		global freeze_latency_toggle
		freeze_latency_toggle=0
		global dig_latency_toggle
		dig_latency_toggle=0
		global any_latency_toggle
		any_latency_toggle=0
		
		#DATA VARS
		global timestamps
		timestamps = [] 
		global cumulative_freeze_data
		cumulative_freeze_data=0
		global cumulative_dig_data
		cumulative_dig_data=0
		global cumulative_any_data
		cumulative_any_data=0
		global counter
		counter=0
		global percentage_freeze
		percentage_freeze = []
		global percentage_dig
		percentage_dig = []
		global percentage_any
		percentage_any = []
		global percentage_time
		percentage_time = []
		global freeze_latency
		freeze_latency=float(sessionlength)
		global dig_latency
		dig_latency=float(sessionlength)
		global any_latency
		any_latency=float(sessionlength)
		global percentage_time_str
		percentage_time_str=[]
		global percentage_freeze_str
		percentage_freeze_str=[]
		global percentage_dig_str
		percentage_dig_str=[]
		global percentage_any_str, dig_latency_str, freeze_latency_str, any_latency_str
		percentage_any_str=[]
		dig_latency_str=""
		freeze_latency_str=""
		any_latency_str=""
		global resetbutton
				          
		""" Reset the stopwatch. """
		self._start = time.time()         
		self._elapsedtime = 0.0    
		self._setTime(self._elapsedtime)   
		resetbutton.configure(activebackground=defaultbg, bg=defaultbg)                
    	
    
	def _setTime(self, elap):	#Only to have a nice time display
		
		""" Set the time string to Minutes:Seconds:Hundreths """
		minutes = int(elap/60)
		seconds = int(elap - minutes*60.0)
		hseconds = int((elap - minutes*60.0 - seconds)*100)                
		self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))
        
	
		
	def Analyze(self):
		global var1,var2,var3
		global percentage_time_str
		percentage_time_str=[]
		global percentage_freeze_str
		percentage_freeze_str=[]
		global percentage_dig_str
		percentage_dig_str=[]
		global percentage_any_str, dig_latency_str, freeze_latency_str, any_latency_str
		percentage_any_str=[]
		dig_latency_str=""
		freeze_latency_str=""
		any_latency_str=""
		
		
		if locale_var=="Comma":
			dig_latency_str=str(dig_latency).replace(".", ",")
			freeze_latency_str=str(freeze_latency).replace(".", ",")
			any_latency_str=str(any_latency).replace(".", ",")
			
			for x in range(0,(len(percentage_time)) ):
				percentage_any_str.append(str(percentage_any[x]).replace(".", ","))
				percentage_time_str.append(str(percentage_time[x]).replace(".", ","))
				percentage_freeze_str.append(str(percentage_freeze[x]).replace(".", ","))
				percentage_dig_str.append(str(percentage_dig[x]).replace(".", ","))
				
		if locale_var=="Point":
			dig_latency_str=str(dig_latency).replace(",", ".")
			freeze_latency_str=str(freeze_latency).replace(",", ".")
			any_latency_str=str(any_latency).replace(",", ".")
			
			for x in range(0,(len(percentage_time)) ):
				percentage_any_str.append(str(percentage_any[x]).replace(",", "."))
				percentage_time_str.append(str(percentage_time[x]).replace(",", "."))
				percentage_freeze_str.append(str(percentage_freeze[x]).replace(",", "."))
				percentage_dig_str.append(str(percentage_dig[x]).replace(",", "."))


		
		def saveasf():
			self.file_opt = options = {}
			options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
			options['initialfile'] = 'freezing_.txt'
			filename = tkFileDialog.asksaveasfilename(**self.file_opt)
			myFile=open(filename,"w")
			myFile.write("[Time Bins]"+"\t"+"[% Freezing]"+"\n")
			for w,x in zip(percentage_time_str,percentage_freeze_str):
				myFile.write(str(w)+"\t"+"\t"+str(x)+"\n")
			myFile.write("Latency to freeze (s):"+"\t"+str(freeze_latency_str))
			myFile.close()	
			
		def saveasd():
			self.file_opt = options = {}
			options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
			options['initialfile'] = 'digging_.txt'
			filename = tkFileDialog.asksaveasfilename(**self.file_opt)
			myFile=open(filename,"w")
			myFile.write("[Time Bins]"+"\t"+"[% Digging]"+"\n")
			for w,x in zip(percentage_time_str,percentage_dig_str):
				myFile.write(str(w)+"\t"+"\t"+str(x)+"\n")
			myFile.write("Latency to dig (s):"+"\t"+str(dig_latency_str))
			myFile.close()	
			
		def saveasa():
			self.file_opt = options = {}
			options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
			options['initialfile'] = 'anything_.txt'
			filename = tkFileDialog.asksaveasfilename(**self.file_opt)
			myFile=open(filename,"w")
			myFile.write("[Time Bins]"+"\t"+"[% Anything]"+"\n")
			for w,x in zip(percentage_time_str,percentage_any_str):
				myFile.write(str(w)+"\t"+"\t"+str(x)+"\n")
			myFile.write("Latency to anything (s):"+"\t"+str(any_latency_str))
			myFile.close()	
		
		if var1.get()==1:	
			top = Toplevel()
			top.title("Freezing")
			menubar = Menu(top)
			menubar.add_command(label="Save", command=saveasf)
			S = Scrollbar(top)
			lines=len(percentage_time)+4
			T = Text(top, height=lines, width=20)
			D = Text(top, height=lines, width=40)
			S.pack(side=RIGHT, fill=Y)
			T.pack(side=LEFT, fill=Y)
			D.pack(side=LEFT, fill=Y)
			S.config(command=T.yview)
			T.config(yscrollcommand=S.set)
			D.config(yscrollcommand=S.set)
			T.insert(END,"[Time Bins (s)]"+"\n")
			T.insert(END,"\n")
			for w in percentage_time_str:
				T.insert(END, str(w)+"\n")
					
			D.insert(END,"[% Freezing]"+"\n")
			D.insert(END,"\n")
			for x in percentage_freeze_str:
				D.insert(END, str(x)+"\n")
			D.insert(END,"\n")	
			D.insert(END,"Latency to freeze (s):"+"\t"+str(freeze_latency_str))
			top.config(menu=menubar)
		
		if var2.get()==1:	
			top = Toplevel()
			top.title("Digging")
			menubar = Menu(top)
			menubar.add_command(label="Save", command=saveasd)
			S = Scrollbar(top)
			lines=len(percentage_time)+4
			T = Text(top, height=lines, width=20)
			D = Text(top, height=lines, width=40)
			S.pack(side=RIGHT, fill=Y)
			T.pack(side=LEFT, fill=Y)
			D.pack(side=LEFT, fill=Y)
			S.config(command=T.yview)
			T.config(yscrollcommand=S.set)
			D.config(yscrollcommand=S.set)
			T.insert(END,"[Time Bins (s)]"+"\n")
			T.insert(END,"\n")
			for w in percentage_time_str:
				T.insert(END, str(w)+"\n")
					
			D.insert(END,"[% Digging]"+"\n")
			D.insert(END,"\n")
			for x in percentage_dig_str:
				D.insert(END, str(x)+"\n")
			D.insert(END,"\n")	
			D.insert(END,"Latency to dig (s):"+"\t"+str(dig_latency_str))
			top.config(menu=menubar)
					
		#if var2.get()==1:	
			#top = Toplevel()
			#top.title("Digging")
			#menubar = Menu(top)
			#menubar.add_command(label="Save", command=saveasd)
			#S = Scrollbar(top)
			#lines=len(percentage_time)+2
			#T = Text(top, height=lines, width=40)
			#S.pack(side=RIGHT, fill=Y)
			#T.pack(side=LEFT, fill=Y)
			#S.config(command=T.yview)
			#T.config(yscrollcommand=S.set)
			#T.insert(END,"[Time Bins]"+"\t"+"\t"+"[% Digging]"+"\n")
			#for w,x in zip(percentage_time_str,percentage_dig_str):
				#T.insert(END, str(w)+"\t"+"\t"+str(x)+"\n")
			#T.insert(END,"Latency to dig (s):"+"\t"+str(dig_latency_str))
			#top.config(menu=menubar)

		if var3.get()==1:	
			top = Toplevel()
			top.title("Anything")
			menubar = Menu(top)
			menubar.add_command(label="Save", command=saveasa)
			S = Scrollbar(top)
			lines=len(percentage_time)+4
			T = Text(top, height=lines, width=20)
			D = Text(top, height=lines, width=40)
			S.pack(side=RIGHT, fill=Y)
			T.pack(side=LEFT, fill=Y)
			D.pack(side=LEFT, fill=Y)
			S.config(command=T.yview)
			T.config(yscrollcommand=S.set)
			D.config(yscrollcommand=S.set)
			T.insert(END,"[Time Bins (s)]"+"\n")
			T.insert(END,"\n")
			for w in percentage_time_str:
				T.insert(END, str(w)+"\n")
					
			D.insert(END,"[% Anything]"+"\n")
			D.insert(END,"\n")	
			for x in percentage_any_str:
				D.insert(END, str(x)+"\n")
			D.insert(END,"\n")	
			D.insert(END,"Latency to anything (s):"+"\t"+str(any_latency_str))
			top.config(menu=menubar)		
	
		#if var3.get()==1:	
			#top = Toplevel()
			#top.title("Anything")
			#menubar = Menu(top)
			#menubar.add_command(label="Save", command=saveasa)
			#S = Scrollbar(top)
			#lines=len(percentage_time)+2
			#T = Text(top, height=lines, width=40)
			#S.pack(side=RIGHT, fill=Y)
			#T.pack(side=LEFT, fill=Y)
			#S.config(command=T.yview)
			#T.config(yscrollcommand=S.set)
			#T.insert(END,"[Time Bins]"+"\t"+"\t"+"[% Anything]"+"\n")
			#for w,x in zip(percentage_time_str,percentage_any_str):
				#T.insert(END, str(w)+"\t"+"\t"+str(x)+"\n")
			#T.insert(END,"Latency to anything (s):"+"\t"+str(any_latency_str))
			#top.config(menu=menubar)
		

			
	def about(self):
		top = Toplevel()
		top.title("About")
		msg = Message(top, font=('arial', 10, 'normal'), text="This software has been designed and" 
		" is maintained by Andreas J. Genewsky (2014). Original and up-to-date version can be found at https://github.com/AGenews/tantalus"+"\n"+version_info, width=300)
		msg.pack()
		button = Button(top, text="Ok", command=top.destroy)
		button.pack()
	
	def helpdia(self):
		top = Toplevel()
		top.title("Help")
		S = Scrollbar(top)
		T = Text(top, height=10, width=60,wrap=WORD,spacing1=2,spacing2=2,spacing3=2)
		S.pack(side=RIGHT, fill=Y)
		T.pack(side=LEFT, fill=Y)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.tag_configure('big', font=('arial', 16, 'bold'))
		T.tag_configure('standard', font=('arial', 10, 'normal'))
		T.insert(END,'\nHelp Menu\n', 'big')
		quote = """Working with Tantalus is actually quite straight forward. Activate \
the modes you'd like to score (Freezing, Digging, Anything). Already \
now you can press the keys and see if they are working (the field \
EVENT DETECTED should turn green). But remember, the Tantalus main window needs to be active for Tantalus to recognize an event! 
Now you might have a look at the SETTINGS menu.

>>> Session Length:
This variable determines how long Tantalus scores your button presses. The default value is set to 180 seconds.
>>> Sample Interval:
This variable determines the update intervall of the clock but also the resolution of your scoring. It also determines the minimal temporal error which is two times the sample intervall. Just leave it at the default value which is 10 ms.
>>> Time Bin:
This variable determines the size of the temporal bin by which the scored data is devided. The default is 20 seconds. The bin affects the scoring process directly!
>>> Decimal Separator:
Here you can choose which decimal separator you'd like to have. It is independent of the systems settings and doesn't at all take the locale settings into account. The default is Point.
>>> Write Config File:
This function generates a file called tantalus_config.cfg and overwrites the same file. It allows you to save the settings mentioned above, but also the states of the MODE toggle switches (Freezing, Digging etc.). So next time you load Tantalus, exactly those settings are used. If now tanatalus_config.cfg is present in the same folder where Tantalus.exe is, only default values will be used.

Now lets have a look at all thes buttons:

>>> Start:
This button starts the timer and changes its color to red, when the clock is ticking.
>>> Stop:
This button stops the timer. If a time bin is not complete the data is lost.
>>> Reset:
This button erases the old data and resets the timer.
>>> Quit:
This button terminates Tantalus.
>>> Show Data:
After pressing this button one window per mode (Freezing, Digging, etc.) will appear. Here you can Copy&Paste your data e.g. to Excel. With the 'Save' function you can save this individual file somewhere. At the end you find the latency in seconds. Changing the Decimal separator allows you to show the data again with e.g. a comma instead of a point as often as you want until you RESET.

You can also decide to save everthing just by clicking File>Save as.

Enjoy!
Andreas Genewsky (October 2014)

"""
		T.insert(END, quote, 'standard')
		T.pack(side=LEFT)


			
	def setsessleng(self):
		top = Toplevel()
		top.title("Set Session length")
		
		def on_button_click(event):
			global sessionlength
			sessionlength=w.get()
			top.destroy()
			self.msg.config(text = sessleng + str(sessionlength) + " s", width=300)
						
		msg = Message(top, font=('arial', 10, 'normal'), text="Set the session length in seconds", width=300)
		msg.pack()
		var = StringVar(top)
		var.set("180")
		w = Spinbox(top, from_=1, to=3600, textvariable=var)
		w.pack()
		button = Button(top, text="Ok", command=on_button_click)
		button.bind("<Button-1>", on_button_click) 
		button.pack()
		
	def setsampinter(self):
		top = Toplevel()
		top.title("Set Sample Interval")
			
		def on_button_click(event):
			global sampleinterval
			sampleinterval=w.get()
			top.destroy()
			self.msg2.config(text = sampinter + str(sampleinterval) + " ms", width=300)
			
		msg2 = Message(top, font=('arial', 10, 'normal'), text="Set the sample interval in milliseconds", width=300)
		msg2.pack()
		var = StringVar(top)
		var.set("10")
		w = Spinbox(top, from_=10, to=100, textvariable=var)
		w.pack()
		button = Button(top, text="Ok", command=on_button_click)
		button.bind("<Button-1>", on_button_click) 
		button.pack()
		
	def settimbin(self):
		top = Toplevel()
		top.title("Set Time Bin")
			
		def on_button_click(event):
			global timebin
			timebin=w.get()
			top.destroy()
			self.msg3.config(text = timbi + str(timebin) + " s", width=300)
			
		msg3 = Message(top, font=('arial', 10, 'normal'), text="Set Time Bin in seconds", width=300)
		msg3.pack()
		var = StringVar(top)
		var.set("20")
		w = Spinbox(top, from_=1, to=600, textvariable=var)
		w.pack()
		button = Button(top, text="Ok", command=on_button_click)
		button.bind("<Button-1>", on_button_click) 
		button.pack()
	
	def saveas(self):
		filename = tkFileDialog.asksaveasfilename(**self.file_opt)
		myFile=open(filename,"w")
		myFile.write("[Time Bins]"+"\t"+"[% Anything]"+"\t"+"[% Freezing]"+"\t"+"[% Digging]"+"\n")
		for w,x,y,z in zip(percentage_time_str,percentage_any_str,percentage_freeze_str,percentage_dig_str):
			myFile.write(str(w)+"\t"+"\t"+str(x)+"\t"+"\t"+str(y)+"\t"+"\t"+str(z)+"\n")
		myFile.write("Latency to freeze (s):"+"\t"+str(freeze_latency_str)+"\n")
		myFile.write("Latency to dig (s):"+"\t"+str(dig_latency_str)+"\n")
		myFile.write("Latency to anything (s):"+"\t"+str(any_latency_str)+"\n")
		myFile.close()
		
	def setlocales(self):
		global v
		top = Toplevel()
		top.title("Decimal Separator")
		
		msg3 = Message(top, font=('arial', 10, 'normal'), text="Set Decimal Separator", width=300)
		msg3.pack()
		
		v = IntVar()
		Radiobutton(top, text="Comma", variable=v, value=1).pack(anchor=W)
		Radiobutton(top, text="Point", variable=v, value=2).pack(anchor=W)
			
			
		def on_button_click(event):
			global locale_var
			if v.get()==1:
				locale_var="Comma"
			elif v.get()==2:
				locale_var="Point"
			top.destroy()
			self.msg7.config(text = separator + locale_var, width=300)
			

		button = Button(top, text="Ok", command=on_button_click)
		button.bind("<Button-1>", on_button_click) 
		button.pack()
	
	def config_file(self):
		config = ConfigParser.RawConfigParser()
		global sessionlength, sampleinterval, timebin, locale_var, var1, var2, var3
		# When adding sections or items, add them in the reverse order of
		# how you want them to be displayed in the actual file.
		# In addition, please note that using RawConfigParser's and the raw
		# mode of ConfigParser's respective set functions, you can assign
		# non-string values to keys internally, but will receive an error
		# when attempting to write to a file or when you get it in non-raw
		# mode. SafeConfigParser does not allow such assignments to take place.
		config.add_section('Settings')
		config.set('Settings', 'sessionlength', sessionlength)
		config.set('Settings', 'sampleinterval', sampleinterval)
		config.set('Settings', 'timebin', timebin)
		config.set('Settings', 'locale_var', locale_var)
		config.set('Settings', 'freezingon', int(var1.get()) )
		config.set('Settings', 'diggingon', int(var2.get()) )
		config.set('Settings', 'anythingon', int(var3.get()) )
		
		with open('tantalus_config.cfg', 'wb') as configfile:
			config.write(configfile)
			
				
	


	        
def main(): 
	root = Tk()
	lo=logger(root)
	lo.pack(side=TOP)
	global defaultbg
	defaultbg = root.cget('bg')
	global startbutton
	global resetbutton
	
	
	def fkeyon(event): #Here we detect the Key pressed event
		global freeze_var, var1
		freeze_var=1
		if var1.get()==1:	
			b.config(state=DISABLED,relief=RAISED,activebackground="green",activeforeground="black" \
			,disabledforeground="black",bg="green",foreground="black")
		
	def fkeyoff(event): #Here we detect the key release event
		global freeze_var, var1
		freeze_var=0
		if var1.get()==1:
			b.config(state=DISABLED,relief=RAISED,activebackground="white",activeforeground="black" \
			,disabledforeground="black",bg="white",foreground="black")
	
	def dkeyon(event): #Here we detect the Key pressed event
		global dig_var, var2
		dig_var=1
		if var2.get()==1:
			b.config(state=DISABLED,relief=RAISED,activebackground="green",activeforeground="black" \
			,disabledforeground="black",bg="green",foreground="black")
		
	def dkeyoff(event): #Here we detect the key release event
		global dig_var, var2
		dig_var=0
		if var2.get()==1:
			b.config(state=DISABLED,relief=RAISED,activebackground="white",activeforeground="black" \
			,disabledforeground="black",bg="white",foreground="black")
	
	def akeyon(event): #Here we detect the Key pressed event
		global any_var, var3
		any_var=1
		if var3.get()==1:
			b.config(state=DISABLED,relief=RAISED,activebackground="green",activeforeground="black" \
			,disabledforeground="black",bg="green",foreground="black")
			
	def akeyoff(event): #Here we detect the key release event
		global any_var, var3
		any_var=0
		if var3.get()==1:
			b.config(state=DISABLED,relief=RAISED,activebackground="white",activeforeground="black" \
			,disabledforeground="black",bg="white",foreground="black")
		
	def keystart(event):
		lo.Start()
	
	def keystop(event):
		lo.Stop()

	def keyreset(event): 
		lo.Reset()
		
	def keyshow(event): 
		lo.Analyze()


	
	frame = Frame(root, width=300, height=0)
	frame.focus_set()
	frame.bind("<f>", fkeyon)
	frame.bind("<KeyRelease-f>", fkeyoff)
	frame.bind("<d>", dkeyon)
	frame.bind("<KeyRelease-d>", dkeyoff)
	frame.bind("<a>", akeyon)
	frame.bind("<KeyRelease-a>", akeyoff)
	frame.bind("<space>", keystart)
	frame.bind("<b>", keystop)
	frame.bind("<r>", keyreset)
	frame.bind("<n>", keyshow)
	frame.bind("<q>", root.quit)
	frame.pack()
	
	buttonframe = Frame(root, width=300, height=50)
	Button(buttonframe, text='Show Data\n(n)', command=lo.Analyze).pack(side=LEFT)
	startbutton=Button(buttonframe, text='Start\n(space)', command=lo.Start)
	startbutton.pack(side=LEFT)
	Button(buttonframe, text='Stop\n(b)', command=lo.Stop).pack(side=LEFT)
	resetbutton=Button(buttonframe, text='Reset\n(r)', command=lo.Reset)
	resetbutton.pack(side=LEFT)
	Button(buttonframe, text='Quit \n', command=root.quit).pack(side=LEFT)
	buttonframe.pack()
	
	menubar = Menu(root)
	# create a pulldown menu, and add it to the menu bar
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Save as", command=lo.saveas)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	settingsmenu = Menu(menubar, tearoff=0)
	settingsmenu.add_command(label="Session Length", command=lo.setsessleng)
	settingsmenu.add_command(label="Time Bin", command=lo.settimbin)
	settingsmenu.add_command(label="Sample Interval", command=lo.setsampinter)
	settingsmenu.add_command(label="Decimal Separator", command=lo.setlocales)
	settingsmenu.add_separator()
	settingsmenu.add_command(label="Write Configuration File", command=lo.config_file)
	menubar.add_cascade(label="Settings", menu=settingsmenu)
	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help", command=lo.helpdia)
	helpmenu.add_command(label="About", command=lo.about)
	menubar.add_cascade(label="Help", menu=helpmenu)


	
	# display the menu
	root.config(menu=menubar)
	root.wm_title("Tantalus | "+version_info)

	#root.iconbitmap('@mouse.ico')
	root.mainloop( )
	#atexit.register(exit_handler)


if __name__ == '__main__':
    main()


