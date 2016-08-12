#### BashRC file on Amanzanatrix
# Current: 3-17-2016

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

############ For Prompt
export PS1='$HOSTNAME:$(pwd)$'  # For prompt customization -- From: http://superuser.com/questions/601181/how-to-display-current-path-in-command-prompt-in-linuxs-sh-not-bash  

############## For LSST DM Stack --- 4-29-2016                                                                                                                                    
export LSSTSW=/Users/m/fizzAndAstro/lsst/lsstsw
export EUPS_PATH=$LSSTSW/stack

echo "---- Issuing:  source $LSSTSW/bin/setup.sh"
source $LSSTSW/bin/setup.sh

cd  /Users/m/fizzAndAstro/lsst/lsstsw/ci_hsc

setup lsst_apps -t b2021

export SUPRIME_DATA_DIR=/Users/m/fizzAndAstro/lsst/lsstsw/ci_hsc/data # 5-2-2016 - path to the registy.sqlite3 file

########### If i want the verbose versions:
#setup  -v -k -r /Users/m/fizzAndAstro/lsst/lsstsw/obs_subaru -t b2021
#setup  -v -k -r /Users/m/fizzAndAstro/lsst/lsstsw/ci_hsc -t b2021

########### Non-verbose setup for getting ci_hsc working

echo "---- Issuing:  setup -k  -r /Users/m/fizzAndAstro/lsst/lsstsw/obs_subaru -t b2021"
setup   -k -r /Users/m/fizzAndAstro/lsst/lsstsw/obs_subaru -t b2021

echo "---- Issuing: setup  -k -r /Users/m/fizzAndAstro/lsst/lsstsw/ci_hsc -t b2021"
setup  -k -r /Users/m/fizzAndAstro/lsst/lsstsw/ci_hsc -t b2021


# echo "---- Issuing: eups declare -r ${CI_HSC_DIR}/sdss-dr9-fink-v5b astrometry_net_data sdss-ci_hsc"
# eups declare -r ${CI_HSC_DIR}/sdss-dr9-fink-v5b astrometry_net_data sdss-ci_hsc

# echo "---- Issuing: setup -j -v astrometry_net_data sdss-ci_hsc"
# setup -j -v astrometry_net_data sdss-ci_hsc
