#!/usr/bin/python

import pathlib as pl, subprocess as sp, contextlib as cl
import os, sys, signal, select, time, errno


def run_tpl_rebuild(tpl_script, tpl_dir):
	for n in range(10):
		try: proc = sp.run([tpl_script, tpl_dir])
		except OSError as err:
			if err.errno != errno.ETXTBSY: raise
			time.sleep(0.1) # exec while file is being updated - retry a few times
			continue
		else: return proc.returncode == 0
		break
	return False

def awf_wrapper(ctx, debounce=0, rebuild_templates=False):
	sig_pipe, sig_pipe_w = os.pipe()
	ctx.callback(os.close, sig_pipe)
	ctx.callback(os.close, sig_pipe_w)
	os.set_blocking(sig_pipe_w, False)
	signal.set_wakeup_fd(sig_pipe_w)
	signal.signal(signal.SIGQUIT, lambda sig,frm: None)
	signal.signal(signal.SIGHUP, lambda sig,frm: None)

	awf_env = os.environ.copy()
	awf_env['GTK_THEME'] = 'clearlooks-phenix-humanity'
	awf = sp.Popen( ['awf-gtk3'], env=awf_env,
		stdin=sp.DEVNULL, stdout=sp.PIPE, stderr=sp.STDOUT,
		preexec_fn=lambda: signal.signal(signal.SIGQUIT, signal.SIG_IGN) )
	ctx.enter_context(awf)
	ctx.callback(awf.terminate)
	os.set_blocking(awf.stdout.fileno(), False)
	awf_out = open(awf.stdout.fileno(), 'rb', 0)

	if rebuild_templates:
		tpl_dir = pl.Path(__file__).parent
		tpl_script = str(tpl_dir / 'css-templater.py')
		if '/' not in tpl_script: tpl_script = './' + tpl_script

	line, s = '', select.epoll()
	ctx.callback(s.close)
	s.register(sig_pipe, select.EPOLLIN)
	s.register(awf.stdout.fileno(), select.EPOLLIN)

	reload_ts = None
	while True:
		for fd, ev in s.poll():
			ts = time.time()
			ts_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

			if fd == sig_pipe:
				sig = os.read(fd, 1)
				if reload_ts and ts - debounce < reload_ts: continue
				reload_ts = ts
				print(f'\r                              \n[{ts_str}] ----- reload -----')
				if rebuild_templates and not run_tpl_rebuild(tpl_script, tpl_dir):
					print(f'[{ts_str}] --- WARNING: template-rebuild script failed')
				awf.send_signal(signal.SIGHUP)
				continue
			else:
				out = awf_out.readline().decode()
				if not out: return
				line += out

			if not line.endswith('\n'): continue
			if not (line := line.strip()): continue
			print(f'[{ts_str}] {line}')
			line = ''


def main(args=None):
	import argparse
	parser = argparse.ArgumentParser(
		description='Run awf-gtk3 with an easy reload'
			' on ^\ via terminal and filtered/timestamped output.')
	parser.add_argument('-p', '--pid-file',
		metavar='file', default='/tmp/awf-gtk3.pid',
		help='Pid file path to use. Empty - disable. Default: %(default)s')
	parser.add_argument('-d', '--reload-debounce',
		type=float, metavar='sec', default=2,
		help='Debounce timeout for reload signal(s), in seconds. Default: %(default)ss')
	parser.add_argument('-t', '--rebuild-templates', action='store_true',
		help='Rebuild .css files from .tpl.css via css-templater.py script on reload signal.')
	opts = parser.parse_args(sys.argv[1:] if args is None else args)

	with cl.ExitStack() as ctx:
		if opts.pid_file.strip():
			pid_file = pl.Path(opts.pid_file)
			pid_file.write_text(f'{os.getpid()}\n')
			ctx.callback(pid_file.unlink, missing_ok=True)

		sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line-buffering
		return awf_wrapper(ctx, opts.reload_debounce, opts.rebuild_templates)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, lambda sig,frm: sys.exit(0))
	sys.exit(main())
