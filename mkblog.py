#!/usr/bin/env python

import os
import django.conf
from django.template import Context, Template
from django.template.loader import render_to_string
import sys

INTERESTING_EXTS = ( "html", "xml", "rss" )
TEMPLATE_DIRS = ( "templates", )
SRC_DIRS = ( "src", )
DEST_DIR = "blog"

def getContext(f):
    """ Read associated config file and return read Context. """
    c = {}
    try:
        config_dir = os.path.abspath(os.path.dirname(f))
        module_name = os.path.splitext(os.path.basename(f))[0] # name without extension
        sys.path = [config_dir] + sys.path
        c = __import__(module_name).context
        sys.path = sys.path[1:]
    except:
        print "No associated config for %s" % f
    return Context(c)

class BlogEntry:
    def __init__(self, filepath):
        if not filepath:
            raise Exception("No file given.  Comitting suicide.")
        self.filepath = filepath
        self.context = getContext(filepath)

    def makeDestPath(self, dd):
        """ Ensure that the path exists in the output directory and return it. """
        p = os.path.join(dd, os.path.basename(self.filepath))
        try: os.makedirs(os.path.dirname(p))
        except: pass # os.makedirs raises error if path exists
        return p

    def write(self, path, moreContext = {}):
        """ write(path, moreContext)

        Write the entry to file path extending the existing context with moreContext.
        """
        open(path, "w").write(Template(open(self.filepath).read()).render(self.context.update(Context(moreContext))))

def main():
    print "* Reading settings"
    # Settings stuff
    try:
        sys.path = ["."] + sys.path # load modules from cur dir
        import settings
        global TEMPLATE_DIRS, SRC_DIRS, DEST_DIR, INTERESTING_EXTS
        INTERESTING_EXTS = getattr(settings, "INTERESTING_EXTS", INTERESTING_EXTS)
        TEMPLATE_DIRS = getattr(settings, "TEMPLATE_DIRS", TEMPLATE_DIRS)
        SRC_DIRS = getattr(settings, "SRC_DIRS", SRC_DIRS)
        DEST_DIR = getattr(settings, "DEST_DIR", DEST_DIR)
    except:
        print "No settings.py found; using default settings."

    # o.p.splitext includes the dot in the extension
    INTERESTING_EXTS = ["." + e for e in INTERESTING_EXTS]
    
    django.conf.settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS)

    # Go through dirs, process files, etc.
    print "* Source: %s" % ", ".join(SRC_DIRS)
    es = []
    for sd in SRC_DIRS:
        for dp, dns, fs in os.walk(sd):
            p = dp[len(sd):].lstrip(os.sep) # cut out the top-level dir
            if p.startswith("."):
                continue # ignore dot files/dirs
            for f in fs:
                if os.path.splitext(f)[1] in INTERESTING_EXTS:
                    fp = os.path.join(sd, f)
                    print "    %s" % fp
                    es.append(BlogEntry(filepath = fp))
    print "* Output: %s" % DEST_DIR
    for e in es:
        op = e.makeDestPath(DEST_DIR)
        print "    %s" % op
        e.write(path = op,
                moreContext = { "entries": es })

if __name__ == "__main__":
    main()
