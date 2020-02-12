#!/usr/bin/python

import pathlib as pl, subprocess as sp, contextlib as cl
import os, sys, signal, select, time


def awf_wrapper(ctx, debounce=0):
	sig_pipe, sig_pipe_w = os.pipe()
	ctx.callback(os.close, sig_pipe)
	ctx.callback(os.close, sig_pipe_w)
	os.set_blocking(sig_pipe_w, False)
	signal.set_wakeup_fd(sig_pipe_w)
	signal.signal(signal.SIGQUIT, lambda sig,frm: None)

	awf_env = os.environ.copy()
	awf_env['GTK_THEME'] = 'clearlooks-phenix-humanity'
	awf = sp.Popen( ['awf-gtk3'], env=awf_env,
		stdin=sp.DEVNULL, stdout=sp.PIPE, stderr=sp.STDOUT,
		preexec_fn=lambda: signal.signal(signal.SIGQUIT, signal.SIG_IGN) )
	ctx.enter_context(awf)
	ctx.callback(awf.terminate)
	os.set_blocking(awf.stdout.fileno(), False)
	awf_out = open(awf.stdout.fileno(), 'rb', 0)

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
				awf.send_signal(signal.SIGHUP)
				print(f'\r                              \n[{ts_str}] ----- reload -----')
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
	opts = parser.parse_args(sys.argv[1:] if args is None else args)

	with cl.ExitStack() as ctx:
		if opts.pid_file.strip():
			pid_file = pl.Path(opts.pid_file)
			pid_file.write_text(f'{os.getpid()}\n')
			ctx.callback(pid_file.unlink, missing_ok=True)

		sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line-buffering
		return awf_wrapper(ctx, opts.reload_debounce)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, lambda sig,frm: sys.exit(0))
	sys.exit(main())
