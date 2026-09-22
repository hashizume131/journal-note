from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


OUT_DIR = Path("output/pdf")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/ARIALUNI.ttf"
pdfmetrics.registerFont(TTFont("ArialUnicode", FONT_PATH))
JP = "ArialUnicode"


def make_styles():
    base = getSampleStyleSheet()
    normal = ParagraphStyle(
        "normal",
        parent=base["Normal"],
        fontName=JP,
        fontSize=9.7,
        leading=15.2,
        wordWrap="CJK",
        spaceAfter=4,
    )
    title = ParagraphStyle(
        "title",
        parent=normal,
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    subtitle = ParagraphStyle(
        "subtitle",
        parent=normal,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#666666"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    h1 = ParagraphStyle(
        "h1",
        parent=normal,
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#174a7c"),
        spaceBefore=8,
        spaceAfter=5,
    )
    h2 = ParagraphStyle(
        "h2",
        parent=normal,
        fontSize=11.2,
        leading=16,
        textColor=colors.HexColor("#222222"),
        spaceBefore=6,
        spaceAfter=3,
    )
    formula = ParagraphStyle(
        "formula",
        parent=normal,
        fontSize=10.2,
        leading=15,
        leftIndent=5,
        rightIndent=5,
        borderWidth=0.5,
        borderColor=colors.HexColor("#c8d8ea"),
        backColor=colors.HexColor("#f4f8fc"),
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5,
    )
    note = ParagraphStyle(
        "note",
        parent=normal,
        fontSize=9.2,
        leading=14,
        textColor=colors.HexColor("#444444"),
        leftIndent=6,
        borderColor=colors.HexColor("#e1d28b"),
        backColor=colors.HexColor("#fff9db"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5,
    )
    cell = ParagraphStyle(
        "cell",
        parent=normal,
        fontSize=7.7,
        leading=10,
        wordWrap="CJK",
    )
    return dict(normal=normal, title=title, subtitle=subtitle, h1=h1, h2=h2, formula=formula, note=note, cell=cell)


S = make_styles()

def clean(text):
    return str(text)


def p(text, style="normal"):
    return Paragraph(clean(text).replace("\n", "<br/>"), S[style])


def f(text):
    return p(text, "formula")


def note(text):
    return p(text, "note")


def bullets(items):
    return [p("・" + item) for item in items]


def heading(story, text, level=1):
    story.append(p(text, "h1" if level == 1 else "h2"))


def tbl(data, widths=None):
    wrapped = []
    for row in data:
        wrapped.append([Paragraph(clean(cell), S["cell"]) for cell in row])
    t = Table(wrapped, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), JP),
                ("FONTSIZE", (0, 0), (-1, -1), 8.2),
                ("LEADING", (0, 0), (-1, -1), 10.5),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9aa4ad")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def page_no(canvas, doc):
    canvas.saveState()
    canvas.setFont(JP, 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(200 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def build(filename, title, subtitle, story):
    path = OUT_DIR / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=16 * mm,
        title=title,
    )
    flows = [p(title, "title"), p(subtitle, "subtitle"), Spacer(1, 4 * mm)] + story
    doc.build(flows, onFirstPage=page_no, onLaterPages=page_no)
    return path.resolve()


def chapter2():
    s = []
    heading(s, "問題一覧とこの章の狙い")
    s.append(p("添付写真で読める第2章の範囲は、問2.1から問2.6を中心にした確率分布の演習です。核になるのは、二項分布の極限、混合分布、分布関数による変数変換、ガンマ分布・ディリクレ分布、正規分布の混合です。"))
    s.append(note("大事な読み方: 密度関数を見たら「積分する」、分布関数を見たら「P(X≤x)に戻す」、混合分布を見たら「条件付き分布×パラメータの分布を積分する」と考えます。"))

    heading(s, "問2.1 二項分布のポアソン近似", 2)
    s.append(p("X∼Bin(M,p) とし、M→∞, p→0 だが Mp→λ となる状況を考えます。これは「試行回数はとても多いが、1回ごとの成功確率は小さい。ただし平均成功回数はλで一定」という場面です。"))
    s.append(f("P(X=x)= C(M,x) p<super>x</super> (1-p)<super>M-x</super>"))
    s.append(p("ここで p=λ/M と置くと、"))
    s.append(f("P(X=x)= [M(M-1)…(M-x+1)/x!] (λ/M)<super>x</super> (1-λ/M)<super>M-x</super>"))
    s.append(p("xを固定してMを大きくすると、M(M-1)…(M-x+1)/M<super>x</super> は 1 に近づきます。また (1-λ/M)<super>M</super> は e<super>-λ</super> に近づきます。したがって、"))
    s.append(f("P(X=x) → e<super>-λ</super> λ<super>x</super> / x!"))
    s.append(p("これは Poisson(λ) の確率関数です。"))
    s.append(note("答案の結論: Bin(M,λ/M) は M→∞ で Poisson(λ) に収束する。近似条件は「Mが大きい」「pが小さい」「Mpが適度な大きさ」です。"))

    heading(s, "問2.2 ポアソン分布とガンマ分布の混合", 2)
    s.append(p("X|Λ=λ ∼ Poisson(λ)、Λ∼Gamma(α,β) とします。λが観測できないので、λについて積分して周辺分布 P(X=x) を求めます。"))
    s.append(f("P(X=x)= ∫<sub>0</sub><super>∞</super> P(X=x|λ) f<sub>Λ</sub>(λ) dλ"))
    s.append(f("= ∫<sub>0</sub><super>∞</super> [e<super>-λ</super> λ<super>x</super>/x!] [β<super>α</super>/Γ(α) λ<super>α-1</super> e<super>-βλ</super>] dλ"))
    s.append(p("指数部分は e<super>-(β+1)λ</super>、λのべきは λ<super>x+α-1</super> です。これはガンマ積分"))
    s.append(f("∫<sub>0</sub><super>∞</super> λ<super>c-1</super> e<super>-dλ</super> dλ = Γ(c)/d<super>c</super>"))
    s.append(p("にそのまま乗ります。よって、"))
    s.append(f("P(X=x)= Γ(x+α)/(x! Γ(α)) ・ (β/(β+1))<super>α</super> ・ (1/(β+1))<super>x</super>"))
    s.append(p("これは負の二項分布の形です。ポアソン分布の平均λが個体ごとに揺らぐと、単純なポアソンよりもばらつきが大きい分布になります。"))
    s.append(note("よくあるミス: P(X=x|λ) だけを書いて終わること。混合分布では必ず λ の分布を掛けて積分します。"))

    heading(s, "問2.3 分布関数による変数変換", 2)
    s.append(p("Fを連続分布の分布関数とします。分布関数の変換では、密度をいきなり微分するより、まず累積確率に戻すと楽です。"))
    s.append(f("P(F<super>-1</super>(U)≤x)=P(U≤F(x))"))
    s.append(p("U∼U(0,1) なら P(U≤F(x))=F(x) なので、X=F⁻¹(U) は分布関数Fを持ちます。これは逆関数法と呼ばれる乱数生成の考え方です。"))
    s.append(p("例として指数分布 F(x)=1-e<super>-λx</super> を考えると、U=F(X) なので、"))
    s.append(f("X=F<super>-1</super>(U)= -(1/λ) log(1-U)"))
    s.append(p("となります。Uを一様乱数として発生させれば、Xは指数分布に従います。"))

    heading(s, "問2.4 ガンマ分布の和と比の分布", 2)
    s.append(p("X₁,X₂,X₃ が独立で Xᵢ∼Gamma(αᵢ,β) のとき、和 T=X₁+X₂+X₃ は Gamma(α₁+α₂+α₃,β) に従います。同じβを持つことがポイントです。"))
    s.append(f("T=X₁+X₂+X₃ ∼ Gamma(α₁+α₂+α₃, β)"))
    s.append(p("さらに比 U₁=X₁/T, U₂=X₂/T, U₃=X₃/T を見ると、U₁+U₂+U₃=1 なので、実質的な自由度は2つです。この比率ベクトルはディリクレ分布になります。"))
    s.append(f("(U₁,U₂,U₃) ∼ Dirichlet(α₁,α₂,α₃)"))
    s.append(p("密度は、和Tを含む変数変換をしてヤコビアンを掛け、Tについて積分することで出ます。計算の見通しは「全体量T」と「割合U」に分けることです。"))

    heading(s, "問2.5 ヤコビアンとディリクレ分布", 2)
    s.append(p("変数変換で最も落としやすいのがヤコビアンです。例えば x₁=t u₁, x₂=t u₂, x₃=t(1-u₁-u₂) のように置くと、元の密度 f(x₁,x₂,x₃) に |J| を掛けます。"))
    s.append(f("変換後の密度 = 元の密度 × |∂(x₁,x₂,x₃)/∂(t,u₁,u₂)|"))
    s.append(p("この計算を通すと、tに関する部分とuに関する部分が分離します。tの部分はガンマ分布、uの部分はディリクレ分布になります。"))
    s.append(note("答案での書き方: 変数変換を宣言する → ヤコビアンを書く → 密度を代入する → tについて積分する → ディリクレ分布の密度を得る、の順に書くと読みやすいです。"))

    heading(s, "問2.6 正規分布のガンマ混合", 2)
    s.append(p("X|Θ=θ ∼ N(0,1/θ)、Θ∼Gamma(p/2,p/2) のような混合を考えます。まずθを固定して正規分布として扱い、その後θの分布で平均します。"))
    s.append(f("E[X]=E{E[X|Θ]}=E[0]=0"))
    s.append(f("V[X]=E{V[X|Θ]} + V{E[X|Θ]} = E[1/Θ]"))
    s.append(p("Θ∼Gamma(a,b) のとき a>1 なら E[1/Θ]=b/(a-1) です。ここでは a=p/2, b=p/2 なので、p>2 のとき"))
    s.append(f("V[X] = (p/2)/(p/2-1) = p/(p-2)"))
    s.append(p("このような混合正規分布は、普通の正規分布より裾が重くなります。極端な値が出やすいデータを扱うときに現れます。"))

    heading(s, "第2章のまとめ")
    s.extend(bullets([
        "極限分布は、確率関数の各因子が何に近づくかを見る。",
        "混合分布は、条件付き分布とパラメータ分布を掛けて積分する。",
        "分布関数の変換は、P(変換後の変数≤値)に戻す。",
        "ガンマ分布の和・比は、和Tと割合Uに分けると見通しがよい。",
    ]))
    return build("statistics_chapter2_explanation.pdf", "統計学 第2章 演習解説ノート 改訂版", "確率分布・変数変換・混合分布を、問題ごとの答案の形で整理", s)


def chapter3():
    s = []
    heading(s, "問題一覧とこの章の狙い")
    s.append(p("第3章は推定論です。添付写真で読める範囲では、問3.1が変数変換と不偏推定・一致推定・クラメール・ラオ下限、問3.2が指数分布の最尤推定・フィッシャー情報量・デルタ法です。"))
    s.append(note("推定論の見方: 推定量を見たら、まず期待値で不偏性、分散の極限で一致性、尤度の微分で最尤推定量、2階微分で情報量を確認します。"))

    heading(s, "問3.1(1) Y=log(1+X) の密度", 2)
    s.append(p("密度 f(x;θ)=θ(1+x)<super>-(1+θ)</super>, x&gt;0 をもつXについて、Y=log(1+X) と変換します。まず逆変換とヤコビアンを書きます。"))
    s.append(f("Y=log(1+X)  ⇔  X=e<super>y</super>-1,    dx/dy=e<super>y</super>"))
    s.append(p("密度変換の公式 g(y)=f(e<super>y</super>-1;θ)・e<super>y</super> を使うと、"))
    s.append(f("g(y)=θ(1+e<super>y</super>-1)<super>-(1+θ)</super> e<super>y</super>"))
    s.append(f("= θ(e<super>y</super>)<super>-(1+θ)</super>e<super>y</super> = θe<super>-θy</super>,   y&gt;0"))
    s.append(p("したがって、Yはパラメータθの指数分布 Exp(θ) に従います。"))

    heading(s, "問3.1(2) Tが1/θの一致推定量であること", 2)
    s.append(p("T=(1/n)Σ log(1+X<sub>i</sub>)=(1/n)ΣY<sub>i</sub> と書けます。Y<sub>i</sub>∼Exp(θ) なので、"))
    s.append(f("E[Y<sub>i</sub>]=1/θ,    V[Y<sub>i</sub>]=1/θ<super>2</super>"))
    s.append(f("E[T]=1/θ,    V[T]=1/(nθ<super>2</super>)"))
    s.append(p("Tの平均は1/θで、分散はnが大きくなると0に近づきます。チェビシェフの不等式を使うと、任意のε>0について"))
    s.append(f("P(|T-1/θ|≥ε) ≤ V[T]/ε<super>2</super> = 1/(nθ<super>2</super>ε<super>2</super>) → 0"))
    s.append(p("よって T は 1/θ の一致推定量です。"))

    heading(s, "問3.1(3) Tが不偏推定量でCR下限を達成すること", 2)
    s.append(p("不偏性は期待値を見ればすぐ分かります。"))
    s.append(f("E[T]=E[(1/n)ΣY<sub>i</sub>]=(1/n)ΣE[Y<sub>i</sub>]=1/θ"))
    s.append(p("次にクラメール・ラオ下限を見ます。推定したい量を τ(θ)=1/θ とします。指数分布1個あたりのフィッシャー情報量は I(θ)=1/θ<super>2</super>、n個では n/θ<super>2</super> です。"))
    s.append(f("τ'(θ)= -1/θ<super>2</super>"))
    s.append(f("CR下限 = {τ'(θ)}<super>2</super> / I<sub>n</sub>(θ) = (1/θ<super>4</super>)/(n/θ<super>2</super>)=1/(nθ<super>2</super>)"))
    s.append(p("これは V[T]=1/(nθ<super>2</super>) と一致します。したがってTは不偏で、しかもCR下限を達成する効率的な推定量です。"))
    s.append(note("よくあるミス: 1/θを推定しているのに、θそのもののCR下限を使ってしまうこと。推定対象がτ(θ)なら、τ'(θ)が必要です。"))

    heading(s, "問3.2(1) 標本平均の期待値と分散", 2)
    s.append(p("X<sub>1</sub>,…,X<sub>n</sub>∼Exp(λ) とします。指数分布の基本性質は E[X]=1/λ, V[X]=1/λ<super>2</super> です。標本平均 X̄=T/n について、"))
    s.append(f("E[X̄]=1/λ"))
    s.append(f("V[X̄]=V((1/n)ΣX<sub>i</sub>)=1/n<super>2</super>・ΣV[X<sub>i</sub>]=1/(nλ<super>2</super>)"))

    heading(s, "問3.2(2) λの最尤推定量", 2)
    s.append(p("観測値を x<sub>1</sub>,…,x<sub>n</sub>、和を t=Σx<sub>i</sub> とします。尤度は"))
    s.append(f("L(λ)=Π λe<super>-λx<sub>i</sub></super> = λ<super>n</super> e<super>-λt</super>"))
    s.append(p("対数を取ると、"))
    s.append(f("ℓ(λ)=n log λ - λt"))
    s.append(p("微分して0と置きます。"))
    s.append(f("dℓ/dλ = n/λ - t = 0"))
    s.append(f("λ̂ = n/t = 1/X̄"))
    s.append(p("指数分布では平均待ち時間が1/λなので、標本平均の逆数が発生率λの推定量になります。"))

    heading(s, "問3.2(3) フィッシャー情報量", 2)
    s.append(p("対数尤度をもう一度微分すると、"))
    s.append(f("d<super>2</super>ℓ/dλ<super>2</super> = -n/λ<super>2</super>"))
    s.append(p("したがって、フィッシャー情報量は"))
    s.append(f("I<sub>n</sub>(λ)= -E[d<super>2</super>ℓ/dλ<super>2</super>] = n/λ<super>2</super>"))
    s.append(p("情報量がnに比例して増えるのは、独立な観測が増えるほど母数についての情報が増えるからです。"))

    heading(s, "問3.2(4) デルタ法による λ̂ の漸近分散", 2)
    s.append(p("λ̂=1/X̄ なので、g(x)=1/x を X̄ にかけたものと見ます。X̄ の中心は μ=E[X]=1/λ です。"))
    s.append(f("g'(x)= -1/x<super>2</super>,    g'(μ)= -1/(1/λ)<super>2</super> = -λ<super>2</super>"))
    s.append(p("デルタ法より、"))
    s.append(f("V(g(X̄)) ≈ {g'(μ)}<super>2</super> V(X̄)"))
    s.append(f("= λ<super>4</super> ・ 1/(nλ<super>2</super>) = λ<super>2</super>/n"))
    s.append(p("したがって λ̂ の漸近分散は λ<super>2</super>/n です。これは最尤推定量の漸近分散 1/I<sub>n</sub>(λ)=λ<super>2</super>/n と一致します。"))

    heading(s, "提出答案で使える短いまとめ")
    s.append(tbl([
        ["問題", "結論", "見るポイント"],
        ["3.1(1)", "Y=log(1+X)∼Exp(θ)", "逆変換 X=eʸ-1 とヤコビアン eʸ"],
        ["3.1(2)", "Tは1/θの一致推定量", "E[T]=1/θ, V[T]→0"],
        ["3.1(3)", "Tは不偏でCR下限達成", "CR下限={τ'(θ)}²/Iₙ(θ)"],
        ["3.2", "λ̂=n/T=1/X̄, Iₙ(λ)=n/λ², AVar(λ̂)=λ²/n", "尤度微分とデルタ法"],
    ], [22 * mm, 78 * mm, 70 * mm]))
    s.append(PageBreak())
    heading(s, "具体例で確認")
    s.append(p("指数分布の観測値が 2,1,3,4 だったとします。n=4, t=10, X̄=2.5 です。"))
    s.append(f("λ̂=n/t=4/10=0.4"))
    s.append(p("平均待ち時間は約2.5、発生率はその逆数0.4という解釈です。もし標本数が増えれば、X̄は1/λに近づき、λ̂=1/X̄もλに近づきます。"))
    heading(s, "よくあるミス")
    s.extend(bullets([
        "T=ΣXᵢ と X̄=T/n を混同する。λ̂は n/T = 1/X̄。",
        "不偏性と一致性を同じものとして扱う。不偏性は期待値、一致性は標本数を増やした極限。",
        "CR下限で、推定対象τ(θ)=1/θの微分を入れ忘れる。",
        "デルタ法で g'(μ) ではなく g'(λ) を使ってしまう。",
    ]))
    return build("statistics_chapter3_explanation.pdf", "統計学 第3章 演習解説ノート 改訂版", "推定量・最尤推定・フィッシャー情報量・デルタ法", s)


def chapter6():
    s = []
    heading(s, "問題一覧とこの章の狙い")
    s.append(p("第6章は多変量解析です。添付写真で読める範囲では、問6.1が英語テストのListening・Readingと期末試験Score(Y)の重回帰分析、問6.2が5科目成績の主成分分析です。ここでは計算結果を『統計を知らない人にも説明できる』形に読む練習が中心です。"))

    heading(s, "問6.1(1) 重回帰モデルの仮定", 2)
    s.append(p("モデルは次の形です。"))
    s.append(f("Y<sub>i</sub> = β + β<sub>1</sub>x<sub>1i</sub> + β<sub>2</sub>x<sub>2i</sub> + ε<sub>i</sub>"))
    s.append(p("ここで x<sub>1</sub> はListening、x<sub>2</sub> はReading、Yは期末試験の点数です。通常置かれる仮定は次の通りです。"))
    s.extend(bullets([
        "線形性: Yの平均が β+β<sub>1</sub>x<sub>1</sub>+β<sub>2</sub>x<sub>2</sub> で表せる。",
        "誤差の平均0: E[ε<sub>i</sub>]=0。",
        "等分散性: V[ε<sub>i</sub>]=σ<super>2</super> がどの学生でも同じ。",
        "独立性: 誤差どうしが独立、または少なくとも無相関。",
        "正規性: t検定・F検定を使うとき、誤差が正規分布に従うと仮定することが多い。",
    ]))
    s.append(note("仮定は『係数を計算するため』というより、『p値や信頼区間を信じてよいか』を支える条件です。"))

    heading(s, "問6.1(2) 重回帰出力の読み取り", 2)
    s.append(p("写真の重回帰結果では、重相関係数0.793、決定係数0.629、自由度調整済み決定係数0.523が示されています。"))
    s.append(f("R<super>2</super>=0.629"))
    s.append(p("これは、Score(Y)のばらつきの約62.9%をListeningとReadingの2変数で説明できている、という意味です。自由度調整済みR²が0.523まで下がるのは、説明変数を2つ入れているのに対して標本数が10と小さいためです。"))
    s.append(p("分散分析表では、回帰のF値が5.926、p値が0.031です。"))
    s.append(f("F=5.926,  p=0.031 < 0.05"))
    s.append(p("したがって5%水準では、モデル全体としてはScore(Y)を説明する力があると判断できます。"))
    s.append(tbl([
        ["係数", "推定値", "p値", "読み取り"],
        ["切片", "-1.938", "0.931", "Listening=0, Reading=0のときの予測値。現実的範囲外なので重視しない。"],
        ["Listening", "0.099", "0.457", "Readingを固定すると、Listeningが1点高い学生はYが約0.099点高いと予測される。ただし有意ではない。"],
        ["Reading", "0.194", "0.141", "Listeningを固定すると、Readingが1点高い学生はYが約0.194点高いと予測される。ただし有意ではない。"],
    ], [22 * mm, 22 * mm, 18 * mm, 105 * mm]))
    s.append(note("モデル全体のp値は有意なのに、個別係数は有意でない。このズレは、ListeningとReadingが似た情報を持つため、どちらの独自効果かを分けにくいときに起こります。"))

    heading(s, "問6.1(3) 単回帰との比較", 2)
    s.append(p("写真では『Listeningのみ』『Readingのみ』『Totalのみ』で回帰した結果もあります。p値は概略としてListeningのみ0.026、Readingのみ0.009、Totalのみ0.007で、単独では有意に見えます。"))
    s.append(p("しかし重回帰ではListeningとReadingを同時に入れるため、『Readingの点数が同じ学生どうしで、Listeningだけが違うとき』という独自効果を見ます。このとき有意でなくなるのは矛盾ではありません。"))
    s.append(p("TotalはListening+Readingなので、1つの総合指標としては分かりやすいです。一方、重回帰はListeningとReadingのどちらが効いていそうかを分けて見たいときに使います。ただしn=10なので、強い結論は避けます。"))

    heading(s, "問6.1の説明例", 2)
    s.append(note("説明例: 入学時の英語テストは期末試験の点数と関連している。ListeningとReadingを合わせたモデルは、期末点のばらつきの約63%を説明し、モデル全体は5%水準で有意である。ただし、ListeningとReadingを同時に入れると個別係数は有意でないため、どちらか一方が明確に効いているとは断定できない。"))

    heading(s, "問6.2 主成分分析の目的", 2)
    s.append(p("5科目の点数には相関があります。主成分分析は、国語・社会・数学・理科・英語の5変数を、情報をなるべく失わずに少数の軸へまとめる方法です。ここでは標準化したデータを使っています。"))
    s.append(note("標準化する理由: 科目ごとの平均や標準偏差が違うと、ばらつきの大きい科目が主成分を支配しやすいからです。標準化すると、各科目を同じ尺度で比べられます。"))

    heading(s, "問6.2 固有値・寄与率・累積寄与率", 2)
    s.append(tbl([
        ["主成分", "固有値", "寄与率", "累積寄与率", "読み取り"],
        ["第1", "3.030", "0.606", "0.606", "全体の60.6%を説明。最も大きい軸。"],
        ["第2", "1.219", "0.244", "0.850", "第1と合わせて85.0%を説明。"],
        ["第3", "0.431", "0.086", "0.936", "追加情報は小さい。"],
        ["第4", "0.178", "0.036", "0.971", "かなり小さい。"],
        ["第5", "0.143", "0.029", "1.000", "残りのわずかな情報。"],
    ], [18 * mm, 19 * mm, 19 * mm, 24 * mm, 85 * mm]))
    s.append(p("第2主成分までで85.0%を説明できるので、5科目の情報を2次元でかなりよく要約できます。"))

    heading(s, "問6.2 固有ベクトルと因子負荷量の読み取り", 2)
    s.append(p("第1主成分の係数は全科目で正です。したがって、第1主成分は『総合学力』の軸と解釈できます。点数が全体的に高い生徒ほど、第1主成分得点が高くなります。"))
    s.append(p("第2主成分では、国語・社会が正、数学・理科が負になっています。したがって、第2主成分は『文系寄りか理系寄りか』を表す軸と考えられます。"))
    s.append(f("主成分得点 = 標準化得点 × 固有ベクトル"))
    s.append(p("因子負荷量は、各科目と主成分の相関のように読めます。係数は主成分得点を作る重み、因子負荷量は元変数との関係の強さです。この2つを混同しないことが大事です。"))

    heading(s, "問6.2 プロットと回転後の解釈", 2)
    s.append(p("第1主成分を横軸、第2主成分を縦軸にして生徒をプロットすると、右に行くほど総合学力が高い生徒、上または下に行くほど科目タイプに偏りがある生徒として読めます。"))
    s.append(p("回転は、軸の意味を解釈しやすくするために行います。回転しても、データの構造を別物にするのではなく、『どの科目群がまとまっているか』を見やすくする操作です。"))

    heading(s, "第6章のよくあるミス")
    s.extend(bullets([
        "R²が高いことを因果関係の証明と考える。回帰はまず関連の分析であり、因果とは別。",
        "モデル全体のF検定と個別係数のt検定を混同する。",
        "単回帰で有意だった変数が重回帰で有意でなくなることを矛盾と考える。",
        "主成分の係数と因子負荷量を同じものとして読む。",
        "主成分の名前を、係数や負荷量を見ずに雰囲気で決める。",
    ]))
    heading(s, "提出答案で使える短い結論")
    s.append(note("問6.1: 入学時英語テストは期末試験点と関連しており、ListeningとReadingの2変数モデルは5%水準で有意である。ただし個別係数は有意でないため、どちらが独自に効いているかは断定できない。"))
    s.append(note("問6.2: 第1主成分は全科目に正の負荷を持つため総合学力、第2主成分は文系科目と理系科目を分ける軸と解釈できる。第2主成分までで約85%を説明できる。"))
    return build("statistics_chapter6_explanation.pdf", "統計学 第6章 演習解説ノート 改訂版", "重回帰分析・主成分分析の出力を答案として読める形に整理", s)


if __name__ == "__main__":
    for created in (chapter2(), chapter3(), chapter6()):
        print(created)
