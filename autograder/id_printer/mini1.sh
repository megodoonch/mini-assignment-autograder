id=$1
module="id_printer"
project="mini1"
min=4


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
if timeout 200 python "$id-$module.py" > $outfile 2> $errfile; then
  log "importing"
  if timeout 10 python importer.py "$id-$module" > $module_out_file; then
    log "running in python"
    # checks $id-out.txt
    # imports and does stuff
    timeout 200 python "$project.py" $id > $errfile
    if [ $? == 124 ]; then
      e="$id,$min,timed out. Infinite loop?"
      log "$e"
      printf "%s\n" "$e" >> "$project.csv"
    fi
  fi

else
  if [ $? == 124 ]; then
      e="$id,$min,timed out. Infinite loop?"
      log "$e"
      printf "%s\n" "$e" >> "$project.csv"
  else
  e="$id,$min,Threw error $(<$errfile)"
  log "$e"
  printf "%s\n" "$e" >> "$project.csv"
fi
fi

