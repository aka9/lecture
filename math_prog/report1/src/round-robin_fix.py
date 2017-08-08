import time
import numpy as np
import copy


def round_robin_input():
    """
    入力するだけの関数です.
    @return :
        A np.ndarray型にした, 荷物の容量, 価格のペア
        B ナップサックの容量
    """

    print("これから総当り法でナップサック問題を解きます.")
    print("袋の容量を入力して下さい")
    B = int(input("B = "))
    print("荷物の容量と, その対応する価格をスペース区切りで入力して下さい. ")
    print("入力がなくなったらenterを押して下さい.")

    A = []
    i = 0
    print("{0:6s} | {1:2s} {2:2s}".format("number", "size", "price"))

    # 改行が入力されるまで, while文で入力を促します.
    while 1:
        # number を表示するだけのための変数
        i += 1
        y = input("{0:6d} | ".format(i)).split()
        # もし改行が入ったら break する.
        if not y:
            break
        A.append(y)
    return np.array(A,int), B

def round_robin(A, B, C, X, i, n, sum_size=0, max_price=0, Save_list=[]):
    """
    総当りで計算する関数です. 再帰を用います.
    @param :
        A 価格のリスト
        B ナップサックの容量
        C 荷物の容量
        X 商品を入れる場合1, 入れない場合0が入るリスト
        i 総当り法のインクリメントに使用する変数
        n 荷物の数
        max_price 最大の値
        Save_list max_price時の選ばれた荷物のリストを保存
    @return:
        max_price 最大の値
        Save_list max_price時の選ばれた荷物のリスト
    """


    global c
    c += 1
    for j in range(2):
        X[i] = j
        sum_price = 0
        # 容量がまだ余っているなら再帰する.
        if sum_size + C[i]*X[i] <= B :
                sum_size += C[i]*X[i]
                if i < n - 1:
                    max_price, Save_list = round_robin(A, B, C, X, i+1, n, sum_size, max_price, Save_list)
                else:
                    for k in range(n):
                        sum_price += A[k]*X[k]

                    if max_price < sum_price :
                        max_price = sum_price
                        Save_list = copy.deepcopy(X)

        # もう余っていないなら, 合計を出し, 再帰しない.
        else :
            for k in range(i):
                sum_price += A[k]*X[k]

            if max_price < sum_price :
                max_price = sum_price
                Save_list = copy.deepcopy(X)



    return max_price, Save_list

if __name__ == '__main__':

    A, B = round_robin_input()

    # --------- 時間計測 start -------- #

    start = time.time()
    print("総当り法の計算を始めます")
    C = A[:, 0]
    A = A[:, 1]
    n = A.shape[0]
    X = np.zeros(n)
    A[7]
    # 総当り法の計算
    c = 1
    x, Save_list = round_robin(A, B, C, X, 0, n)
    # 選ばれた商品番号のリストを作成.
    indexes = [i for i, x in enumerate(Save_list) if x == 1]
    for i in range(len(indexes)):
        print(" {0}番目".format(indexes[i] + 1))
    print("が選ばれた場合が最良であり, 価格の最大値は{0}です.".format(x))
    exec_time = time.time() - start

    # -------- 時間計測 finish -------- #

    print ("exec_time:{0}[sec]".format(exec_time))
    print("総当り回数:{0}".format(c))