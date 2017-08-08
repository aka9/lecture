# @Author: e155753
# @Date:   2017-05-09T10:20:03+09:00
# @Email:  e155753@gmail.com
# @Last modified by:   e155753
# @Last modified time: 2017-05-09T23:31:48+09:00

import scipy.linalg as linalg
import numpy as np
import sys

def equation_input():
    """
    連立方程式の入力を行います. 返り値として次のようなものを返します.
    @return :
        A 入力された数字を行列として返します.
        N 変数の数を返します.
        row 入力された行数(式の数)を返します.
    """

    print("n元連立一次方程式の計算を行います.")
    print("変数の個数nを入力して下さい")
    N = int(input("n = "))
    print("\n連立方程式の係数を左から順に入力して下さい. 係数0も含みます.")
    print("右辺は文字も移行して, 数字だけにして下さい.")
    print("例 x + y = 1 -> 1 1 1, x + y = z -> 1 1 -1 \\n")
    A = []
    # for文で変数の個数分, 入力を促します.
    for row in range(N):
        # xの0で初期化されたリストを作ります.
        x = [0]*(N + 1)

        # yに入力された数字を代入します.
        y = input().split()

        # もし, yに改行が入力されると, while文を抜けます.
        if not y:
            break

        # 入力された分だけ, xの1次元リストを上書きします.
        x[:len(y)] = y

        # Aにxの行を追加します.
        A.append(x)

    # Aをfloat型のndarray型に直し, N, rowを同時に返します.
    return np.array(A, float), N


def output_formula(A, N):
    """
    式の形を画面に表示するだけの関数です.
    @param :
        A ndarray型の行列
        N 変数の数
    """
    row = A.shape[0]
    for j in range(row):
        for k in range(N):

            operator = "=" if k == N-1 else "+"

            print("({0}*x_{1}) {2} ".format(A[j, k], k, operator), end='')

        print("{0}    ---- ({1})".format(A[j, N], j + 1))


def compute_and_result(A, N):
    """
    連立方程式を計算し, 解を表示します.
    @param :
        A ndarray型の行列
        N 変数の数
    """
    B = A[:, N]
    A = A[:, :N]
    try:
        # L+UからLの単位対角成分を除いた行列と、置換行列を表す指数をLUに代入.
        LU = linalg.lu_factor(A)
        # LUとBの方程式を解く.
        X = linalg.lu_solve(LU, B)
        #X = numpy.linalg.solve(A, B)
        print("この連立方程式の解は次のようになりました.")
        for i in range(N):
            print("x_{0} = {1}".format(i, X[i]))
    except:
        sys.stderr.write("正則行列じゃないので計算できません. プログラムを終了します.\n")



if __name__ == '__main__':
    A, N = equation_input()
    output_formula(A, N)
    compute_and_result(A, N)
