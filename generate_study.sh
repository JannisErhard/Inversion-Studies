#!/bin/bash

for Sys in He2_+ H3 Li Be B C 
  do
  #sourcefolders=`ls -d --color=never ~/DMs/FCI/$Sys/*_aug-cc-pwCV?Z`
  sourcefolders=`ls -d --color=never ~/DMs/FCI/$Sys/*_aug-cc-pwCVTZ`
  for sourcefolder in $sourcefolders
    do 
    name=`echo $sourcefolder | sed "s/\//\ /g" | awk '{print $NF}'`
    AO_Basis=`echo $name | sed "s/\_/\ /g" | awk '{print $NF}'`
    Element=`echo  $name | sed "s/\_/\ /g" | awk '{print $1}'`
    Charge=`echo  $name | sed "s/\_/\ /g" | awk '{print $3}'`
    Unpaired=`echo  $name | sed "s/\_/\ /g" | awk '{print $5}'`
    E_Referenz=`grep "FCI STATE  1.1 Energy " $sourcefolder/output | tail -n 1  | awk '{print $NF}'`
    Major=`grep $name ~/DMs/FCI/$Sys/Table | awk '{print $2}'`
    Minor=`grep $name ~/DMs/FCI/$Sys/Table | awk '{print $3}'`
    if [[ $Minor == "" ]]
 then
      Minor=0d0
    fi
    mkdir $Element
    mkdir "$Element"/"$name"
    for thr in 5d-2 1d-2 8d-3 6d-3 4d-3 2d-3 1d-3 8d-4 5d-4 1d-4 5d-5 1d-5 5d-6 1d-6 
    do
      #for OEP_Basis in  "aug-cc-pVDZ" "aug-cc-pwCVDZ" "aug-cc-pVTZ" "aug-cc-pwCVTZ" "aug-cc-pVQZ"
      #for OEP_Basis in  "cc-pVDZ" "cc-pwCVDZ" "cc-pVTZ" "cc-pwCVTZ" "cc-pVQZ"
      for OEP_Basis in  "cc-PVDZ"
      do
          #echo  $Element $Charge $Unpaired $AO_Basis $OEP_Basis $thr $E_Referenz
          sub_name=OEP_"$OEP_Basis"_thr_"$thr"
          mkdir "$Element"/"$name"/"$sub_name"
          #echo "$Element"/"$name"/$sub_name $E_Referenz $Major $Minor
          ln -s $sourcefolder/dm.dat "$Element"/"$name"/"$sub_name"/dm.dat
          sed "s/THR_DUMMY/$thr/g ; s/CHARGEDUMMY/$Charge/g; s/SYS_DUMMY/$Sys/g ; s/SPINDUMMY/$Unpaired/g; s/REFERENCEDUMMY/$E_Referenz/g; s/OEP_BASISDUMMY/$OEP_Basis/g ; s/AO_BASISDUMMY/$AO_Basis/g; s/MAJOR_DUMMY/"$Major"/g ; s/MINOR_DUMMY/"$Minor"/g ;"  input > "$Element"/"$name"/"$sub_name"/input
      done
    done
  done
done 
