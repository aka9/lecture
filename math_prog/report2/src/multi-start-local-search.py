import random
import numpy as np
import copy as cp
import sys

def random_input(A, B, C, D):
    """
    初期解の数を入力し, ランダムに生成した後, そのリストを返す関数.
    @param : 今回の問題で出た割当問題の作業時間. Aさん ~ Dさん.
    @return :
        データは加工しやすいようにndarray型に変換し, returnする.
        np.array(init_list) : 各初期解を行ごとに保存したもの.
    """

    init_list=[] # S_0 から S_Pまでの初期解を保存する変数
    print("これから多スタート局所探索法を行います.")
    print("初期解の個数を入力して下さい.")
    P = int(input("P = "))
    print("初期解は次のようになります.")

    for i in range(P):
        # 初期解を1つランダムに生成する.
        S = random.sample(range(1, 5), 4)
        # 初期解より実際に求めた値を保存する
        x = A[S[0] - 1] + B[S[1] - 1] + C[S[2] - 1] + D[S[3] - 1]

        print("S_{0} = {1} = {2}".format(i, S, x))
        init_list.append(S) # 初期解をリストに加える

    # 初期解のリストを返す.
    return np.array(init_list)



def local_search(A, B, C, D, init_list, non_display=False):
    """
    局所探索を行う関数です.
    @param :
        A : 今回の問題で出た割当問題の作業時間. Aさん
        B : 今回の問題で出た割当問題の作業時間. Bさん
        C : 今回の問題で出た割当問題の作業時間. Cさん
        D : 今回の問題で出た割当問題の作業時間. Dさん
        init_list : ランダムに生成された初期解のリスト.
    @return :
        final_interim_form,  : 各暫定解を行ごとに保存したリスト.
        process_sol : 各暫定解の目的関数値を保存したリスト.
    """
    count = 0 # 何回目の探索かを保持する関数.
    P = init_list.shape[0] # 初期解の数
    # 暫定解を保持する関数.
    final_interim_form = cp.deepcopy(init_list)
    # 初期解のリストをprocess_listにコピー
    process_list = cp.deepcopy(init_list)
    # 解の目的関数値のリストを保持する変数.
    process_sol = np.empty(P, dtype=int)

    # 各初期解の目的関数値をprocess_solに代入.
    for i in range(P):
        S = process_list[i]
        process_sol[i] = A[S[0] - 1] + B[S[1] - 1] + C[S[2] - 1] + D[S[3] - 1]

    # 終了条件に達するまでwhileでループ. 探索する.
    while 1:
        count += 1
        # 1回の摂動を行い, 返ってきたそれぞれの近傍解をprocess_listに代入
        process_list = neighborhood_search(A, B, C, D, process_list)

        # 途中経過の表示と暫定解の入れ替え
        for i in range(P):
            # ある解S_iをSに代入
            S = process_list[i]
            # Sによって求められた値をxに代入
            x = A[S[0] - 1] + B[S[1] - 1] + C[S[2] - 1] + D[S[3] - 1]

            # non-displayがFalseなら経過を表示.
            if(not (non_display)):
                # ある解S_iとそれによって求まった値xを出力
                print("P_{0}{1} = {2} = {3}".format(i, count, S, x))

            # もし, 求まった値xが初期解で求められた値より小さかったら.
            if (process_sol[i] > x):
                # 新しい式をリストに加える.
                final_interim_form[i] = S
                # 新しい解をリストに加える.
                process_sol[i] = x

        # もし, 終了条件を満たしていればループを抜ける.
        if(end_rule(count)): break

    return final_interim_form, process_sol


def neighborhood_search(A, B, C, D, process_list):
    """
    摂動を加える関数です. (今回は, 数字を1つとなりにrotateするという処理)
    @param :
        A : 今回の問題で出た割当問題の作業時間. Aさん
        B : 今回の問題で出た割当問題の作業時間. Bさん
        C : 今回の問題で出た割当問題の作業時間. Cさん
        D : 今回の問題で出た割当問題の作業時間. Dさん
        process_list : 途中解のリスト.
    @return :
        process_list : 各途中解に摂動を加えた後, そのリストを返す.
    """

    # 数字を1つ隣に rotate するという処理を「摂動」と定義して適用する
    process_list = process_list + 1
    process_list[process_list==5] = 1

    # 摂動後の途中解を返す.
    return process_list


def end_rule(count):
    """
    終了条件を定義する関数. 今回は3回摂動をすれば終了するという定義にしている.
    @param :
        count : 何回摂動を行ったかを保持している変数.
    @return :
        True or False : 終了条件に達したらTrue, それ以外はFalse
    """
    end_point = 3 # x回摂動を行うと終了という条件. 今回は3.

    # 終了条件に達していたらTrue, それ以外はFalseを返す.
    if count == end_point: return True
    else:                            return False


def output(last_list, last_interim_sol):
    """
    結果を表示するだけの関数.
    @param :
        last_list : 最後に保持している全ての暫定解のリスト.
        last_interim_sol : 最後に保持している目的関数値のリスト.
    """

    P = last_list.shape[0] # 解の数
    print("最終暫定解はこのようになりました.")

    # 暫定解と目的関数値の表示.
    for i in range(P):
        print("S_{0} = {1} = {2}".format(i, last_list[i], last_interim_sol[i]))
    # 一番短い作業時間の表示.
    print("よって, 1番短い作業時間は{0}となります".format(last_interim_sol.min()))


# main
if __name__ == '__main__':

    A = [6, 1, 9, 3] # Aくんの作業時間
    B = [2, 5, 7, 8] # Bくんの作業時間
    C = [6, 3, 5, 4] # Cくんの作業時間
    D = [3, 5, 2, 1] # Dくんの作業時間
    
    argvs = sys.argv # 引数を取得
    non_display=False # 途中解を表示するかどうかを判定する変数

    # もし引数があり, "-n"ならば, 途中解は表示しない.
    if(len(argvs) != 1):
        if(argvs[1] == "-n"):
            non_display=True

    # 初期解をランダムに生成する.
    print("------- input -------\n")
    init_list= random_input(A, B, C, D)

    # 局所探索法を適用する.
    print("\n------- search -------\n")
    last_list, last_interim_sol = local_search(A, B, C, D, init_list,non_display)

    # 暫定解と目的関数値の表示
    print("\n------- output -------\n")
    output(last_list, last_interim_sol)