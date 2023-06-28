id=$1  # student id
module="tags"  # python module students hand in, eg if they hand in foo.py, set module="foo"
project="tags"
min=4
max_time=20  # timeout after 20 seconds

# verbosity
_V=0

OPTIND=2
while getopts "v" opt; do
  case $opt in
    v) _V=1
    ;;
    \?) echo "Invalid option -$OPTARG"
    ;;
  esac
done


# logfunction: if $_V is 1, echo, otherwise, don't.
function log () {
    if [[ $_V -eq 1 ]]; then
        echo "$@"
    fi
}


# for printing to sout in __main__ or just in file
outfile=$"$id-out.txt"
touch $outfile

errfile=$"$id-err.txt"
module_out_file="$id-module-out.txt"

log ""
log "Marking $id"
log "running in shell"
if timeout $max_time python "$id-$module.py" > $outfile 2> $errfile; then
  log "importing"
  if timeout $max_time python importer.py "$id-$module" > $module_out_file; then
    log "running in python"
    # checks $id-out.txt
    # imports and does stuff
    timeout $max_time python "$project.py" $id > $errfile
    if [ $? == 124 ]; then
      e="\"$id\",\"$min\",\"timed out. Infinite loop?\""
      log "$e"
      printf "%s\n" "$e" >> "$project.csv"
    fi
  fi

else
  if [ $? == 124 ]; then
      e="\"$id\",\"$min\",\"timed out. Infinite loop?\""
      log "$e"
      printf "%s\n" "$e" >> "$project.csv"
  else
    err=`cat $errfile`
    err=${err//$'\n'/ }
    err=${err//$'"'/\'}
    e="\"$id\",\"$min\",\"Threw error $err }\""
    log "$e"
    printf "%s\n" "$e" >> "$project.csv"
fi
fi
