#!/usr/bin/python

import os, sys, pathlib as pl, subprocess as sp
import xml.etree.ElementTree as et

# glob-patterns for files to process with gtk-encode-symbolic-svg
svg_globs = ['arrow-*.svg']
p_img = pl.Path(__file__).parent / 'gtk-3.0/img'

for pat in svg_globs:
	for p in p_img.glob(pat):
		p_png = p_img / (p.name.rsplit('.', 1)[0] + '.symbolic.png')
		try: ts_dst = p_png.stat().st_mtime
		except OSError: ts_dst = 0
		if p.stat().st_mtime <= ts_dst: continue

		svg = et.parse(p).getroot()
		wh = svg.attrib['width'] + 'x' + svg.attrib['height']

		cmd = ['gtk-encode-symbolic-svg', '-o', str(p_img), str(p), wh]
		print(' '.join(cmd))
		sp.run(cmd, check=True)
