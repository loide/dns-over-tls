#!/bin/bash

function run() {
    for d in $(cat domains_list.txt);
    do
        x=$(( ( RANDOM % 10 )  + 1 ))
        if [ "$x" -le 5 ]; then
            echo "dig @127.0.0.1 $d"
            dig @127.0.0.1 $d &
        else
            echo "dig @127.0.0.1 $d +tcp"
            dig @127.0.0.1 $d +tcp &
        fi
    done
}
run
