# 備忘録
__各言語の記法備忘録__

## C
---
### 静的配列宣言
    <型> <配列名>[サイズ] = {}  

### 動的配列宣言(malloc)
    #include <stdlib.h>
    <ポインタ変数> = malloc(必要なメモリサイズ)
    ex)int* array = (*int)malloc(sizeof(int));

### malloc解放
    free(ポインタ変数)  

↑[参考](https://9cguide.appspot.com/19-01.html)

### ポインタ関係
    <型> *<ポインタ変数名> = <アドレス>   
先頭に&をつけて`&<変数名>`とすると変数のアドレスを取得する

### フォーマット指定子
|指定子|対応する型|説明|使用例|
|:---:|:---|:---|:---|
|%c|char|１文字を出力|"%c"|
|%s|char*|文字列を出力|"%8s"|
|%d|int, short|整数を10進で出力|"%10d", "%09d"|
|%u|unsigned int, unsigned short|符号なし整数を10進で出力|"%2u", "%02u"|
|%o|int, short, <br> unsigned int, unsigned short|整数を8進で出力|"%06o", "%3o"|
|%x|int, short, <br> unsigned int, unsigned short|整数を16進で出力|"%04x"|
|%f|float|実数を出力|"%5.2f"|
|%e|float|実数を指数表示で出力|"%5.3e"|
|%g|float|実数を最適な形式で出力|"%g"|
|%ld|long|倍精度整数を10進で出力|"%10ld"|
|%lu|unsigned long|符号なし倍精度整数を10進で出力|"%10lu"|
|%lo|long, unsigned long|倍精度整数を8進で出力|"%12o"|
|%lx|long, unsigned long|倍精度整数を16進で出力|"%08lx"|
|%lf|double|倍精度実数を出力|"%8.2lf"|

### 文字列からの入力
    sscanf(<char型配列>, "<フォーマット指定子>", <変数 or 変数へのアドレス>)


## C++
---

## Python
---
### 配列宣言  
    list = []

### 変数の型指定   
    <変数名>: <型名>     

### 返り値の型指定  
    def <関数名>(引数) -> <型名>:     

## PowerShell
---
### 変数宣言
    $<変数名> = <?> 

### プロセス起動
    Start-Process <Path> <-option> 

## FPGA
---
    [入力信号]
    input   <変数名>

    [出力信号]
    output  <[ビット幅]>  <変数名>

### データ型
    [レジスタ型]
    reg     [<ビット幅>]    <変数名>
reg はレジスタを表し、信号を保持しておくもの
reg宣言を行った信号はalways文でしか使用できない

    [ネット型]
    wire    [<ビット幅>]    <変数名>
wire : 無名の信号を次の回路につなぐ線のようなもの

### 制約ファイル
ボード上のピンをアサインしないと正しく動かない。
    IOSTANDARD LVCMOS<電圧>
