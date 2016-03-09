from distutils.spawn import find_executable
import logging as log
import os
import shutil
from subprocess import call
import tempfile


class open_eos(object):
    """An EOS file wrapper that acts like the native `open`.

    Example usage:
        with open_eos('/eos/path/to/file.txt') as f:
            print f.readlines()
    The file will be copied to a local directory, and deleted once the `with`
    context is exited.
    """
    # Name of executable that copies files from EOS to local
    XRDCP = 'xrdcp'
    # Prefix to use when querying EOS
    EOS_PREFIX = 'root://eoslhcb.cern.ch/'

    def __init__(self, path, progress_bar=False):
        """Initialise an open_eos object.

        The bare object is not of much use, as this object is intended to be
        used inside a `with...as` context.
        This initialisation will raise an OSError if the open_eos.XRDCP binary
        cannot be found in the current PATH.

        If progress_bar is True, the xrdcp download progress bar is shown.
        """
        if not find_executable(self.XRDCP):
            raise OSError('Could not find executable {0}'.format(self.XRDCP))
        self.path = path
        self.fname = os.path.basename(self.path)
        self.progress_bar = progress_bar

    def _cleanup(self):
        """Remove temporary directory used to store EOS download."""
        try:
            tmpdir = self.tmpdir
        except AttributeError:
            # Don't need to do anything if the temp dir isn't set
            return
        shutil.rmtree(tmpdir)

    def __enter__(self):
        """Download file from EOS and return a `file` object like `open`."""
        self.tmpdir = tempfile.mkdtemp()
        # Don't need to append the prefix if it's already there
        if self.path.startswith(self.EOS_PREFIX):
            origin = self.path
        else:
            origin = self.EOS_PREFIX + self.path
        destination = os.path.join(self.tmpdir, self.fname)

        cmd = [self.XRDCP, origin, destination]
        if not self.progress_bar:
            cmd.append('--nopbar')
        rtn = call(cmd)
        log.debug('Commmand `%s` exited with code %i', ' '.join(cmd), rtn)
        if rtn > 0:
            self._cleanup()
            # Native `open` raises IOError on file-not-found, follow suit here
            raise IOError('Could not download file {0} from EOS'.format(
                self.path
            ))

        self.fhandle = open(os.path.join(self.tmpdir, self.fname))
        return self.fhandle

    def __exit__(self, type, value, traceback):
        """Delete downloaded file and parent directory."""
        self.fhandle.close()
        self._cleanup()

    def __repr__(self):
        return 'open_eos({0!r})'.format(self.path)
