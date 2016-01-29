import re

from mercurial import cmdutil, hg, error
from hgext import schemes

cmdtable = {}
command = cmdutil.command(cmdtable)

_ = lambda x: x

class ShortRepository(object):
    def __init__(self, url, scheme, templater):
        self.scheme = scheme
        self.templater = templater
        self.url = url
        try:
            self.parts = max(map(int, re.findall(r'\{(\d+)\}', self.url)))
        except ValueError:
            self.parts = 0

    def __repr__(self):
        return '<ShortRepository: %s>' % self.scheme

    def instance(self, ui, url, create):
        url = self.resolve(ui, url)
        return hg._peerlookup(url).instance(ui, url, create)

    def resolve(self, ui, url):
        # Should this use the util.url class, or is manual parsing better?
        try:
            url = url.split('://', 1)[1]
        except IndexError:
            raise error.Abort(_("no '://' in scheme url '%s'") % url)
        parts = url.split('/', self.parts)
        if len(parts) > self.parts:
            tail = parts[-1]
            parts = parts[:-1]
        else:
            tail = ''
        context = dict((str(i + 1), v) for i, v in enumerate(parts))
        return ''.join(self.templater.process(self.url, context)) + tail

@command('expand-scheme', norepo=True)
def expand_scheme(ui, url, **opts):
    """given a repo path, provide the scheme-expanded path
    """
    repo = hg._peerlookup(url)
    if isinstance(repo, schemes.ShortRepository):
        new_repo = ShortRepository.__new__(ShortRepository)
        new_repo.__dict__.update(vars(repo))
        url = new_repo.resolve(ui, url)
    ui.status(url + '\n')
