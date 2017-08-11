/**
 * @Author: e155753
 * @Date:   2017-05-05T21:55:56+09:00
 * @Email:  e155753@gmail.com
 * @Last modified by:   e155753
 * @Last modified time: 2017-05-07T00:57:53+09:00
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 256文字まで読み取れる.
#define char_num 256

void lntrim(char*);
int DPmatching(char*, char*, int, int);
int d(char, char);
int min(int, int, int);

int main(int argc, char const *argv[]) {
        char strA[char_num] = {'\0'}; // 文字列A
        char strB[char_num] = {'\0'}; // 文字列B
        int c; // 最短コスト

        // 文字列が入力されるまで, ループする.
        while(1) {
                printf("文字列Aを入力して下さい.\n");
                fgets( strA, char_num, stdin );
                if(strcmp(strA, "\n") != 0) break;
                printf("文字列が入力されていません!\n");
        }

        while(1) {
                printf("文字列Bを入力して下さい.\n");
                fgets( strB, char_num, stdin );
                if(strcmp(strB, "\n") != 0) break;
                printf("文字列が入力されていません!\n");
        }


        lntrim(strA);
        lntrim(strB);

        printf("文字列マッチングを行います.\n\n");

        // 距離を計算し, cに代入する.
        c = DPmatching(strA, strB, strlen( strA ), strlen( strB ));

        printf("同じ文字にするのに必要な操作は%d回です.\n",c);

        return 0;
}


/**
 * [lntrim 文字列の最後の改行を'\0'に置き換える.]
 * @param str [文字列]
 */
void lntrim(char *str) {
        char *p;
        p = strchr(str, '\n');
        if(p != NULL) {
                *p = '\0';
        }
}


/**
 * [DPmatching この関数を用いてAとBの距離を計算する.]
 * @param  A         [文字列Aのポインタ]
 * @param  B         [文字列Bのポインタ]
 * @param  strA_size [文字列Aの長さ]
 * @param  strB_size [文字列Bの長さ]
 * @return           [文字列A, Bの距離を返す.]
 */
int DPmatching(char* A, char* B, int strA_size, int strB_size){

        // 18文字*19文字のループでエラーになる.
        /*
           int g[strA_size + 1][strB_size + 1];
           int tab_d[strA_size+1][strB_size+1];
           for(int i = 0; i <= strA_size + 1; i++) {
                for(int j = 0; j <= strB_size + 1; j++) {
                        g[i][j] = 0;
                }
           }*/

        // callocを用いてメモリの確保を行うことでエラーが出ない.
        int **g;
        int **tab_d; // dの表を表示するために使う変数.
        int row = strA_size + 1, column = strB_size + 1;

        // g[row][column], tab_d[row][column]のメモリの確保を行う.
        g = (int **)calloc(row, sizeof (int*));
        tab_d = (int **)calloc(row, sizeof (int*));
        for(int i = 0; i < row; i++) {
                g[i] = (int *)calloc(column, sizeof (int));
                tab_d[i] = (int *)calloc(column, sizeof (int));
        }

        g[0][0] = 2*d(A[0],B[0]);

        printf("strA=%s, strB=%s\n",A,B);
        printf("strA_size=%d, strB_size=%d\n\n", strA_size, strB_size);

        // 変数g, tab_dにそれぞれ値を代入.
        for(int i = 1; i <= strA_size; i++) {
                for(int j = 1; j <= strB_size; j++) {
                        tab_d[i][j]=d(A[i-1],B[j-1]);

                        // 行, 列のそれぞれの時はそれぞれで計算する.
                        if(j==1) {
                                g[i][j] = g[i-1][j] + d(A[i-1], B[j-1]);
                        }else if(i==1) {
                          g[i][j] = g[i][j-1] + d(A[i-1], B[j-1]);
                        }else {
                                // 条件式の通り計算を行い, 最小値を代入
                                g[i][j] = min(
                                        (g[i-1][j] + d(A[i-1], B[j-1])),
                                        (g[i-1][j-1] + 2 * d(A[i-1], B[j-1])),
                                        (g[i][j-1] + d(A[i-1], B[j-1])));
                        }


                }
        }

        // --- test start --- //
        // 表をそれぞれ表示
        printf("dの表は次のようになりました.\n");

        for(int i = strA_size; i > 0; i--) {
                for(int j = 1; j <= strB_size; j++) {
                        printf("%3d |", tab_d[i][j]);
                }
                printf("\n");
        }

        printf("\ngの表は次のようになりました.\n");

        for(int i = strA_size; i > 0; i--) {
                for(int j = 1; j <= strB_size; j++) {
                        printf("%3d |", g[i][j]);
                }
                printf("\n");
        }
        // --- test finish --- //

        // 距離を返す.
        return g[strA_size][strB_size];
}


/**
 * [d 条件式d]
 * @param  a [文字列A中のある文字]
 * @param  b [文字列B中のある文字]
 * @return   [aとbが同じ文字なら0, 他は1を返す.]
 */
int d(char a, char b){
        if(a==b) return 0;
        else return 1;
}


/**
 * [min 3つの値から小さい値を返す.]
 * @param  a [教科書では(g(i-1, j) + d(i,j))に対応]
 * @param  b [教科書では(g(i-1, j-1) + 2*d(i,j))に対応]
 * @param  c [教科書では(g(i, j-1) + d(i,j))に対応]
 * @return   [a, b, cの中で最小の値を返す.]
 */
int min(int a, int b, int c){
        if(a < b) {
                if (a < c) return a;
                else return c;
        }else{
                if(b < c) return b;
                else return c;
        }

}
