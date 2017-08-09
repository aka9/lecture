# 数理計画とアルゴリズム report2
「数理計画とアルゴリズム」 report2の課題プログラムです.

## Description
大学の講義のプログラム「数理計画とアルゴリズム」のreport2の課題プログラムです.
課題は次のようになっています.
- P 個の初期解を与えて実行できる多スタート局所探索法 (Multi- Start Local Search)のプログラムを作成しなさい.<br>
  「multi-start-local-search.py」

なお, このプログラムで求めようとした割当問題は次のようなものです.

>割当て問題において英語=1、数学=2、物理=3、化学=4 で表す。 このときの 一つの可能解 X が(A,B,C,D)=(3,4,1,2)である場合、近傍探索法を適用すると、どうなるか?
>
>なお, 4 人の科目による作業時間は表 3 のとおりである.
><table border="1">
><caption>表3: 4 人の科目による作業時間</caption>
><tr><td></td><td>英語</td><td>数学</td><td>物理</td><td>化学</td></tr>
><tr><td>A</td><td>6</td><td>1</td><td>9</td><td>3</td></tr>
><tr><td>B</td><td>2</td><td>5</td><td>7</td><td>8</td></tr>
><tr><td>C</td><td>6</td><td>3</td><td>5</td><td>4</td></tr>
><tr><td>D</td><td>3</td><td>5</td><td>2</td><td>1</td></tr>
></table>



## Dependencies
- [Python3](https://www.python.org/)
- [NumPy](http://www.numpy.org/)


## Demo
```Python
python multi-start-local-search.py
```
![multi-start-local-search.py](https://github.com/e155753/lecture/wiki/images/math_prog/report2/multi-start-local-search.gif)

## Author
e155753
