#-*- coding: utf-8 -*-
import wx
from wx.lib.scrolledpanel import ScrolledPanel
from selenium import webdriver
import os
import random
from datetime import datetime
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class MyPanel(ScrolledPanel):
	def __init__(self, parent):
		ScrolledPanel.__init__(self, parent)
 
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Visual similarity comparison
		self.mainSizer.Add(wx.StaticText(self, label="Rate the page look similarity:"), 0, wx.CENTER|wx.ALL, 25)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(wx.StaticText(self, label="Not similar"))
		self.visualSlider = wx.Slider(self, value=10, maxValue=10, style=wx.SL_LABELS)
		hbox.Add(self.visualSlider, 0)
		hbox.Add(wx.StaticText(self, label="Exactly the same"))
		self.mainSizer.Add(hbox, 0, wx.CENTER)

		# Content completion comparison
		self.mainSizer.Add(wx.StaticText(self, label="Rate the page content similarity:"), 0, wx.CENTER|wx.ALL, 25)
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(wx.StaticText(self, label="Not similar"))
		self.contentSlider = wx.Slider(self, value=10, maxValue=10, style=wx.SL_LABELS)
		hbox.Add(self.contentSlider, 0)
		hbox.Add(wx.StaticText(self, label="Exactly the same"))
		self.mainSizer.Add(hbox, 0, wx.CENTER, 25)
		
		# Identify types of missing content
		self.mainSizer.Add(wx.StaticText(self, label="What types of content are missing? Check all that apply."), 0, wx.CENTER|wx.ALL, 25)
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.contentTypes = []
		self.contentTypes.append(wx.CheckBox(self, label="Text"))
		self.contentTypes.append(wx.CheckBox(self, label="Images"))
		self.contentTypes.append(wx.CheckBox(self, label="Advertisements"))
		self.contentTypes.append(wx.CheckBox(self, label="Video"))
		self.contentTypes.append(wx.CheckBox(self, label="Layout/beautifiers"))
		self.contentTypes.append(wx.CheckBox(self, label="Images"))
		self.contentTypes.append(wx.CheckBox(self, label="Other embeds (i.e. maps, tweets)"))

		for c in self.contentTypes:
			vbox.Add(c, 0, wx.LEFT)
		self.mainSizer.Add(vbox, 0, wx.CENTER)

		# Count specific types of elements
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		instruction = wx.StaticText(self, label="Identify the number of menu / navigation elements:")
		vbox.Add(instruction, 0, wx.TOP, 20)
		instruction = wx.StaticText(self, label="Identify the number of search bars:")
		vbox.Add(instruction, 0, wx.BOTTOM|wx.TOP, 5)
		instruction = wx.StaticText(self, label="Identify the number of image scrollers / galleries:")
		vbox.Add(instruction, 0, wx.BOTTOM, 5)

		hbox.Add(vbox, 0, wx.ALIGN_LEFT | wx.RIGHT, 25)

		self.inputs = []
		for j in range(2):
			vbox = wx.BoxSizer(wx.VERTICAL)
			if j == 0:
				vbox.Add(wx.StaticText(self, label="Left window"))
			else:
				vbox.Add(wx.StaticText(self, label="Right window"))
			for i in range(3):
				user_input = wx.TextCtrl(self)
				user_input.Size.SetWidth(20)
				self.inputs.append(user_input)
				vbox.Add(user_input, 0)

			hbox.Add(vbox, 0)

		self.mainSizer.Add(hbox, 0, wx.ALL | wx.CENTER, 25)

		# Next page button
		self.submit_btn = wx.Button(self, label='Next page')
		self.submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
		self.mainSizer.Add(self.submit_btn, 0, wx.CENTER | wx.BOTTOM, 25)

		# StaticText field for error messages
		self.msg_box = wx.StaticText(self, label="")
		self.msg_box.SetForegroundColour((255,0,0)) # make text red
		self.mainSizer.Add(self.msg_box, 0, flag=wx.LEFT, border=25)

		self.SetSizer(self.mainSizer)
		self.SetupScrolling()
		self.cnt = 0
		self.analyze()

	def analyze(self):
		self.url = random.choice(sites)
		self.url = sites[self.cnt]
		self.cnt = self.cnt + 1 % len(sites)
		print(self.url)
		try:
			driver1.get(self.url)
			if (self.url[-1] == '/'):
				driver2.get(self.url + "JSCleaner.html")
			else:
				driver2.get(self.url + "/JSCleaner.html")
			self.msg_box.SetLabel("")
		except Exception as e:
			self.msg_box.SetLabel(str(e))
			print(e)
			return

	def on_submit(self, event):
		self.msg_box.SetLabel("Please wait... loading page")
		with open('results.csv', 'a+') as file:
			try:
				mc = [c.GetValue() for c in self.contentTypes]
				ans = []
				for i in self.inputs:
					if i.GetValue() == "":
						raise ValueError("No input in textfield")
					ans.append(i.GetValue())
			except ValueError:
				self.msg_box.SetLabel("Please answer all questions")
				return
			print(self.url, file=file, end=',')
			print(str(self.visualSlider.GetValue())+ ',' + str(self.contentSlider.GetValue()), file=file, end=',')
			for i in mc + ans:
				print(i, file=file, end=',')
			print(datetime.now(), file=file)

		self.visualSlider.SetValue(10)
		self.contentSlider.SetValue(10)
		for c in self.contentTypes:
			c.SetValue(False)
		for i in self.inputs:
			i.SetValue("")
		self.msg_box.SetLabel("")
		self.analyze()

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, parent=None, title="Comparison Evaluation")
		
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()
		exitMenuItem = fileMenu.Append(101, "Exit", "Exit the application")
		aboutMenuItem = fileMenu.Append(102, "About", "About")

		menuBar.Append(fileMenu, "&File")
		self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
		self.Bind(wx.EVT_MENU, self.onAbout, aboutMenuItem)
		self.SetMenuBar(menuBar)

		self.fSizer = wx.BoxSizer(wx.VERTICAL)
		panel = MyPanel(self)
		self.fSizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.fSizer)
		self.Fit()
		self.Show()

	def onExit(self, event):
		self.Close()

	def onAbout(self, event):
		msg = wx.MessageDialog(self, "This tool is built for evaluation of simplified pages by the ComNets AD lab @ NYUAD. October 2019.","About",wx.OK | wx.ICON_INFORMATION)
		msg.ShowModal()

