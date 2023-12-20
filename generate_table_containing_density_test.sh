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
    if [[ "$Minor" == "" ]]; then
      Minor=0d0
    fi
    for thr in 5d-2 1d-2 8d-3 6d-3 4d-3 2d-3 1d-3 8d-4 5d-4 1d-4 5d-5 1d-5 5d-6 1d-6 
    do
      #for OEP_Basis in  "aug-cc-pVDZ" "aug-cc-pwCVDZ" "aug-cc-pVTZ" "aug-cc-pwCVTZ" "aug-cc-pVQZ"
      #for OEP_Basis in  "cc-pVDZ" "cc-pwCVDZ" "cc-pVTZ" "cc-pwCVTZ" "cc-pVQZ"
      for OEP_Basis in  "cc-PVTZ"
      do
	sub_name=OEP_"$OEP_Basis"_thr_"$thr"
	n_channels=`grep "HOMO" "$Element"/"$name"/"$sub_name"/output_2  | tail -n 1 | awk '{print NF}'`
        Alpha_Eigenvalue=""
        Alpha_E_EH="" 
        Beta_Eigenvalue=""
        Beta_E_EH=""
	if (($n_channels  == 3 && $Unpaired >  0)) ; then
	  Alpha_Eigenvalue=`grep Deviation "$Element"/"$name"/"$sub_name"/output_2 | grep alpha | awk -v major=$Major '{print $(NF-1), $NF, $NF/major*100 }'`
	  Alpha_E_EH=`grep "E_H" "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $3}'`
	  Beta_Eigenvalue=`grep Deviation "$Element"/"$name"/"$sub_name"/output_2 | grep beta | awk -v minor=$Minor '{print $(NF-1), $NF, $NF/minor*100 }'`
	  Beta_E_EH=`grep "E_H" "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $4}'`
	  Alpha_Density_Error=` grep alpha-Density-Test "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $2}'`
	  Alpha_t_II=`grep "t_rhs_II_alpha" "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $2}'`
	  Beta_t_II=`grep "t_rhs_II_beta" "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $2}'`
	  Beta_Density_Error=` grep beta-Density-Test "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $2}'`
	  echo alpha $AO_Basis $Element $Charge  $Unpaired $OEP_Basis $thr $Alpha_Eigenvalue $Alpha_E_EH $Alpha_Density_Error $Alpha_t_II | awk 'NF==13{print $0}'
	  echo beta  $AO_Basis $Element $Charge  $Unpaired $OEP_Basis $thr $Beta_Eigenvalue  $Beta_E_EH  $Beta_Density_Error  $Beta_t_II | awk 'NF==13{print $0}'
  	elif (( $n_channels == 2 )); then
	  Alpha_Eigenvalue=`grep Deviation "$Element"/"$name"/"$sub_name"/output_2 | grep alpha | awk -v major=$Major '{print $(NF-1), $NF, $NF/major*100 }'`
	  Alpha_E_EH=`grep "E_H" "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $3}'`
	  Alpha_Density_Error=` grep alpha-Density-Test "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $2}'`
	  Alpha_t_II=`grep "t_rhs_II_alpha" "$Element"/"$name"/"$sub_name"/output_2 | awk '{print $2}'`
	  echo alpha $AO_Basis $Element $Charge  $Unpaired $OEP_Basis $thr $Alpha_Eigenvalue $Alpha_E_EH $Alpha_Density_Error $Alpha_t_II | awk 'NF==13{print $0}'
        fi
      done
    done
  done
done 
