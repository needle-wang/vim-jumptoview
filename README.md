
*Jump to a view's define from url map.*   
*Only work with str style of view at a line,*  
*Supports django and web.py's url.*  

Based on ViMango, but totally different code in the end.  
So maybe say inspired by ViMango.  

Install:

* Put jumptoview.vim in $VIMRUNTIME/plugin  
    a vim package manager like vundle can do it well.

* Put jumptoview.py in $PYTHONPATH  
    e.g.  
    `sudo ln -sf ~/.vim/bundle/vim-jumptoview/plugin/jumptoview.py /usr/local/lib/python2.7/dist-packages/jumptoview.py`

Usage:  
* Type `gO` at a view str line in urls.py:

  * `r'^url/$', 'app.views.func', ...`  
      can jump to `func` in app/views.py

  * `r'^app$', include('app.urls'), ...`  
      can jump to app/urls.py

  * `r'index', direct_to_template, {'template_name': 'app/index.html'}, ...`  
      can jump to templates/app/index.html

No settings are imported and no django modules used.  
If you want to set variable or modify sth.  
the source code is short, see it for more detail.  

Combining with ycm, would be more convenient!

Bugs:
  * can't handle the case that re of one line contained `',` or `",`. 
