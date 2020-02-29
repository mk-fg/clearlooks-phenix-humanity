#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os, sys, subprocess as sp


class DemoWin(Gtk.ApplicationWindow):

	def __init__(self, app, txt):
		name = 'gtk3-widget-demo.IUG66'
		super().__init__(name=name, application=app)
		self.set_title(name)
		self.connect('destroy', lambda a: app.quit())

		self.set_default_size(600, 400)

		# ScrolledWindow -> TextView to test scrollbar styles
		ww = w = Gtk.ScrolledWindow()
		self.add(w)
		w = Gtk.TextView()
		w.set_wrap_mode(Gtk.WrapMode.NONE)
		w.get_buffer().set_text(txt)
		ww.add(w)

		self.show_all()


class DemoApp(Gtk.Application):

	def __init__(self, txt):
		super().__init__()
		self.txt = txt

	def do_activate(self):
		self.win = DemoWin(self, self.txt)


def main(args=None):
	import argparse
	parser = argparse.ArgumentParser(
		description='Simple placeholder/demo app to show and theme various widgets.')
	opts = parser.parse_args(sys.argv[1:] if args is None else args)

	txt = sp.run(
		'pandoc -f rst -t plain --wrap=none README.rst'.split(),
		check=True, stdout=sp.PIPE, stderr=sp.DEVNULL )
	txt = txt.stdout.decode()
	DemoApp(txt).run()

if __name__ == '__main__':
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	sys.exit(main())
