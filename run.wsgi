# -*- coding: utf-8 -*- 
import sys, os
PROJECT_DIR = '/var/www/sgo'
activate_this = os.path.join(PROJECT_DIR, 'venv/bin', 'activate_this.py')
#exec(activate_this, dict(__file__=activate_this))
sys.path.insert(0, PROJECT_DIR)
#sys.path.insert(0, '/var/www/sgo')
from run import app as application
