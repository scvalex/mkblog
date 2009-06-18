import os
from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string

TEMPLATE_DIRS = ( "templates", )
SRC_DIRS = ( "src1", "src2", )
DEST_DIR = "blog"

def makeDestPath(p):
    """ Ensure that the path exists in the output directory and return it """
    p = os.path.join(DEST_DIR, p)
    try: os.makedirs(p)
    except: pass # os.makedirs raises error if path exists
    return p

def main():
    settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS)

    for sd in SRC_DIRS:
        for dp, dns, fs in os.walk(sd):
            p = dp[len(sd):].lstrip(os.sep) # cut out the top-level dir
            p = makeDestPath(p) # prepend the dest dir and ensure path exists
            print "%s: %s" % (p, ", ".join(fs))
            for f in fs:
                open(os.path.join(p, f), "w").write(Template(open(os.path.join(dp, f)).read()).render(Context()))

if __name__ == "__main__":
    main()
