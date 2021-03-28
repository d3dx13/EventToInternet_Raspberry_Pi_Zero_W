#!/bin/bash

update=False

echo "ping https://github.com"
case "$(curl -s --max-time 2 -I https://github.com | sed 's/^[^ ]*  *\([0-9]\).*/\1/; 1q')" in
  [23]) echo "HTTP connectivity is up"; update=True;;
  5) echo "The web proxy won't let us through";;
  *) echo "The network is down or very slow";;
esac

if [[ ${update} == True ]]
then
    update=False

    git remote update

    UPSTREAM=${1:-'@{u}'}
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "$UPSTREAM")
    BASE=$(git merge-base @ "$UPSTREAM")

    if [[ ${LOCAL} = ${REMOTE} ]]
    then
        echo "Up-to-date"
    elif [[ ${LOCAL} = ${BASE} ]]
    then
        echo "Need to pull"
        update=True
    elif [[ ${REMOTE} = ${BASE} ]]
    then
        echo "Need to push"
    else
        echo "Diverged"
    fi
fi

if [[ ${update} == True ]]
then
    git checkout .
    git clean -fd
    git pull --force
    cp -f /etc/systemd/system/EventToInternet/EventToInternet.service /etc/systemd/system/EventToInternet.service
    sudo systemctl restart EventToInternet.service
fi




