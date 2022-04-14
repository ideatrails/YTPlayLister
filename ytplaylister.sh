#!/usr/bin/bash
# -----------------------------------------------------------------------------
# automate the searching and updating
# run python script that is in a python vvirtual env
# linux python directory linvenv
# (dev windows WSL2 directory venv)
# -----------------------------------------------------------------------------
AppDirProd="/home/gesso/prod/vidory/YTPlayLister"
AppDirDev="/home/coolin/staging/vidory/YTPlayLister"

prod=

if [[ $prod ]]; then
    AppDir=$AppDirProd
else
    AppDir=$AppDirDev
fi

VenvCmd_wsl="${AppDir}/linvenv/bin/activate"

if [[ $# < 3 ]]; then
    echo "params count $# lees then 3"
    exit 42
fi

while getopts c:p:e: flag
do
    case "${flag}" in
        c) corpus=${OPTARG};;
        p) playlist=${OPTARG};;
        e) enable_cmd=${OPTARG};;
    esac
done

#overrides
#enable_cmd=

# echo "corpus: $corpus";
# echo "playlist: $playlist";
# echo "enable_cmd: $enable_cmd";

if [[ ! $corpus || ! $playlist ]]; then
    exit 42
fi

Process_Corpus_YTPlayister() {
    # echo "Process - yt Playlist"
    # source the python venv
    lister_cmd_str="cd ${AppDir} && source ${VenvCmd_wsl} && python ${AppDir}/ytplaylist.py"
    lister_cmd_str+=" -c ${corpus}"
    lister_cmd_str+=" --playlist ${playlist}"

    local return_eval=
    if [[ $enable_cmd ]]; then
        eval ${lister_cmd_str}
        return_eval=$?
        # echo && echo "return eval ${return_eval}"
    else
        echo "Dry run for command : "
        echo ${lister_cmd_str}
    fi
}

Process_Corpus_YTPlayister
