#!/usr/bin/env python

#Script copied from
#Basic Django deployment with virtualenv, fabric, pip and rsync - Colin Copeland
#http://www.caktusgroup.com/blog/2010/04/22/basic-django-deployment-with-virtualenv-fabric-pip-and-rsync/

import os, sys, subprocess

#check if the script is run in a virtual environment
if "VIRTUAL_ENV" not in os.environ:
    sys.stderr.write("$VIRTUAL_ENV not found.\n\n")
    parser.print_usage()
    sys.exit(-1)
    
#If we are in a virtual environment
virtualenv = os.environ["VIRTUAL_ENV"]
file_path = os.path.dirname(__file__)
subprocess.call(["pip", "install", "-E", virtualenv, "--requirement",
                 os.path.join(file_path, "requirements/apps.txt")])
