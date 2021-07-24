import re
import datetime

from pnbp.models import Notebook, Note
from pnbp.wrappers import pass_nb

"""
	- #todo a task to record _complete and perm remove w/ #complete
	- doesn't require todo tag to #complete
	(&& -> record to nb/_complete.md under datestamp YYYY-MM-DD section)

	- [x] my task item to record and reset to incomplete
	->
	- [ ] my task item to record and reset to incomplete
	(&& -> record to nb/_complete.md under datestamp YYYY-MM-DD section)

	- [x] reoccuring parameterized task w/ (param1: 10units,param2:blahblah,)
	-> record _complete w/ param 
	- [ ] reoccuring parameterized task w/ (param1: ,param2: ,)
	(&& -> record to nb/_complete.md under datestamp YYYY-MM-DD section, with 
	additional param "@" timestamp collected - [x] task (p1:hello,@:12:33:58))
"""

TASK_INCOMPLETE = r'(^|\s)(-\s\[\s\]\s)(.*)'
TASK_COMPLETE = r'(^|\s)(-\s\[x\]\s)(.*)'

TASK_VARS = r'\((.+:+.+)\)'



"""
"""
def md_task_uncheck(matchobj):
	""" str replacement func """
	t = matchobj.group(3).strip().replace(r'\t', ' ')

	if matchobj.group(1) == '\t':
		return f'\t- [ ] {t}'

	return f'- [ ] {t}'

def md_reoccurring_task_uncheck(matchobj):
	""" str replacement func """
	return f'- [ ] {t}'



# @pass_nb
def record_complete_tasks(c_tasks:list=[], nb: Notebook=None):
	""" called by other tasks fnxs (not a command)
		initialize nb/_complete.md -> 
		record c_tasks at YYYY-MM-DD section 

	:param list c_tasks: complete tasks e.g. ['- [x] clean room', '- [x] laundry', '- [x] some fake task']
	:param nb: explicitely expecting a notebook instance 
	"""
	COMPL_NOTE = nb.config.get('COMPL_NOTE')

	if not COMPL_NOTE:
		COMPL_NOTE = '_complete'

	if not nb.get(COMPL_NOTE):
		nb.generate_note(COMPL_NOTE, "")

	if c_tasks:
		fin_item_str = '\n'.join(c_tasks)

	new_day = True
	d_today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
	repl_section = ''
	for i, s in enumerate(nb.notes[COMPL_NOTE].sections):
		if re.match(d_today, s):
			repl_section = s + '\n' + fin_item_str
			_md_out = nb.notes[COMPL_NOTE].sections.copy()
			_md_out[i] = repl_section

			nb.notes[COMPL_NOTE].md_out = '\n\n--- \n'.join(_md_out)
			nb.notes[COMPL_NOTE].save(nb)
			new_day = False

	if new_day:
		_md_out = nb.notes[COMPL_NOTE].sections.copy()
		_md_out.insert(1, f'{d_today}\n{fin_item_str}')
		nb.notes[COMPL_NOTE].md_out = '\n\n--- \n'.join(_md_out)
		nb.notes[COMPL_NOTE].save(nb)


@pass_nb
def _uncheck_complete_tasks(note: Note=None, nb=None):
	""" - [x] taskname -> - [ ] taskname 
		(&& -> nb/_complete.md)
	"""
	p = re.compile(TASK_COMPLETE)

	ns = note.md.splitlines()

	complete_tasks = []
	for i, li in enumerate(ns):
		if p.search(li):
			complete_tasks.append(li)
			ns[i] = p.sub(md_task_uncheck, li)

	if complete_tasks:
		record_complete_tasks(complete_tasks, nb)

		note.md_out = '\n'.join(ns)
		note.save(nb)


@pass_nb
def _complete_complete_tasks(note: Note=None, nb=None):
	""" - todo #complete -> ... (remove line)
		 (&& -> nb/_complete.md)
	"""
	COMPL_TAG = nb.config.get('COMPL_TAG')

	if not COMPL_TAG:
		COMPL_TAG = '#complete'

	ns = note.md.splitlines()

	p = re.compile(COMPL_TAG)

	complete_tasks = []
	for i, li in enumerate(ns):
		if p.search(li):
			complete_tasks.append(li)

	if complete_tasks:
		record_complete_tasks(complete_tasks, nb=nb)

		_md_out = note.md
		for t in complete_tasks:
			# print("**********\n",t, _md_out)
			# print(re.findall(t, _md_out))
			# _md_out = re.sub(t, '', _md_out) # this was working.. -> 
			_md_out = _md_out.replace(t, '') # more explicit 
			# print("-------->\n", _md_out)

		note.md_out = _md_out
		note.save(nb)


