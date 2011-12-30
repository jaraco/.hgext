import mercurial.commands

def preupdatehook(ui, repo, parent1=None, **kwargs):
	start_changeset = repo[None].parents()[0]
	changeset = repo[parent1]
	start = start_changeset.node().encode('hex')
	stop = changeset.node().encode('hex')
	my_ui = MyUI()
	try:
		mercurial.commands.status(my_ui, repo, rev=[start, stop], include=['setup.py'])
	except Exception:
		pass
	if my_ui: print("setup.py changed; consider updating dependencies")

class MyUI(list):
	quiet = False
	def write(self, *args, **kwargs):
		self.append((args, kwargs))

def reposetup(ui, repo):
	ui.setconfig('hooks', 'preupdate.setupdated', preupdatehook)
