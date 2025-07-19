# gnuplot関連メモ



## ループ

gnuplot では，大きな範囲でループする`do for`ループと，`plot`コマンド内でループする`plot for`の2つのループが存在する。

http://gnuplot.info/docs/loc9437.html#:~:text=If%20many%20similar%20files%20or%20functions%20are%20to,plot%20for%20[%20=%20%20:%20%20{:}]


do for

http://gnuplot.info/docs/loc6974.html


plot for

http://gnuplot.info/docs/loc9437.html


iteration

http://gnuplot.info/docs/loc3551.html



どちらも共通の書き方か

> Iteration is controlled by an iteration specifier with syntax
>
> ```
>      for [<var> in "string of N elements"]
> ```
>
> or
>
> ```
>      for [<var> = <start> : <end> { : <increment> }]
> ```


for

http://gnuplot.info/docs/loc7845.html


この説明を見ると，`set for`も使用できるようだ。


array

http://gnuplot.info/docs/loc3296.html



## multiplot

複数のグラフを並べたものを作成できる。

http://gnuplot.info/docs/loc13319.html



## 例

matplotlibで採用されている10色を使ってlineのstyleを設定する。10以上の値をプロットするときのために，11以上は点線を設定している。

```
    array linecolors[10] = \
        ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    
    set for [i=1:10] style line i lw 2 lc rgb linecolors[i]
    set for [i=1:10] style line 10+i lw 2 lc rgb linecolors[i] dt "--"
```