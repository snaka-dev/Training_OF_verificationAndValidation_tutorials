# OpenFOAMのV&V例題の実行と解読：注意事項

https://develop.openfoam.com/Development/openfoam/-/tree/master/tutorials/verificationAndValidation

この`verificationAndValidation`例題集を実行する前に，注意事項を確認してください。思ったよりも多くの計算量とディスク容量が必要となるかもしれません。使用するマシンのスペックを確認して，実行に問題がないかを検討してください。


## 実行に必要なディスク容量

`verificationAndValidation`例題集を実行すると，全体で8GB程度のディスク容量を消費することになる。

```shell
verificationAndValidation$ du -hd 1
1.1G    ./multiphase
953M    ./turbulenceModels
1.5G    ./schemes
4.5G    ./atmosphericModels
235M    ./turbulentInflow
8.2G    .

verificationAndValidation$ du -hs multiphase/*/
183M    multiphase/StefanProblem/
857M    multiphase/interIsoFoam/

verificationAndValidation$ du -hs turbulenceModels/*/
953M    turbulenceModels/planeChannel/

verificationAndValidation$ du -hs turbulentInflow/*/
235M    turbulentInflow/oneCellThickPlaneChannel/

verificationAndValidation$ du -hs atmosphericModels/*/
936M    atmosphericModels/atmDownstreamDevelopment/
2.9G    atmosphericModels/atmFlatTerrain/
700M    atmosphericModels/atmForestStability/

verificationAndValidation$ du -hs schemes/*/
36M     schemes/divergenceExample/
998M    schemes/nonOrthogonalChannel/
477M    schemes/skewnessCavity/
584K    schemes/weightedFluxExample/
```



## 並列計算

並列計算の準備状況を調査する。まずは，ケース内に`decomposeParDict`が存在するか否かを，シェルの`find`コマンドで調べてみる。

```shell
verificationAndValidation$ find . -name decomposeParDict
./turbulentInflow/oneCellThickPlaneChannel/setups.orig/common/system/decomposeParDict
./schemes/nonOrthogonalChannel/setups.orig/common/system/decomposeParDict
./schemes/skewnessCavity/setups.orig/common/system/decomposeParDict
./turbulenceModels/planeChannel/setups.orig/common/system/decomposeParDict
./multiphase/StefanProblem/setups.orig/common/system/decomposeParDict
./multiphase/interIsoFoam/porousDamBreak/system/decomposeParDict
./atmosphericModels/atmForestStability/setups.orig/common/system/decomposeParDict
./atmosphericModels/atmDownstreamDevelopment/setups.orig/common/system/decomposeParDict
./atmosphericModels/atmFlatTerrain/successor/setups.orig/common/system/decomposeParDict
./atmosphericModels/atmFlatTerrain/precursor/setups.orig/common/system/decomposeParDict
```



`find`で見つかるファイルの中で，領域分割数`numberOfSubdomains`の文字を探し（grepを使う），分割数を確認する。

```shell
verificationAndValidation$ find ./ -name decomposeParDict -exec grep 'numberOfSubdomains' {} \;
numberOfSubdomains  4;
numberOfSubdomains  2;
numberOfSubdomains  2;
numberOfSubdomains  2;
numberOfSubdomains  2;
numberOfSubdomains 4;
numberOfSubdomains 2;
numberOfSubdomains 8;
numberOfSubdomains 8;
numberOfSubdomains 2;
```



`find`と`xargs`とを組み合わせて`grep`を使うと，ファイル名とともに表示される。

```shell
verificationAndValidation$ find . -name decomposeParDict | xargs grep 'numberOfSubdomains'
./turbulentInflow/oneCellThickPlaneChannel/setups.orig/common/system/decomposeParDict:numberOfSubdomains  4;
./schemes/nonOrthogonalChannel/setups.orig/common/system/decomposeParDict:numberOfSubdomains  2;
./schemes/skewnessCavity/setups.orig/common/system/decomposeParDict:numberOfSubdomains  2;
./turbulenceModels/planeChannel/setups.orig/common/system/decomposeParDict:numberOfSubdomains  2;
./multiphase/StefanProblem/setups.orig/common/system/decomposeParDict:numberOfSubdomains  2;
./multiphase/interIsoFoam/porousDamBreak/system/decomposeParDict:numberOfSubdomains 4;
./atmosphericModels/atmForestStability/setups.orig/common/system/decomposeParDict:numberOfSubdomains 2;
./atmosphericModels/atmDownstreamDevelopment/setups.orig/common/system/decomposeParDict:numberOfSubdomains 8;
./atmosphericModels/atmFlatTerrain/successor/setups.orig/common/system/decomposeParDict:numberOfSubdomains 8;
./atmosphericModels/atmFlatTerrain/precursor/setups.orig/common/system/decomposeParDict:numberOfSubdomains 2;
```



`Allrun`スクリプト

```shell
verificationAndValidation$ find -name Allrun* | xargs grep 'runParallel'
./turbulentInflow/oneCellThickPlaneChannel/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./turbulentInflow/oneCellThickPlaneChannel/setups.orig/common/Allrun-parallel:# runParallel -s decompose redistributePar -decompose -latestTime
./turbulentInflow/oneCellThickPlaneChannel/setups.orig/common/Allrun-parallel:runParallel -s 2 $(getApplication)
./schemes/nonOrthogonalChannel/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./schemes/skewnessCavity/setups.orig/common/Allrun-parallel:runParallel postProcess -constant
./turbulenceModels/planeChannel/setups.orig/EBRSM.setTurbulenceFields/Allrun-parallel:runParallel setTurbulenceFields
./turbulenceModels/planeChannel/setups.orig/EBRSM.setTurbulenceFields/Allrun-parallel:runParallel $(getApplication)
./turbulenceModels/planeChannel/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./multiphase/StefanProblem/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./multiphase/interIsoFoam/porousDamBreak/Allrun:runParallel $(getApplication)
./atmosphericModels/atmForestStability/setups.orig/common/Allrun-parallel:runParallel setFields
./atmosphericModels/atmForestStability/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./atmosphericModels/atmForestStability/setups.orig/common/Allrun-parallel:runParallel redistributePar -reconstruct -latestTime
./atmosphericModels/atmDownstreamDevelopment/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./atmosphericModels/atmFlatTerrain/successor/setups.orig/common/Allrun-parallel:runParallel $(getApplication)
./atmosphericModels/atmFlatTerrain/precursor/setups.orig/common/Allrun-parallel:runParallel $(getApplication)

```



