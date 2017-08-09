import numpy as np
import pandas as pd
import sys

def simplex_input():

    A = []
    print("これからシンプレックス法を用いて式を解きます. Zの係数を入力して下さい.")
    print("例: max Z = X_1 + X_2 -> max Z = 1 1")
    Z = input("max Z = ").split()
    print("制約条件について, 係数を入れてください.")
    print("例: X_1 + X_2 = 1 -> 1 1 1")
    print("入力がなくなったらenterを押して下さい.")



    # 改行が入力されるまで, while文で入力を促す.
    while 1:
        y = input().split()
        # もし改行が入ったら break する.
        if not y:
            break
        A.append(y)

    Z.append(0) # Zに0を追加する.
    A.append(Z) # AにZの式を追加する.
    A = np.array(A, int) # Aをndarrayのint型に変換.
    row, column = A.shape # 次元をそれぞれ変数として代入.
    A[row-1]=-A[row-1]

    # -------------------- 式を表示する -------------------- #

    print("min Z = ", end="")
    for k in range(0,column-1):
        operator = "" if k == column-2 else "+"
        print("({0}*x_{1}) {2} ".format(A[row-1, k], k, operator), end='')

    print()

    for j in range(0,row-1):
        for k in range(column-1):
                operator = "=" if k == column-2 else "+"

                print("({0}*x_{1}) {2} ".format(A[j, k], k, operator), end='')
        print("{0}    ---- ({1})".format(A[j, column-1], j))

    # ------------------------------------------------------------ #

    # {column}列目が定数なので, 1列目に移動.
    A=np.c_[A[:,column-1]  ,A[:,0:column-1]]


    return A


def simplex_method(A):
    row, column = A.shape

    print("次のシンプレックスタブローを得ました.")
    simplex_tableau=init_simplex_tableau(A)
    print(simplex_tableau)

    # 停止条件に入るまで, ループする.
    # 停止条件は, 1: Zの式で負の数がなくなった時. 2: PEが負の時. としている.
    while 1:
        Z=simplex_tableau.iloc[row-1,:]

        # Zの式で負の数がなくなった場合, 解を表示
        if Z.min() >= 0 :
            print("解は次のようになりました")
            for i in range(1,column):
                index="X_{0}".format(i)
                if index in simplex_tableau.index:
                    x=simplex_tableau["定数"][index]
                else:
                    x=0
                print("X_{0} = {1}".format(i, x))
            print("Z = {0}".format(simplex_tableau.iloc[row-1][0]))

            break

        else:
            # PEの行番号, 列番号を取得
            pivot_col, pivot_row = select_pivot_element(simplex_tableau)
            # PEの値を取得
            pivot_element=simplex_tableau.iloc[pivot_row, pivot_col]

            # PEが正の時, シンプレックスタブローを更新.
            if(pivot_element > 0):
                print("PEは{0}行{1}列目の{2}です.".format(pivot_row+1, pivot_col+1, pivot_element))
                simplex_tableau = new_simplex_tableau(simplex_tableau, pivot_row, pivot_col)
                print(simplex_tableau)
            else:
                print("pivot_elementに該当する値がありません. ")
                print("よって, 最適解は存在しません.")
                break

    return 0


def select_pivot_element(simplex_tableau):
    """
    PEの行番号と列番号を, PEの選び方による計算で得ます.
    """

    row, column = simplex_tableau.shape
    # Zの式から一番低い値をPEの列番号にします.
    Z=simplex_tableau.iloc[row-1,1:]
    pivot_col_num=simplex_tableau.columns.get_loc(Z.argmin())

    # PEの列から, 定数の列を割ったものを, 配列として取得します.
    pivot_col=simplex_tableau.iloc[:row-1,pivot_col_num]
    pivot_col=pivot_col.where(pivot_col > 0, sys.float_info.min)
    tmp=simplex_tableau.iloc[:row-1,0]/pivot_col

    # 割った配列の中で値が小さい行を得ます.
    pivot_row_num=tmp.index.get_loc(tmp.argmin())

    return pivot_col_num, pivot_row_num



def new_simplex_tableau(simplex_tableau, pivot_row, pivot_col):
    """
    新しいシンプレックスタブローを返します.
    """

    row, column = simplex_tableau.shape
    pivot_element=simplex_tableau.iloc[pivot_row, pivot_col]

    # PEの行をPEで割ります.
    new_row=simplex_tableau.iloc[pivot_row,:]/pivot_element
    new_row=new_row.values

    # PEの列を取得します.
    old_col=simplex_tableau.iloc[:,pivot_col].values.reshape(row,1)

    # 新しいタブローを得ます
    simplex_tableau = simplex_tableau - new_row * old_col
    simplex_tableau.iloc[pivot_row,:] = new_row

    # 列名, 行名を変更します.
    old_col_name="-X_{0}".format(pivot_col)
    old_row_name="X_{0}".format(column+pivot_row)
    new_col_name="X_{0}".format(pivot_col)
    new_row_name="-X_{0}".format(column+pivot_row)

    simplex_tableau.rename(columns={old_col_name:new_row_name},
                                            index={old_row_name: new_col_name},
                                            inplace=True)

    return simplex_tableau



def init_simplex_tableau(A):
    """
    最初のシンプレックスタブローを返します.
    """

    A=pd.DataFrame(A)
    row, column = A.shape

    index_list=[]
    columns_list=[]

    # 列名, 行名を割り振る.
    for i in range(column,row+column):
        if i == column+row - 1:
            index_str="Z"
        else:
            index_str="X_{0}".format(i)
        index_list.append(index_str)

    for i in range(column):
        if i == 0:
            columns_str = "定数"
        else:
            columns_str = "-X_{0}".format(i)
        columns_list.append(columns_str)

    A.index = index_list
    A.columns = columns_list

    return A

# main
if __name__ == '__main__':

    A = simplex_input()
    simplex_method(A)
