id=$1
project=$2
min=0.5  # minimum score possible
max_time=10

modules=()

# verbosity
_V=0

OPTIND=3
while getopts "m:v" opt; do
  case $opt in
    v) _V=1
    ;;
    m) modules+=("${OPTARG}")
      ;;
    \?) echo "Invalid option -$OPTARG"
    ;;
  esac
done

# log function: if $_V is 1, echo, otherwise, don't.
function log () {
    if [[ $_V -eq 1 ]]; then
        echo "$@"
    fi
}

function report_error_and_exit () {
  e="\"$id\",\"$1\",\"$2\""
        log "$e"
        printf "%s\n" "$e" >> "$project.csv"
        exit
}

function format_error_for_csv () {
  err=$(cat "$errfile")
      err=${err//$'\n'/ }
      err=${err//$'"'/\'}
      echo "$err"
}

# for printing to sout in __main__ or just in file
outfile=$"$id-out.txt"
touch "$outfile"

errfile=$"$id-err.txt"

log ""
log "Marking $id"
for module in "${modules[@]}"; do
  if [ ! -f "$module""_$id.py" ]; then
    report_error_and_exit $min "Misnamed file"
  fi
  if [ ! -s "$module""_$id.py" ]; then
    report_error_and_exit "0" "Empty file"
  fi
  log "running checker in python"
  # imports and does stuff
  if timeout $max_time python "$project""_checker.py" "$id" 2> "$errfile"; then
    log "ok"
  else  # if checker threw an error
    # see which kind of error
    if [ $? == 124 ]; then
      report_error_and_exit $min "timed out. Infinite loop?"
    else
      err=$(format_error_for_csv)
      report_error_and_exit 0.5 "Checker threw error $err"
    fi
  fi
done

