#!/bin/bash

__corpustk_comp()
{
    cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$1" -- "$cur"))
    return 0
}

_corpustk_completion()
{
    cur=${COMP_WORDS[COMP_CWORD]}
    COMMANDS='\
        tmx2bitext tmx2db bitext2tmx\
        clean'
    case "${cur}" in
       *) __corpustk_comp "$COMMANDS" ;;
    esac
}

complete -o default -o nospace -F _corpustk_completion corpustk
