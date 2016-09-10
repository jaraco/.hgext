"""
Add git-only tags by tagging with ``--git``.
"""

import contextlib

from mercurial import commands, extensions, scmutil


def wrapper(orig, ui, repo, *names, **opts):
    if opts.get('git'):
        rev = opts.get('rev', '.')
        rev = scmutil.revsingle(repo, rev).hex()
        opener = repo.opener('git-tags', 'a+', atomictemp=True)
        # Mercurial 3.8 compat
        opener = contextlib.closing(opener)
        with opener as file:
            for name in names:
                file.write("%s %s\n" % (rev, name))
    else:
        orig(ui, repo, *names, **opts)

extensions.wrapcommand(commands.table, 'tag', wrapper)

_, options, _ = commands.table['tag']
options.append(('', 'git', None, 'Create a Git-only tag'))
