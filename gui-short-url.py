from __future__ import with_statement
from tkinter import Tk, Label, Entry, END, W, E, Button, StringVar
from tkmacosx import Button, ColorVar
import contextlib
import pyperclip
try: 
	from urllib.parse import urlencode
	from urllib.error import HTTPError
except ImportError:
	from urllib import urlencode

from urllib.request import urlopen


# description: URL SHORTENER
class URLShortener(object):
	LABEL_TEXT = [
		'Type your URL: ',
		'Shorten URL: ',
		'Quit',
		'Reset'
	]
	
	def __init__(self, master):
		# color vars
		black_txt = ColorVar(value='#000')
		red_bg = ColorVar(value='red')
		blue_bg = ColorVar(value='blue')
		wht_txt = ColorVar(value='#fff')
		
		# title
		master.title('URL Shortener')
		
		# label 'Type your URL'
		self.typeurl_label_text = StringVar()
		self.typeurl_label_text.set(self.LABEL_TEXT[0])
		self.label = Label(master, textvariable=self.typeurl_label_text).grid(row=0, column=1, sticky=W)
		
		# results label
		self.message = ''
		self.show_results_text = StringVar()
		self.show_results_text.set(self.message)
		self.results_label = Label(master, textvariable=self.show_results_text, fg=red_bg)
		self.results_label.grid(row=0, column=2, sticky=E)
		
		# Type your URL field box
		self.typeurl_input_box = Entry(master)
		self.typeurl_input_box.grid(row=1, sticky=W+E, column=1, columnspan=3)
	
		# Button Quit
		self.quit_btn = Button(master, text=self.LABEL_TEXT[2], bg=red_bg, fg=wht_txt, borderless=1, command=master.quit)
		self.quit_btn.grid(row=3, column=1, sticky=W+E)
		# Button Shortener
		self.shorturl_btn = Button(master, text=self.LABEL_TEXT[1], fg=black_txt, borderless=1, command=self.make_tiny)
		self.shorturl_btn.grid(row=3, column=2, sticky=W + E)
		self.shorturl_btn.focus_set()
		# Button Reset
		self.reset_btn = Button(master, text=self.LABEL_TEXT[3], bg=blue_bg, fg=wht_txt, borderless=1, command=self.reset)
		self.reset_btn.grid(row=3, column=3, sticky=W+E)
		

	def make_tiny(self):
		full_url = self.typeurl_input_box.get()
		if not full_url:
			self.message = 'Please type a url'
			self.show_results_text.set(self.message)
		else:
			url = full_url.strip()
			try:
				request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
				with contextlib.closing(urlopen(request_url)) as response:
					self.message = response.read().decode('utf-8')
					self.show_results_text.set(self.message + ' - Copy to clipboard')
					pyperclip.copy(self.message)
			except HTTPError as err:
				if err.code == 400:
					self.message = 'Please enter a real URL'
					self.show_results_text.set(self.message)
	
	def reset(self):
		self.typeurl_input_box.delete(0, END)
		self.message = ''
		self.show_results_text.set(self.message)
		

root: Tk = Tk()
urlShorter: URLShortener = URLShortener(root)
root.mainloop()
