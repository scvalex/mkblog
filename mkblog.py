#!/usr/bin/env python

import os
import django.conf
from django.template import Context, Template
from django.template.loader import render_to_string

TEMPLATE_DIRS = ( "templates", )
SRC_DIRS = ( "src", )
DEST_DIR = "blog"

def makeDestPath(p):
    """ Ensure that the path exists in the output directory and return it """
    p = os.path.join(DEST_DIR, p)
    try: os.makedirs(p)
    except: pass # os.makedirs raises error if path exists
    return p

def main():
    try:
        import settings
        global TEMPLATE_DIRS, SRC_DIRS, DEST_DIR
        TEMPLATE_DIRS = getattr(settings, "TEMPLATE_DIRS", TEMPLATE_DIRS)
        SRC_DIRS = getattr(settings, "SRC_DIRS", SRC_DIRS)
        DEST_DIR = getattr(settings, "DEST_DIR", DEST_DIR)
    except:
        print "No settings.py found; using default settings."
    
    django.conf.settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS)

    for sd in SRC_DIRS:
        for dp, dns, fs in os.walk(sd):
            p = dp[len(sd):].lstrip(os.sep) # cut out the top-level dir
            p = makeDestPath(p) # prepend the dest dir and ensure path exists
            print "%s: %s" % (p, ", ".join(fs))
            for f in fs:
                open(os.path.join(p, f), "w").write(Template(open(os.path.join(dp, f)).read()).render(Context()))

if __name__ == "__main__":
    main()
