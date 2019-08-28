# random
##### Just some random scripts
This repo has some of the scripts that I write.  I share them for anyone to:
* Use - they work just fine as far as I know
* Look at as examples of how a certain something _might_ be done
* Sigh / laugh at (Note - please let me know if there's a much easier way to so something)

### So far...
##### djargs
This is a Python 3 module which does all the heavy lifting for processing and validating command line arguments.  It uses a configuration file to define the allowed arguments and rules to apply to them.

**Excerpt from the config file** shows the available properties of defined arguments:
```# valid 'fields' are:
#
#   description : string, description used in help REQUIRED
#   type : string, one of "string, int, float, date", optional (default "none")
#   delimiter: list of strings used to delimiter multiple values for the field, optional, (default no delimmiter)
#   regex : a regex pattern to match when type is "string", optional (default ".*" except for type 'date' - see below)
#   unique : bool, whether the parameter must be specified at most once. optional (default False)
#   default: list, if parameter is not specified, use this value, optional.  Applied after dependancies and requirements etc, but before rules.
#   required : bool, whether the parameter is required. optional (default False)
#   required_unless : list, negate requirement if *one or more* other parameters are specified (implies 'required = true'), optional
#   depends : list, parameters which must *all* also be specified with this one, optional
#   exclusive_of : lits, parameters *any* of which must not also be specified, optional
#   help : string, text used in extended help REQUIRED
#   rules : list of strings, each of which will be evaluated as ("parameter value" rule), optional. See below.


#   the simplest parameter takes this form:

#   "-p": {
#       "description": "example parameter",
#       "help": "help for example paramter"
#   }
```

I use it in my project 'pyngctl' (which is also why I started writing it) which is a command line tool for interacting with Nagios and CheckMK. **Note** I know there's a standard module for Python for *arg*ument *pars*ing ;). There's a **readme.md** in that repo, but if you're familiar with Python it hopefully makes sense when you read the code.

##### djtable
I wrote this because I wanted an easy way to display CSV data in a terminal as a table.  It takes input from STDIN and tries to display the data as a table.  Arguments allow you to specify the delimiter, whether to make the first row a header, the last row a footer and also the style.  A minimum and maximum number of rows needed to determine the maximum column widths have defaults but can also be specified
```-d=<delim>, d=<delim>   delimter to use for columns in each line; default is ;

-h, h                   first data line contains column header names, use default round style
-h=style, h=style       first data line contains column header names, use specified style

-f, f                   last data line contains footer data, use default round style
-f=style, f=style       last data line contains footer data, use specified style

-r=<style>, r=<style>   row style, default light

-t=<style>, t=<style>   top style when no header specified, default round

-e=<style>, e=<style>   end style when no footer specified, default round

--ascii, -a a           draw all table elements using simple ascii

--noerrors, -n, n       don't report data input errors
```
'style' can be 'light', 'bold', 'round' or 'ascii', depending on the table part (eg. a row can't be 'round')

It works with Python 2, so it could probably be better (my original version was for Python 3, but I only had Python 2 where I wanted to use it).

*to be continued*