### 実行後の確認

計算を実行した後の`verificationAndValidation`ディレクトリで，ログファイルの中に並列計算オプション`-parallel`が使われているかを確認する。

```shell
verificationAndValidation$ find -name log.* | xargs grep '\-parallel'
./turbulentInflow/oneCellThickPlaneChannel/results/DFM/log.pisoFoam.2:Exec   : pisoFoam -parallel
./turbulentInflow/oneCellThickPlaneChannel/results/DFM/log.pisoFoam:Exec   : pisoFoam -parallel
./turbulentInflow/oneCellThickPlaneChannel/results/DFSEM/log.pisoFoam.2:Exec   : pisoFoam -parallel
./turbulentInflow/oneCellThickPlaneChannel/results/DFSEM/log.pisoFoam:Exec   : pisoFoam -parallel
./turbulentInflow/oneCellThickPlaneChannel/results/FSM/log.pisoFoam.2:Exec   : pisoFoam -parallel
./turbulentInflow/oneCellThickPlaneChannel/results/FSM/log.pisoFoam:Exec   : pisoFoam -parallel
./multiphase/StefanProblem/results/interCondensatingEvaporatingFoam/log.interCondensatingEvaporatingFoam:Exec   : interCondensatingEvaporatingFoam -parallel
./multiphase/StefanProblem/results/icoReactingMultiphaseInterFoam/log.icoReactingMultiphaseInterFoam:Exec   : icoReactingMultiphaseInterFoam -parallel
./multiphase/interIsoFoam/porousDamBreak/log.interIsoFoam:Exec   : interIsoFoam -parallel
./atmosphericModels/atmForestStability/results/unstable/log.redistributePar:Exec   : redistributePar -parallel -reconstruct -latestTime
./atmosphericModels/atmForestStability/results/unstable/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmForestStability/results/unstable/log.setFields:Exec   : setFields -parallel
./atmosphericModels/atmForestStability/results/stable/log.redistributePar:Exec   : redistributePar -parallel -reconstruct -latestTime
./atmosphericModels/atmForestStability/results/stable/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmForestStability/results/stable/log.setFields:Exec   : setFields -parallel
./atmosphericModels/atmForestStability/results/slightlyStable/log.redistributePar:Exec   : redistributePar -parallel -reconstruct -latestTime
./atmosphericModels/atmForestStability/results/slightlyStable/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmForestStability/results/slightlyStable/log.setFields:Exec   : setFields -parallel
./atmosphericModels/atmForestStability/results/veryStable/log.redistributePar:Exec   : redistributePar -parallel -reconstruct -latestTime
./atmosphericModels/atmForestStability/results/veryStable/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmForestStability/results/veryStable/log.setFields:Exec   : setFields -parallel
./atmosphericModels/atmForestStability/results/slightlyUnstable/log.redistributePar:Exec   : redistributePar -parallel -reconstruct -latestTime
./atmosphericModels/atmForestStability/results/slightlyUnstable/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmForestStability/results/slightlyUnstable/log.setFields:Exec   : setFields -parallel
./atmosphericModels/atmForestStability/results/neutral/log.redistributePar:Exec   : redistributePar -parallel -reconstruct -latestTime
./atmosphericModels/atmForestStability/results/neutral/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmForestStability/results/neutral/log.setFields:Exec   : setFields -parallel
./atmosphericModels/atmDownstreamDevelopment/results/kEpsilon/log.simpleFoam:Exec   : simpleFoam -parallel
./atmosphericModels/atmDownstreamDevelopment/results/kOmegaSST/log.simpleFoam:Exec   : simpleFoam -parallel
./atmosphericModels/atmFlatTerrain/successor/results/kEpsilon/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmFlatTerrain/successor/results/kL/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmFlatTerrain/successor/results/kOmegaSST/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmFlatTerrain/precursor/results/kEpsilon/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmFlatTerrain/precursor/results/kL/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
./atmosphericModels/atmFlatTerrain/precursor/results/kOmegaSST/log.buoyantBoussinesqSimpleFoam:Exec   : buoyantBoussinesqSimpleFoam -parallel
```



## 2023年9月以降のOpenFOAMでのrunParallel

2023年8月のコミット（August 31, 2023 at 2:56:12 AM GMT+9）により，OpenMPIを使ったシステムでは，`runParallel`で並列計算を実行すると`--oversubscribe`オプションが付加されるようになった。このオプションをつけると，使用できるスレッド数よりも多い並列計算を実行してもエラーが発生せず，計算が実行できる。（従来は，There are not enough slots available in the system ... といったエラーが発生した。ただし，CPU数が増える訳ではないので，計算は遅いままである。）

[CONFIG: runParallel with --oversubscribe for openmpi (dfde6ed) · Commits · Development / openfoam · GitLab](https://develop.openfoam.com/Development/openfoam/-/commit/df6de6ed33b0fe995bdae348a1a7369c62203d32)
