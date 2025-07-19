#!/bin/bash

export PYTHONPATH=/usr/lib/python3/dist-packages
source /usr/lib/openfoam/openfoam2412/etc/bashrc

# run from results directory
#for casedir in `find . -maxdepth 1 -type d -not -name mesh -not -name . -not -name dynamicCode`; do

# run from skewnessCavity directory
cd results
for casedir in `find . -maxdepth 1 -type d -not -name mesh -not -name . -not -name dynamicCode`; do
   #echo $casedir
   casename=`echo "$casedir" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
   echo $casename

   # magError
   datatype=magError
   filename=${casedir}/postProcessing/cuttingPlaneMagError/constant/zNormal.vtp
   echo $filename
   pvbatch error-screenshot-01.py $filename $datatype $casename 

   # error 
   # TODO 
   datatype=error
   filename=${casedir}/postProcessing/cuttingPlaneError/constant/zNormal.vtp
   echo $filename
   pvbatch error-screenshot-01.py $filename $datatype $casename 
   echo ""
done