@pass_nb
def _reset_reoccurring_param_tasks(note: Note=None, nb=None):
	""" - [x] taskname (var1: x, ) -> - [ ] taskname (var1: , )
		 (&& -> nb/_complete.md)
	"""
	p = re.compile(TASK_COMPLETE)
	p2 = re.compile(TASK_VARS)

	ns = note.md.splitlines()

	complete_tasks = []
	for i, li in enumerate(ns):

		if p.search(li) and (m := p2.search(li)):

			_vars = m.group(0).strip('(').strip(')').split(',')
			_vars = [v for v in _vars if not v == ' ']
			print('_vars', _vars)

			_key = li.strip('-[x] ').split('(')[0].strip()
			print('_key', _key)

			_t = datetime.datetime.strftime(datetime.datetime.now(), '%X')
			print('_t', _t)
			
			_keys = [v.split(':')[0].strip() for v in _vars if v.split(':')[0].strip()]
			print('_keys', _keys)

			_vals = [v.split(':')[1:][0].strip() for v in _vars if len(v.split(':')) > 1]
			print('_vals', _vals)

			d = {x:_vals[i] for i, x in enumerate(_keys)}
			print('d', d)

			if not '@' in d.keys():
				d.update({'@': _t})
			if d['@'] == '':
				d['@'] = _t

			print('d', d)
			print('-> exit to api')
			# ... todo
			# ... -> exit to api
			

			# formatting reset task (e.g. ->"- [ ] taskname (var1: , )")
			reset_out = ''.join([f'{k}: ,' for k in _keys])
			reset_out = '(' + reset_out.strip(',') + ')'
			_reset_out_str = p.sub(md_task_uncheck, li)
			_reset_out_str = p2.sub(reset_out, _reset_out_str)

			# -> format _complete task (w/ e.g. added timestamp "@:07:30") above
			complete_out = ''.join([f'{k}:{v}, ' for k,v in d.items()]).strip()
			complete_out = f'- [x] {_key} ({complete_out})'
			print('complete_out', complete_out)

			complete_in = li # carrying w/ us for str.replace() below
			complete_tasks.append([complete_in, complete_out, _reset_out_str])
			

	if complete_tasks:
		# -> reset task & vars
		# -> record to _complete
		_md_out = note.md
		for t in complete_tasks:
			c_in, c_out, r_out = t
			_md_out = _md_out.replace(c_in, r_out)
		
		note.md_out = _md_out
		note.save(nb)
		
		record_complete_tasks([t[1] for t in complete_tasks], nb)



""" commands -> cli
"""
@pass_nb
def _nb_task_settle(nb=None):
	""" #tasks -> nb/_complete.md
		(1) collect and reset parameterized tasks
		(2) ^^ for - [x] standard tasks
		(3) ^^ and remove - bullet-only todos marked #complete
	"""
	TASKS_TAG = nb.config.get('TASKS_TAG')

	if not TASKS_TAG:
		TASKS_TAG = '#tasks'

	tasked = [n for n in nb.get_tagged(TASKS_TAG)]
	print([n.name for n in tasked])

	for n in tasked:
		_reset_reoccurring_param_tasks(nb.get(n), nb) 	# fresh get from nb.notes dict is
		_uncheck_complete_tasks(nb.get(n), nb) 			# ensuring our note n being passed
		_complete_complete_tasks(nb.get(n), nb) 		# is holding curr saved .md


@pass_nb
def _collect_tasks_note(nb=None):
	""" if #tasks -> [[tasks]]
		(link all notes containg "#tasks" to nb/tasks.md)
	"""
	TASKS_TAG = nb.config.get('TASKS_TAG')
	TASKS_NOTE = nb.config.get('TASKS_NOTE')

	if not TASKS_TAG:
		TASKS_TAG = '#tasks'
	if not TASKS_NOTE:
		TASKS_NOTE = 'tasks'

	tasked = [n for n in nb.get_tagged(TASKS_TAG)]
	ns = '\n'.join([f'[[{n.name}]]' for n in tasked])

	nb.generate_note(TASKS_NOTE, md_out=ns, overwrite=True, pnbp=True)



"""
"""
@pass_nb
def _move_sched_tasks_today(nb=None):
	""" """
	tasked = [n for n in nb.get_tagged(TASKS_TAG)]
	for n in tasked:
		for li in n.md.splitlines():
			if '#sched' in li and li.strip().startswith('-'):
				pass


# @pass_nb
def _parse_today_note(nb=None):
	""" ... under development """
	n = nb.get('TODAY')
	# print(n.sections)
	td = datetime.datetime.today().date()
	td = datetime.datetime.strftime(td, '%Y-%m-%d')
	print(td)

	has_today = False
	for s in n.sections:
		# print(s)
		if s.strip().startswith(td):
			has_today = True
			j = '\n'.join([x for x in s.split('\n') if not x.startswith('-')])
			print(j) #journal content
			# -> ^^ what do w/ - ?
			# for x in n.md.splitlines():
			# 	if x.startswith('-'):
			# 		pass
			# print(s)

	if not has_today:
		i = 0 if not n.header else 1
		ns = n.sections.copy()
		ns.insert(i, td)
		n.md_out = '\n\n--- \n'.join(ns)
		n.save(nb)




if __name__ == '__main__':
	pass
	# nb = Notebook()
	# parse_today_note(nb)









