#!/bin/env python3

import subprocess
import getpass
import json
import os
import pathlib
import logging
import sys

logger = logging.getLogger('qndrdp')

class qndrdp:
    def __init__(self):
        self.configfile = os.path.join(pathlib.Path.home(), '.config', 'qndrdp', 'config.json')
        os.makedirs(os.path.dirname(self.configfile), exist_ok=True)

    def run(self):
        self._get_values()
        self._run_yad()
        self._run_freerdp()
        self._save_config()

    def _set_host_and_domain(self, err):
        logger.error('config file missing or malformed, '+str(err))
        # start dialog for host/domain selection, run _save_config
        raise NotImplementedError

    def _get_values(self):
        try:
            with open(self.configfile, 'r') as fh:
                filecontent = fh.read()
        except FileNotFoundError as err:
            self._set_host_and_domain(err)
        try:
            jsondata = json.loads(filecontent)
            self.rdpdomain = jsondata['rdpdomain']
            self.rdphost = jsondata['rdphost']
        except (KeyError, ValueError, AttributeError, TypeError) as err:
            self._set_host_and_domain(err)
        try:
            self.rdpuser = jsondata['rdpuser']
            self.focusfield = 2
        except KeyError:
            self.focusfield = 1
            self.rdpuser = ''

    def _run_yad(self):
        command = ['yad']
        command.append('--title')
        command.append('qndrdp')
        command.append('--form')
        command.append('--field')
        command.append('Benutzername')
        command.append(self.rdpuser)
        command.append('--field')
        command.append('Passwort:H')
        command.append('--focus-field')
        command.append(str(self.focusfield))

        results = subprocess.run(command, stdout=subprocess.PIPE)
        entered_data = results.stdout.rstrip().decode('utf-8')
        self.rdpuser = entered_data.split('|')[0]
        self.rdppassword = entered_data.split('|')[1]

    def _run_freerdp(self):
        localuser = getpass.getuser()
        command = ['xfreerdp']
        command.append('/f')
        command.append('/multimon')
        command.append('/bpp:16')
        command.append('/cert-ignore')
        command.append('/gfx')
        command.append('/drive:media,/run/media/'+localuser)
        command.append('/d:'+self.rdpdomain)
        command.append('/v:'+self.rdphost)
        command.append('/u:'+self.rdpuser)
        command.append('/p:'+self.rdppassword)
        subprocess.run(command)

    def _save_config(self):
        config = {}
        config['rdpuser'] = self.rdpuser
        config['rdpdomain'] = self.rdpdomain
        config['rdphost'] = self.rdphost
        with open(self.configfile, 'wb') as fh:
            filecontent = json.dumps(config)
            fh.write(filecontent.encode('utf-8'))


if __name__ == '__main__':
    gui = qndrdp()
    gui.run()
