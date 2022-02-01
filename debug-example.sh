#!/bin/bash

# Some console colour codes
    # Foreground colours
    fg_red="\e[31m\e[1m"
    fg_green="\e[32m"
    fg_yellow="\e[33m"
    fg_blue="\e[34m"
    fg_purple="\e[95m"
    fg_black="\e[30m"

    # Background colours
    bg_red="\e[41m"
    bg_green="\e[42m"
    bg_yellow="\e[103m"
    bg_blue="\e[46m"
    bg_purple="\e[105m"
    bg_grey="\e[100m"

    # Other formatting
    fg_bold="\e[1m"
    fg_reverse="\e[7m"
    fg_underline="\e[4m"

    # Console resets
    fg_reset="\e[39m"
    bg_reset="\e[49m"
    fbg_reset="\e[0m"

if [ "$1" == "" ]; then debugLevel=1;fi
if [ "$1" == "1" ]; then debugLevel=1;fi
if [ "$1" == "2" ]; then debugLevel=2;fi


out (){
# Debug function
# use:
#       out debug <string>
#       to log a level 1 debug message
#
#       out DEBUG <string>
#       to log a level 2 debug message

  case "$1" in
    debug)
      if [ $debugLevel -gt 0 ] || [ $debugLevel -eq 2 ];then
        fn=${FUNCNAME[@]/out/}
        fn=($fn)
        newFn=''
        for f in $(seq ${#fn[@]} -1 0); do
          newFn=$newFn"${fn[$f]} "
        done
        fn=${newFn:1:-1}
        msg=$@
        printf "$bg_grey$fg_black[${fn// / > }]$fbg_reset$bg_grey";echo -e "${msg/debug/}$fbg_reset"
        return 0
      fi
      ;;
    DEBUG)
      if [ $debugLevel -eq 2 ];then
        fn=${FUNCNAME[@]/out/}
        fn=($fn)
        newFn=''
        for f in $(seq ${#fn[@]} -1 0); do
          newFn=$newFn"${fn[$f]} "
        done
        fn=${newFn:1:-1}
        msg=$@
        printf "$bg_yellow$fg_black[${fn// / > }]$fbg_reset$fg_bold$bg_grey";echo -e "${msg/DEBUG/}$fbg_reset"
        return 0
      fi
      ;;
  esac
}

function1(){
    out DEBUG "Starting 'function1'"
    out debug "I need help with something"
    helperFunction
    out DEBUG "Finished 'function1'"
}

helperFunction(){
    out DEBUG "Starting helperFunction"
    out debug "I'm doing something!"
    out DEBUG "Finished helperFunction"
}

#Main process
out debug "Starting main"
function1
out debug "Finished"
