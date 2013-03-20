#!/bin/bash

__corpustool_comp()
{
    cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$1" -- "$cur"))
    return 0
}

_corpustool_completion()
{
    cur=${COMP_WORDS[COMP_CWORD]}
    COMMANDS='\
        tmx2bitext tmx2db bitext2tmx\
        clean'
    case "${cur}" in
       *) __corpustool_comp "$COMMANDS" ;;
    esac
}

complete -o default -o nospace -F _corpustool_completion corpustool
