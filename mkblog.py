import os
from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string

TEMPLATE_DIRS = ( "templates", )
SRC_DIRS = ( "src1", "src2", )
DEST_DIR = "blog"

def pathComponents(p):
    """ pathComponents(p) -> [dir1, dir2, ..., filename]
    """
    ds = []
    while p:
        ds.append(os.path.basename(p))
        p = os.path.dirname(p)
    ds.reverse()
    return ds

def makeDestPath(ds):
    """ Ensure that the path exists in the output directory and return it
    """
    p = os.path.join(*([DEST_DIR] + ds))
    try:
        os.makedirs(p)
    except:
        pass # os.makedirs raises error if path exists
    return p

def main():
    settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS)

    for sd in SRC_DIRS:
        for dp, dns, fs in os.walk(sd):
            rp = pathComponents(dp)[1:] # Break the path into components and drop the first dir
            p = makeDestPath(rp)
            print "%s: %s" % (str(rp), ", ".join(fs))
            for f in fs:
                open(os.path.join(p, f), "w").write(Template(open("test.txt").read()).render(Context()))

if __name__ == "__main__":
    main()