if __name__ == "__main__":
	app = wx.App(False)
	width, height = wx.GetDisplaySize()
	
	options = FirefoxOptions()
	options.log.level = "trace"
	options.add_argument("--width="+str(width/2))
	options.add_argument("--height="+str(height))

	# start selenium firefox web driver
	fp1 = webdriver.FirefoxProfile("/Users/Jacinta/Library/Application Support/Firefox/Profiles/kciui8dl.default")
	fp2 = webdriver.FirefoxProfile("/Users/Jacinta/Library/Application Support/Firefox/Profiles/7irvo3ii.Simplified")
	# fp.set_preference("devtools.toolbox.selectedTool", "netmonitor")
	# fp.set_preference("browser.cache.disk.enable", False)
	# fp.set_preference("browser.cache.memory.enable", False)
	# fp.set_preference("browser.cache.offline.enable", False)
	# fp.set_preference("network.http.use-cache", False)
	driver1 = webdriver.Firefox(options=options, firefox_profile=fp1)
	driver2 = webdriver.Firefox(options=options, firefox_profile=fp2)
	driver1.set_window_position(0, 0)
	driver2.set_window_position(width/2, 0)

	# Open a random site from the top 500
	f = open("top25.txt", 'r')
	sites = f.read().split()
	f.close()

	frame = MyFrame()
	frame.SetSize(800, 650)

	app.MainLoop()
	driver1.quit()
	driver2.quit()
