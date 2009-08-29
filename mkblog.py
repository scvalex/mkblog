#!/usr/bin/env python

from datetime import datetime
from imp import load_source
from jinja2 import Environment, FileSystemLoader
from jinja2.nodes import Block
import os

SETTINGS = { "INTERESTING_EXTS": ("html", "xml", "rss"),
             "SRC_DIRS": ("src", ),
             "TEMPLATE_DIRS": ("templates", ),
             "DEST_DIR": "blog"}

def read_variable(fn, vn="context"):
    """Return variable from filename"""
    try: return getattr(load_source("mlblf", fn), vn, None)
    except: return None

def makeDestPath(dd):
    try: os.makedirs(dd)
    except: pass # o.makedirs raises if path exists
    return dd

def date(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

def keysort(xs, key, reverse=False):
    ys = xs[:]
    ys.sort(key=lambda x: getattr(x, key, datetime(1970, 1, 1)), reverse=reverse)
    return ys

class Page:
    def __init__(self, filepath, env):
        if not filepath or not env:
            raise Exception("Page constructor needs path to input file and an environment")

        self.filepath = filepath
        self.env = env

        self.uid = os.path.basename(self.filepath)

        c = read_variable(filepath+".py", "context")
        if c:
            for k,v in c.items():
                setattr(self, k, v)
        else:
            print "Warning: No context for %s" % filepath

        self.blocks = []
        try:
            self.blocks = list(self.env.parse(open(filepath).read()).find_all(Block))
            self.blocks = dict([(b.name, b.body[0].nodes[0].data) for b in self.blocks])
        except Exception as e:
            print "Could not get blocks from %s" % filepath
            print "Actual error: ", e

    def write(self, path, more_context = {}):
        t = self.env.get_template(self.uid)
        open(os.path.join(path, self.uid), "w").write(t.render(more_context))

def main():
    print "* Reading settings"
    global SETTINGS
    try:
        ss = read_variable("settings.py", "settings")
        SETTINGS.update(ss)
    except Exception as e:
        print "No settings.py found; using default settings"
        print "Actual error", e

    # splittext includes the dot in the extension
    SETTINGS["INTERESTING_EXTS"] = ["." + e for e in SETTINGS["INTERESTING_EXTS"]]

    env = Environment(loader = FileSystemLoader(SETTINGS["SRC_DIRS"] + SETTINGS["TEMPLATE_DIRS"]))
    env.filters["date"] = date
    env.filters["keysort"] = keysort

    print "* Source: %s" % ", ".join(SETTINGS["SRC_DIRS"])
    ps = [] # Pages
    for sd in SETTINGS["SRC_DIRS"]:
        for dp, dns, fs in os.walk(sd):
            d = dp[len(sd):].lstrip(os.sep) # cut out the top-level dir
            if d.startswith("."):
                continue # ignore dot files/dirs
            for f in fs:
                if os.path.splitext(f)[1] in SETTINGS["INTERESTING_EXTS"]:
                    fp = os.path.join(sd, f)
                    print "    %s" % fp
                    ps.append(Page(filepath = fp, env = env))

    print "* Output: %s" % SETTINGS["DEST_DIR"]
    mega_context = { "pages": ps}
    op = makeDestPath(SETTINGS["DEST_DIR"])
    for p in ps:
        print "    %s" % p.uid
        p.write(path = op,
                more_context = mega_context)

if __name__ == "__main__":
    main()
