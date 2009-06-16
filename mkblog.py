import os
from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string

TEMPLATE_DIRS = ( "templates", )

def main():
    settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS)
    
    print Template(open("test.txt").read()).render(Context())

if __name__ == "__main__":
    main()
