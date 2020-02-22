#!/usr/bin/env python3

import pathlib as pl, collections as cs, dataclasses as dc
import os, sys, re, tempfile, subprocess as sp

import textx as tx # pip3 install --user textx


tx_css = tx.metamodel_from_str('''
css: blocks*=block;
block: st=statement | c=comment;

statement: sels+=sel '{' rules+=rule '}';
comment: '/*' body=/(?s).*?(?=\*\/)/ '*/';

rule: name=/[-\w]+/ ':' val=/[^;]+/ ';' | comment;
sel: atoms+=sel_atom ','?;
sel_atom: /[-\w.:>]+/ | '*';
''')


class TemplateError(Exception): pass

@dc.dataclass
class Subst:
	a: int
	b: int = -1
	s: str = ''
	strip_tail: bool = False

@dc.dataclass
class Ext:
	sels: list
	prefix: bool = False # whether these are prefixes

def template(css_tpl, print_diffs=False):
	m = tx_css.model_from_str(css_tpl)
	substs = list() # all text-replacement Subst's

	# Build by-selector index of statements and extensions
	ext_idx, st_idx = cs.defaultdict(list), cs.defaultdict(list)
	# Also dict of all -x-var-* variables to find/replace later
	ext_vars = dict()

	for st in tx.model.get_children_of_type('statement', m):
		sel_exts = list(s for s in st.sels if '-ext' in s.atoms)
		if not sel_exts:
			for s in st.sels: st_idx[tuple(s.atoms)].append(st)
			continue
		st_str = ' '.join(css_tpl[st._tx_position:st._tx_position_end].splitlines())

		if len(sel_exts) != len(st.sels):
			sel_list = list(' '.join(s.atoms) for s in st.sels)
			raise TemplateError(f'Mixed -ext and regular selectors: {sel_list}')
		substs.append(Subst(st._tx_position, st._tx_position_end, strip_tail=True))

		sel_prefixes = list( # remaining selectors with -ext stripped
			filter(None, (' '.join(a for a in s.atoms if a != '-ext') for s in sel_exts)) )

		for rule in st.rules:
			if not rule.name: continue # comment
			if rule.name in ['-x-same-as', '-x-same-rules']:
				if not sel_prefixes:
					raise TemplateError(f'Bogus statement with -ext selector and no prefixes: {st_str!r}')
				prefix = rule.name == '-x-same-as'
				for s in rule.val.split(','):
					s = tuple(s.strip().split())
					ext_idx[s].append(Ext(sel_prefixes, prefix=prefix))
			elif rule.name.startswith('-x-var-'): ext_vars[rule.name[7:]] = rule.val
			else: raise TemplateError(f'Unrecognized extension rule: {rule.name!r} = {rule.val!r}')

	# Add Subst with extra selectors/prefixes before all matching statements
	st_exts = cs.defaultdict(list) # to dedup prepended selectors
	for sx, ext_list in ext_idx.items():
		for ext in ext_list:
			for st in st_idx[sx]:
				sel_exts, sx_str = st_exts[st._tx_position], ' '.join(sx)
				for s_ext in ext.sels:
					if ext.prefix: s_ext = f'{s_ext} {sx_str}'
					sel_exts.append(f'{s_ext},')
	for pos, sel_exts in st_exts.items():
		sel_exts = sorted(set(sel_exts))
		substs.append(Subst(pos, s='\n'.join(sel_exts) + '\n'))

	# Perform all positional substitutions from "substs"
	css = css_tpl
	for s in sorted(substs, key=lambda s: (s.a, -s.b), reverse=True):
		if s.b < 0: s.b = s.a
		head, tail = css[:s.a], css[s.b:]
		if s.strip_tail: tail = tail.lstrip()
		css = head + s.s + tail

	# Replace all variables set via -x-var-* to "ext_vars"
	for k, v in sorted(ext_vars.items(), key=lambda kv: -len(kv[0])):
		v = v.replace('\\\\', '\ue000').replace('\\', ';').replace('\ue000', '\\')
		css = re.sub( r'(?<=[^-\w])' +
			re.escape(f'-x-var-{k}') + r'(?=[^-\w])', lambda m: v, css )

	if print_diffs:
		if not hasattr(template, 'diff_cmd'):
			template.diff_cmd = 'colordiff'
			try: sp.run([template.diff_cmd, '--help'], stdout=sp.DEVNULL, check=True)
			except OSError: template.diff_cmd = 'diff'
		with tempfile.NamedTemporaryFile(prefix='template.css.') as a,\
				tempfile.NamedTemporaryFile(prefix='generated.css.') as b:
			a.write(css_tpl.encode())
			b.write(css.encode())
			a.flush()
			b.flush()
			sp.run([template.diff_cmd, '-uw', a.name, b.name])

	return css


def template_file(p_tpl, p_dst, verbose=False):
	css_tpl = p_tpl.read_text()
	css = template(css_tpl, print_diffs=verbose)
	p_dst.write_text(css) # no need for tempfile-replace here

def iter_tpl_file_pairs(p_dirs, fn_re, ignore_mtimes=False):
	if isinstance(fn_re, str): fn_re = re.compile(fn_re)
	for p_dir in p_dirs:
		for root, dirs, files in os.walk(p_dir):
			root = pl.Path(root)
			for fn in files:
				if not (m := fn_re.search(fn)): continue
				p_tpl = root / fn
				a, b = m.span(1)
				p_dst = root / (fn[:a] + fn[b:])
				if ( not ignore_mtimes and p_dst.exists()
					and p_dst.stat().st_mtime > p_tpl.stat().st_mtime ): continue
				yield (p_tpl, p_dst)

def main(args=None):
	import argparse
	parser = argparse.ArgumentParser(
		description='Parse/convert all .css.tpl files into .css in a dir tree.')
	parser.add_argument('dir', nargs='*', help='Directory(-ies) to process. Default: current one.')
	parser.add_argument('-e', '--tpl-ext-re',
		metavar='regexp', default=r'(\.tpl).css$',
		help='Regexp to match basename of the template file,'
			' with group 1 to be stripped after templating. Default: %(default)s')
	parser.add_argument('-i', '--ignore-mtimes', action='store_true',
		help='Ignore file modification time check, i.e. always process all templates.')
	parser.add_argument('-v', '--verbose',
		action='store_true', help='List processed files, print diffs.')
	opts = parser.parse_args(sys.argv[1:] if args is None else args)

	p_dirs = list(map(pl.Path, opts.dir or ['.']))
	for p in p_dirs:
		if not p.exists(): parser.error(f'Specified dir not accessible: {p}')

	paths = list(iter_tpl_file_pairs( p_dirs,
		opts.tpl_ext_re, ignore_mtimes=opts.ignore_mtimes ))
	for p_tpl, p_dst in paths:
		if opts.verbose: print('\n' + '-'*10, p_tpl, '->', p_dst)
		template_file(p_tpl, p_dst, verbose=opts.verbose)

if __name__ == '__main__': sys.exit(main())
