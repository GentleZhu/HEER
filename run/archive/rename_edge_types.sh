#!/bin/bash

# to be called from input_data/

for filename in *dblp*
do
(
    sed -i 's/ PA/ PA:u/g' "$filename"
    sed -i 's/ PV/ PV:u/g' "$filename"
    sed -i 's/ PW/ PW:u/g' "$filename"
    sed -i 's/ PY/ PY:u/g' "$filename"
    sed -i 's/ PP/ PP:d/g' "$filename"
) &
done
wait

for filename in *yago*
do
(
    sed -i 's/ 1$/ <isAffiliatedTo>:u/g' "$filename"
    sed -i 's/ 2$/ <playsFor>:u/g' "$filename"
    sed -i 's/ 3$/ <wasBornIn>:u/g' "$filename"
    sed -i 's/ 6$/ <holdsPosition>:u/g' "$filename"
    sed -i 's/ 9$/ <created>:u/g' "$filename"
    sed -i 's/ 10$/ <isCitizenOf>:u/g' "$filename"
    sed -i 's/ 11$/ <graduatedFrom>:u/g' "$filename"
    sed -i 's/ 12$/ <hasWonPrize>:u/g' "$filename"
    sed -i 's/ 13$/ <livesIn>:u/g' "$filename"
    sed -i 's/ 15$/ <hasCapital>:d/g' "$filename"
    sed -i 's/ 17$/ <diedIn>:u/g' "$filename"
    sed -i 's/ 20$/ <wroteMusicFor>:u/g' "$filename"
    sed -i 's/ 21$/ <happenedIn>:u/g' "$filename"
    sed -i 's/ 25$/ <actedIn>:u/g' "$filename"
    sed -i 's/ 26$/ <isMarriedTo>:u/g' "$filename"
    sed -i 's/ 27$/ <directed>:u/g' "$filename"
    sed -i 's/ 29$/ <hasChild>:d/g' "$filename"
    sed -i 's/ 30$/ <influences>:d/g' "$filename"
    sed -i 's/ 31$/ <isConnectedTo>:u/g' "$filename"
    sed -i 's/ 33$/ <isPoliticianOf>:u/g' "$filename"
    sed -i 's/ 35$/ <isAdvisedBy>:d/g' "$filename"
    sed -i 's/ 36$/ <edited>:u/g' "$filename"
    sed -i 's/ 38$/ <isLocatedIn>:u/g' "$filename"
    sed -i 's/ 39$/ <isPartOf>:d/g' "$filename"
    sed -i 's/ 1-1$/ <isAffiliatedTo>:u-1/g' "$filename"
    sed -i 's/ 2-1$/ <playsFor>:u-1/g' "$filename"
    sed -i 's/ 3-1$/ <wasBornIn>:u-1/g' "$filename"
    sed -i 's/ 6-1$/ <holdsPosition>:u-1/g' "$filename"
    sed -i 's/ 9-1$/ <created>:u-1/g' "$filename"
    sed -i 's/ 10-1$/ <isCitizenOf>:u-1/g' "$filename"
    sed -i 's/ 11-1$/ <graduatedFrom>:u-1/g' "$filename"
    sed -i 's/ 12-1$/ <hasWonPrize>:u-1/g' "$filename"
    sed -i 's/ 13-1$/ <livesIn>:u-1/g' "$filename"
    sed -i 's/ 15-1$/ <hasCapital>:d-1/g' "$filename"
    sed -i 's/ 17-1$/ <diedIn>:u-1/g' "$filename"
    sed -i 's/ 20-1$/ <wroteMusicFor>:u-1/g' "$filename"
    sed -i 's/ 21-1$/ <happenedIn>:u-1/g' "$filename"
    sed -i 's/ 25-1$/ <actedIn>:u-1/g' "$filename"
    sed -i 's/ 26-1$/ <isMarriedTo>:u-1/g' "$filename"
    sed -i 's/ 27-1$/ <directed>:u-1/g' "$filename"
    sed -i 's/ 29-1$/ <hasChild>:d-1/g' "$filename"
    sed -i 's/ 30-1$/ <influences>:d-1/g' "$filename"
    sed -i 's/ 31-1$/ <isConnectedTo>:u-1/g' "$filename"
    sed -i 's/ 33-1$/ <isPoliticianOf>:u-1/g' "$filename"
    sed -i 's/ 35-1$/ <isAdvisedBy>:d-1/g' "$filename"
    sed -i 's/ 36-1$/ <edited>:u-1/g' "$filename"
    sed -i 's/ 38-1$/ <isLocatedIn>:u-1/g' "$filename"
    sed -i 's/ 39-1$/ <isPartOf>:d-1/g' "$filename"
) &
done
wait