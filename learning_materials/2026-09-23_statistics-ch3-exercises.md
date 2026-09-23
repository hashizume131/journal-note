# 統計学3章 演習解説ノート

作成日: 2026-09-23

## このPDFの使い方

添付画像に写っている3章の演習を、推定量の性質が見えるように解説した復習ノートです。問題文そのものの転記ではなく、読み取れた内容をもとに「どの式を使うか」「なぜその式になるか」を中心に整理しています。

## まず押さえる前提

- 一致性: 標本サイズ n を大きくすると、推定量が推定したい値に近づく性質です。
- 不偏性: 推定量の期待値が、推定したい値そのものになる性質です。
- フィッシャー情報量: パラメータを少し動かしたとき、分布がどれだけ敏感に変わるかを表す量です。
- クラメール–ラオ下限: 不偏推定量の分散がこれより小さくなれない、という理論上の下限です。
- デルタ法: 推定量を関数で変換したときの近似分散を、微分で求める方法です。

## 問3.1: 変数変換で指数分布に直す

確率密度が `f(x; theta) = theta(1+x)^-(1+theta), x>0` の母集団から標本を取る設定です。ここで `Y = log(1+X)` とおくと、難しそうな密度が指数分布になります。

### 変数変換

`y = log(1+x)` なので、逆変換は `x = exp(y)-1`、微分は `dx/dy = exp(y)` です。したがって

`g(y) = f(exp(y)-1; theta) * exp(y) = theta exp(-theta y), y>0`

となり、Y は率パラメータ theta の指数分布に従います。

### 平均と分散

Y が指数分布 `Exp(theta)` なら、

- `E[Y] = 1/theta`
- `Var(Y) = 1/theta^2`

です。X の形で考えるより、Y に直してから指数分布の公式を使うのが近道です。

### T が 1/theta の一致推定量である理由

`T = (1/n) sum log(1+X_i)` は、変換後の `Y_i` の標本平均です。大数の法則より、標本平均は母平均に近づきます。

`T = Ybar -> E[Y] = 1/theta`

したがって T は `1/theta` の一致推定量です。

### T が不偏推定量である理由

期待値の線形性を使うと、

`E[T] = E[(1/n) sum Y_i] = (1/n) sum E[Y_i] = 1/theta`

となります。よって T は `1/theta` の不偏推定量です。

### T の分散とクラメール–ラオ下限

独立な標本平均なので、

`Var(T) = Var(Ybar) = Var(Y)/n = 1/(n theta^2)`

一方、1標本あたりの対数尤度は `log theta - theta y` なので、theta に関する情報量は `I_1(theta)=1/theta^2`、n標本では `I_n(theta)=n/theta^2` です。

推定対象を `tau(theta)=1/theta` とすると、`tau'(theta)=-1/theta^2` です。クラメール–ラオ下限は

`[tau'(theta)]^2 / I_n(theta) = (1/theta^4)/(n/theta^2) = 1/(n theta^2)`

となり、T の分散と一致します。つまり T は、この設定では分散の意味でかなり良い不偏推定量です。

## 問3.2: 指数分布の最尤推定とデルタ法

率パラメータ lambda の指数分布 `f(x)=lambda exp(-lambda x), x>=0` から独立に n 個観測する設定です。

### 標本平均の期待値と分散

指数分布では `E[X]=1/lambda`, `Var(X)=1/lambda^2` なので、

- `E[Xbar] = 1/lambda`
- `Var(Xbar) = 1/(n lambda^2)`

です。

### lambda の最尤推定量

観測値の和を `t = x_1 + ... + x_n` とすると、尤度は

`L(lambda) = lambda^n exp(-lambda t)`

対数尤度は

`ell(lambda) = n log lambda - lambda t`

です。微分して0にすると、

`n/lambda - t = 0`

より、

`lambda_hat = n/t = 1/Xbar`

です。

### フィッシャー情報量

2階微分は `ell''(lambda) = -n/lambda^2` です。よって

`I_n(lambda) = -E[ell''(lambda)] = n/lambda^2`

です。

### デルタ法による lambda_hat の漸近分散

`lambda_hat = g(Xbar)`、`g(u)=1/u` と見ます。`Xbar` は平均 `1/lambda`、分散 `1/(n lambda^2)` をもちます。

`g'(u) = -1/u^2` なので、`u=1/lambda` では `g'(1/lambda)=-lambda^2` です。

したがって

`Var(lambda_hat) ≈ [g'(1/lambda)]^2 Var(Xbar) = lambda^4 * 1/(n lambda^2) = lambda^2/n`

となります。

## つまずきやすい点

- 「一致」と「不偏」は別物です。不偏は平均として正しいこと、一致は n を増やしたとき近づくことです。
- `X` のまま悩まず、`Y=log(1+X)` に直すと指数分布になります。
- クラメール–ラオ下限で推定対象が `theta` ではなく `1/theta` のときは、`tau'(theta)` を必ず入れます。
- デルタ法では、関数そのものではなく、その点での微分が近似分散に効きます。

## 確認問題

1. `Y~Exp(theta)` のとき、`nYbar` ではなく `Ybar` が推定している量は何か。
2. `lambda_hat = 1/Xbar` は、なぜ `lambda` の直感的な推定量といえるか。
3. クラメール–ラオ下限で `tau(theta)=1/theta` と置いたとき、`tau'(theta)` は何か。

## 参考リンク

- Cramér–Rao bound: https://en.wikipedia.org/wiki/Cram%C3%A9r%E2%80%93Rao_bound
- Fisher information: https://en.wikipedia.org/wiki/Fisher_information
- Exponential distribution: https://en.wikipedia.org/wiki/Exponential_distribution
