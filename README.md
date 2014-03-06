cform
=====

A sublime plugin for CloudFormation

# Setup

To use, cd to your `Sublime Text 2/Packages/User` dir and clone this repo.  The location of the User Packages directory for various operating systems is: http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory .

To remove, simply rm -rf the `cform` directory that was created by the clone.

# Use

1.  Open a new file in Sublime
2.  Set the file type to `Cloudformation`
3.  Type `start` - a CloudFormation template scaffold will appear
4.  Under each section, type the thing you're trying to make (eg, `parameter`, `output`, etc) and it will populate the text for you.  
5.  Tab through the different fields and fill in your values
6.  Save it with the extension `cform`, `template` or `cloudformation` and run it through the CloudFormation console
7.  Profit

