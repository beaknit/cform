cform
=====

A sublime plugin for CloudFormation

# Setup

CForm is now available via the Sublime Text package control.  See https://packagecontrol.io/

# Use

1.  Open a new file in Sublime
2.  Set the file type to `Cloudformation` by either selecting from the menu in the bottom-right corner of the ST window or hitting Cmd|Ctrl + Shift + P to open the Command Palatte and typing `SetSyntax: CloudFormation`.
3.  Type `start` - a CloudFormation template scaffold will appear
4.  Under each section, type the thing you're trying to make (eg, `parameter`, `output`, etc) and it will populate the text for you.  
5.  Tab through the different fields and fill in your values
6.  Save it with the extension `cform`, `template` or `cloudformation` and run it through the CloudFormation console
7.  Profit

# Update the snippets

## Requirements

1. You will need ```Python 2.7.10+```
2. Run ```pip install -r build/requirements.txt```

## Updating the docs from the latest

1. Go inside the build dir from the comand line
2. Run ```rm -rf *.pyc && python build-snippets.py```
