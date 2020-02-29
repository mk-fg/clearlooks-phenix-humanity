#!/usr/bin/python

import os, sys, pathlib as pl, subprocess as sp

# glob-patterns for files to process with gtk-encode-symbolic-svg
svg_globs = ['dropdown-*.svg']
p_img = pl.Path(__file__).parent / 'gtk-3.0/img'

for pat in svg_globs:
	for p in p_img.glob(pat):
		p_png = p_img / (p.name.rsplit('.', 1)[0] + '.png')
		try: ts_dst = p_png.stat().st_mtime
		except OSError: ts_dst = 0
		if p.stat().st_mtime <= ts_dst: continue

		# Note: gtk-encode-symbolic-svg produces very blurry icons, unlike inkscape
		cmd = (
			'inkscape --without-gui --export-dpi=90 --export-background-opacity=0'.split()
			+ ['--export-png', str(p_png), str(p)] )
		print(' '.join(cmd))
		sp.run(cmd, check=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
