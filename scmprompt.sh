SELF=$(readlink -f ${BASH_SOURCE[0]})

if [ "x$__SCM_PROMPT_DIR" == "x" ]
then
  __SCM_PROMPT_DIR=$(dirname $SELF)
fi

function update_current_SCM_vars() {
    unset __CURRENT_SCM_STATUS
    local scmstatus="${__SCM_PROMPT_DIR}/scmstatus.py"

    _SCM_STATUS=$(python $scmstatus)
    __CURRENT_SCM_STATUS=($_SCM_STATUS)
    SCM_TYPE=${__CURRENT_SCM_STATUS[0]}
    SCM_BRANCH=${__CURRENT_SCM_STATUS[1]}
    SCM_REMOTE=${__CURRENT_SCM_STATUS[2]}
    if [[ "." == "$SCM_REMOTE" ]]; then
        unset SCM_REMOTE
    fi
    SCM_STAGED=${__CURRENT_SCM_STATUS[3]}
    SCM_CONFLICTS=${__CURRENT_SCM_STATUS[4]}
    SCM_CHANGED=${__CURRENT_SCM_STATUS[5]}
    SCM_UNTRACKED=${__CURRENT_SCM_STATUS[6]}
    SCM_CLEAN=${__CURRENT_SCM_STATUS[7]}
}

function setScmPrompt() {
    local exit_code=$?
    # Colors
	# Reset
	local ResetColor="\[\033[0m\]"       # Text Reset

	# Regular Colors
	local Red="\[\033[0;31m\]"          # Red
	local Yellow="\[\033[0;33m\]"       # Yellow
	local Blue="\[\033[0;34m\]"         # Blue
	local WHITE='\[\033[37m\]'

	# Bold
	local BGreen="\[\033[1;32m\]"       # Green

	# High Intensty
	local IBlack="\[\033[0;90m\]"       # Black

	# Bold High Intensty
	local Magenta="\[\033[1;95m\]"     # Purple

	# Various variables you might want for your PS1 prompt instead
	local Time12a="\@"
	local PathShort="\w"
	local Hostname="\H"
	local Username="\u"

	# Default values for the appearance of the prompt. Configure at will.
	local SCM_PROMPT_PREFIX="["
	local SCM_PROMPT_SUFFIX="]"
	local SCM_PROMPT_SEPARATOR="|"
	local SCM_PROMPT_BRANCH="${Magenta}"
	local SCM_PROMPT_STAGED="${Red}● "
	local SCM_PROMPT_CONFLICTS="${Red}✖ "
	local SCM_PROMPT_CHANGED="${Blue}✚ "
	local SCM_PROMPT_REMOTE=" "
	local SCM_PROMPT_UNTRACKED="…"
	local SCM_PROMPT_CLEAN="${BGreen}✔"
    unset PROMPT_START
    unset PROMPT_END
    if [[ $EUID -ne 0 ]]; then
        local _USER="$BGreen$Username$ResetColor"
    else
        local _USER="$Red$Username$ResetColor"
    fi
    PROMPT_START="$_USER@$Yellow$Hostname $Blue$PathShort$ResetColor"
    PROMPT_END=" $WHITE$Time12a$ResetColor\\$ "

    if [ $exit_code -eq 0 ]; then
        exit_code="$BGreen$exit_code$ResetColor"
    else
        exit_code="$Red$exit_code$ResetColor"
    fi
    update_current_SCM_vars
    set_virtualenv

    if [ -n "$__CURRENT_SCM_STATUS" ]; then
      STATUS=" ${Yellow}$SCM_TYPE$ResetColor $SCM_PROMPT_PREFIX$SCM_PROMPT_BRANCH$SCM_BRANCH$ResetColor"

      if [ -n "$SCM_REMOTE" ]; then
          STATUS="$STATUS$SCM_PROMPT_REMOTE$SCM_REMOTE$ResetColor"
      fi

      STATUS="$STATUS$SCM_PROMPT_SEPARATOR"
      if [ "$SCM_STAGED" -ne "0" ]; then
          STATUS="$STATUS$SCM_PROMPT_STAGED$SCM_STAGED$ResetColor"
      fi

      if [ "$SCM_CONFLICTS" -ne "0" ]; then
          STATUS="$STATUS$SCM_PROMPT_CONFLICTS$SCM_CONFLICTS$ResetColor"
      fi
      if [ "$SCM_CHANGED" -ne "0" ]; then
          STATUS="$STATUS$SCM_PROMPT_CHANGED$SCM_CHANGED$ResetColor"
      fi
      if [ "$SCM_UNTRACKED" -ne "0" ]; then
          STATUS="$STATUS$SCM_PROMPT_UNTRACKED$SCM_UNTRACKED$ResetColor"
      fi
      if [ "$SCM_CLEAN" -eq "1" ]; then
          STATUS="$STATUS$SCM_PROMPT_CLEAN"
      fi
      STATUS="$STATUS$ResetColor$SCM_PROMPT_SUFFIX"

      PS1="[$exit_code] $PYTHON_VIRTUALENV$PROMPT_START$STATUS$PROMPT_END"
    else
      PS1="[$exit_code] $PROMPT_START$PROMPT_END"
    fi
}

# Determine active Python virtualenv details.
function set_virtualenv () {
  if test -z "$VIRTUAL_ENV" ; then
      PYTHON_VIRTUALENV=""
  else
      PYTHON_VIRTUALENV="${BLUE}(`basename \"$VIRTUAL_ENV\"`)${ResetColor} "
  fi
}

PROMPT_COMMAND=setScmPrompt
