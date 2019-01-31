#### 

Need to add the markdown readme content here. It'll mostly be about what the local module does and the quirks about Billboards chart site which I think would be useful to share.

#Might need to add this information about appending a new Python related path to look for modules:
>>> import sys 
>>> sys.path.append('/ufs/guido/lib/python')

Solution to create a symlink to the site packages folder which is in the python path
mklink /D link target
#Linux
ln -s /path/to/my/package /path/to/anaconda/env/myenv/lib/python2.7/site-packges/
#WIndows
mklink /D D:\Libraries\Documents\local_python_modules C:\Users\jacks\Anaconda3\lib\site-packages

