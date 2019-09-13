# random
##### Just some random scripts
This repo has some of the scripts that I write.  I share them for anyone to:
* Use - they work just fine as far as I know
* Look at as examples of how a certain something _might_ be done
* Sigh / laugh at (Note - please let me know if there's a much easier way to so something)

### So far...
#### args2arr (demo)
This is "args to array" in Bash - it parses command line arguments and provides 2 index matched arrays of all the arguments and all the values (if specified).  It can also check if provided arguments are 'allowed'. If you want to use it you just need the function 'parseArgs' with the 'allowedArgs' and 'allowAllArgs' variables set appropriately, the rest is just for demo or testing.

*Eample*
```
└─ᗒ ./args2arr -b=1 -c -d 44 -s='-Some more text' --douglas=42
Arg -b, value 1
Arg -c, value None_found
Arg -d, value 44
Arg -s, value -Some more text
Arg --douglas, value 42
```
Can accept multiple arguments as a string as such for -abc:
```
└─ᗒ ./args2arr -abc 5 -def=10 --long 99 -d 1 -t=2 --last=test
Arg a, value None_found
Arg b, value None_found
Arg c, value 5
Arg def, value 10
Arg long, value 99
Arg d, value 1
Arg t, value 2
Arg last, value test
```
Note: If an argument is more than a single character it must be preceeded with '--'. For example '--help' is a single argument, but '-help' is the same as '-h -e -l -p'


Edit the variables in the function to set the acceptable arguments or override checking. For example, with checking enabled and "('a' 'b' 'x' 'help')" set as acceptable arguments:
```
└─ᗒ ./args2arr -ab -x=3 --help 
Arg a, value None_found
Arg b, value None_found
Arg x, value 3
Arg help, value None_found

└─ᗒ ./args2arr -ab -x=3 --help -s
Invalid parameter 's'
1 errors found
```

Disable checking by scripts by exporting ARGS2ARR_ALL=1 :
```
└─ᗒ export ARGS2ARR_ALL=1

└─ᗒ ./args2arr -ab -x=3 --help -s
Arg a, value None_found
Arg b, value None_found
Arg x, value 3
Arg help, value None_found
Arg s, value None_found
```


#### djargs
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

I use it in my project 'pyngctl' (which is also why I started writing it) which is a command line tool for interacting with Nagios and CheckMK. **Note** I know there's a standard module for Python for *arg*ument *pars*ing ;). There's a **readme.md** in my pyngctl repo, but if you're familiar with Python it hopefully makes sense when you read the code.

#### gd_dns
This is for updating a DNS record with GoDaddy with the current WAN IP of your router.  You'll need to get an API key and password to use it.  It's meant to run as a cron job so if your public IP changes your DNS record is updated with the new IP.
There's a seperate config file which has the API key and password so that access to that can be restricted via permissions if needed.

#### djtable
I wrote this because I wanted an easy way to display CSV data in a terminal as a table.  It takes input from STDIN and tries to display the data as a table.  Arguments allow you to specify the delimiter, whether to make the first row a header, the last row a footer and also the style.  

**Note** This script reads the entire input into memory - it will ~~probably~~ cause 'issues' if you feed it too much; it's intended to display a 'sensible' amount of data, not an entire 2GB log file.
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

*Examples*
```
└─ᗒ cat example-data.txt | djtable 
╭────┬──────┬───────────┬────────────────────┬─────────────────────────────────────────────╮
│id  │state │host_name  │service_description │service_alert                                │
│143 │2     │dc01-web01 │uptime_status       │CRIT: Host uptime is 0:30                    │
│145 │2     │dc01-web02 │                    │CRIT: Host uptime is 0:50 and some more info │
│146 │2     │dc03-web01 │uptime_status       │CRIT: Host uptime is 0:25                    │
│149 │2     │dc03-web04 │uptime_status       │CRIT: Host uptime is 0:15                    │
│145 │2     │dc01-web02 │uptime_status       │CRIT: Host uptime is 0:50 and some more info │
│145 │2     │dc01-web02 │                    │CRIT: Host uptime is 0:50 and some more info │
└────┴──────┴───────────┴────────────────────┴─────────────────────────────────────────────┘

└─ᗒ cat example-data.txt | djtable -h
╭────┬──────┬───────────┬────────────────────┬─────────────────────────────────────────────╮
│id  │state │host_name  │service_description │service_alert                                │
├────┼──────┼───────────┼────────────────────┼─────────────────────────────────────────────┤
│143 │2     │dc01-web01 │uptime_status       │CRIT: Host uptime is 0:30                    │
│145 │2     │dc01-web02 │                    │CRIT: Host uptime is 0:50 and some more info │
│146 │2     │dc03-web01 │uptime_status       │CRIT: Host uptime is 0:25                    │
│149 │2     │dc03-web04 │uptime_status       │CRIT: Host uptime is 0:15                    │
│145 │2     │dc01-web02 │uptime_status       │CRIT: Host uptime is 0:50 and some more info │
│145 │2     │dc01-web02 │                    │CRIT: Host uptime is 0:50 and some more info │
╰────┴──────┴───────────┴────────────────────┴─────────────────────────────────────────────╯

└─ᗒ cat example-data.txt | djtable -h -a
+----+------+-----------+--------------------+---------------------------------------------+
|id  |state |host_name  |service_description |service_alert                                |
+----+------+-----------+--------------------+---------------------------------------------+
|143 |2     |dc01-web01 |uptime_status       |CRIT: Host uptime is 0:30                    |
|145 |2     |dc01-web02 |                    |CRIT: Host uptime is 0:50 and some more info |
|146 |2     |dc03-web01 |uptime_status       |CRIT: Host uptime is 0:25                    |
|149 |2     |dc03-web04 |uptime_status       |CRIT: Host uptime is 0:15                    |
|145 |2     |dc01-web02 |uptime_status       |CRIT: Host uptime is 0:50 and some more info |
|145 |2     |dc01-web02 |                    |CRIT: Host uptime is 0:50 and some more info |
+----+------+-----------+--------------------+---------------------------------------------+
```

#### e2d
e2d is 'epoch to date'; it's for converting Unix timestamps in log files or such and displaying them as a date and time string. It takes input from STDIN and any 10 digit integer gets replaced with a date and time string, and outputs the result of each line to STDOUT.

*Example*
```
└─ᗒ cat testdata.log 
1232343567,some log line with valid date,user 1,2
1232343667,some other line with valid date,user 2,2
12323437677,some other with invalid date; log lines,user,2
1232343767,some log line with valid date,user 5,2
1232343,some log line with invalid date,user,2

└─ᗒ cat testdata.log | e2d
2009-01-19 05:39:27,some log line with valid date,user 1,2
2009-01-19 05:41:07,some other line with valid date,user 2,2
12323437677,some other with invalid date; log lines,user,2
2009-01-19 05:42:47,some log line with valid date,user 5,2
1232343,some log line with invalid date,user,2
```

#### wsv.py
wsv.py is "what seperated values". It tries to work out what the delimiter is in cvs type file when it's not known. It takes input from STDIN, and has a minimum and maximum number of lines to look at to come up with an answer, or not.

This is a work in progress, and will only work where the input data has a consistent number of fields for the sample size, nor will it respect a delimiter in a quoted string.  Using the same 'testdata.log' file from above, it does this
```
└─ᗒ cat testdata.log | ./wsv.py 
,
```




*to be continued*
