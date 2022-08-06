### 3DSMAX Style Renamer for AutodeskMaya

A renamer/replace tool based on the 3dsmax renamer.

This tool support maya undo. (Ctrl + Z)  
There are some limitations from the maya naming system, you cannot have a number prefix, or duplicated names in the same hierarchy.  
You can rename maya non-DAG Objects, like shading nodes, etc, from the outliner.  
The auto-padding feature works reading the selection order, if you want the same results on padding, just select items in the same order. (Select Top item, shift-click and select bottom item)

![renamer screenshot](https://github.com/MaxRocamora/MayaRenamer/blob/master/renamer/img/renamer.png?raw=true>)

### Install

Maya 2022+ *Python3 Only*

Download and add the folder to your PYTHONPATH environment variable or copy into your maya/scripts folder.

PYTHONPATH += *'D:\directory\renamer'*

### Run

Create a shelf button with this python command:
```python
import renamer.main as renamer
renamer.load()
```
