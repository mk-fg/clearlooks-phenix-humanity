#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os, sys, string, subprocess as sp, functools as ft


class adict(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__dict__ = self

def render(wt, app):
	name = app.get_application_id()
	win = Gtk.ApplicationWindow(name=name, title=name, application=app)
	win.connect('destroy', lambda w: app.quit())

	win.set_default_size(600, 400)
	ww = w = Gtk.ScrolledWindow()
	win.add(w)

	if wt == 'textview':
		## Long/wide TextView to test scrollbar styles
		txt = sp.run(
			'pandoc -f rst -t plain --wrap=none README.rst'.split(),
			check=True, stdout=sp.PIPE, stderr=sp.DEVNULL )
		txt = txt.stdout.decode()
		w = Gtk.TextView()
		w.set_wrap_mode(Gtk.WrapMode.NONE)
		w.get_buffer().set_text(txt)
		ww.add(w)

	elif wt == 'table':
		## Table to test TreeView/.cell styles
		table_dim = adict(w=3, h=10)
		table = Gtk.ListStore.new([str]*table_dim.w)
		for row in range(table_dim.h):
			table.append(list(
				f'cell {row:02d} {string.ascii_uppercase[n]}'
				for n in range(table_dim.w) ))
		w = Gtk.TreeView( model=table,
			reorderable=False, headers_visible=True, enable_search=False )
		for n in range(table_dim.w):
			w.append_column(Gtk.TreeViewColumn(
				title=f'column-{n}', text=n,
				cell_renderer=Gtk.CellRendererText() ))
		ww.add(w)

	else:
		app.quit()
		raise ValueError(wt)

	win.show_all()


def main(args=None):
	import argparse, textwrap
	dd = lambda text: (textwrap.dedent(text).strip('\n') + '\n').replace('\t', '  ')
	fill = lambda s,w=90,ind='  ',ind_next=None,**k: textwrap.fill(
		s, w, initial_indent=ind, subsequent_indent=ind if ind_next is None else ind_next, **k )

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawTextHelpFormatter,
		description='Simple placeholder/demo app to show and theme various widgets.')
	parser.add_argument('widget', help=dd('''
		Widget type to render, supported ones:

		- textview - Large editable textview in scrolledwindow.
			Requires pandoc to get un-wrapped text from README.rst.

		- table - treeview with couple rows/cells.
			These are non-introspectable and have buggy primitive styling in gtk-3.24.'''))

	opts = parser.parse_args(sys.argv[1:] if args is None else args)

	app = Gtk.Application.new('gtk3-widget-demo.IUG66', 0)
	app.connect('activate', ft.partial(render, opts.widget))
	app.run()


if __name__ == '__main__':
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	sys.exit(main())
