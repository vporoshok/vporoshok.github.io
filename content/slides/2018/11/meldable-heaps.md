---
title: Кучи с эффективным слиянием
description: Локоть к локтю, кирпич к стене
date: 2018-11-15T14:00:00Z
draft: false
katex: true
mermaid: true
back: /post/2018/11/meldable-heaps/
---

<style>
    .w-75 {
        width: 75%;
        margin-left: auto;
        margin-right: auto;
    }
    .w-50 {
        width: 50%;
        margin-left: auto;
        margin-right: auto;
    }
    .w-25 {
        width: 25%;
        margin-left: auto;
        margin-right: auto;
    }
</style>

{{<slide title="Кучи с эффективным слиянием" class="clear" shout="true"/>}}

{{<slide title="План" class="toc" id="toc">}}
{{<columns class="two">}}
1. [задача и применение](#problem)
2. [биномиальные кучи](#binomial)
    1. [хранение и адресация](#address)
    2. [слияние](#binomial-meld)
    3. [извлечение минимума](#binomial-min)
3. [левацкие кучи](#leftish)
{{</columns>}}
{{</slide>}}

{{<slide title="Задача и применение" class="section" id="problem" />}}

{{<slide title="Задача и применение">}}
Операция слияния куч находит применение в таких алгоритмах, как многопутевые слияния, поиск кратчайшего пути в графе и других. Вместо добавления новых элементов по одному.
{{</slide>}}

{{<slide title="Биномиальные кучи" class="section" id="binomial" />}}

{{<slide title="Биномиальные кучи">}}
Биномиальная куча
: лес, состоящий из биномиальных деревьев
{{</slide>}}

{{<slide title="Биномиальные деревья">}}
{{<mermaid>}}
graph TD
    subgraph k = 3
    H(( ))
    H --- I(( ))
    H --- J(( ))
    H --- K(( ))
    J --- L(( ))
    K --- M(( ))
    K --- N(( ))
    N --- O(( ))
    end

    subgraph k = 2
    D(( ))
    D --- E(( ))
    D --- F(( ))
    F --- G(( ))
    end

    subgraph k = 1
    B(( ))
    B --- C(( ))
    end

    subgraph k = 0
    A(( ))
    end
{{</mermaid>}}
{{</slide>}}

{{<slide title="Биномиальные деревья">}}
Биномиальное дерево порядка \\(0\\) состоит из одной вершины, а биномиальное дерево порядка \\(k\\) является объединением двух деревьев порядка \\(k - 1\\) так, что корень одного из них является сыном корня другого.
{{</slide>}}

{{<slide title="Биномиальные кучи">}}
{{<equation>}}
\tbinom{5}{i} = (1, 5, 10, 10, 5, 1)
{{</equation>}}
{{<mermaid>}}
graph TD
    A(( ))

    A --- B(( ))
    A --- C(( ))
    A --- D(( ))
    A --- E(( ))
    A --- F(( ))

    C --- G(( ))
    D --- H(( ))
    D --- J(( ))
    E --- I(( ))
    E --- K(( ))
    E --- L(( ))
    F --- M(( ))
    F --- N(( ))
    F --- O(( ))
    F --- P(( ))

    J --- Q(( ))
    K --- R(( ))
    L --- S(( ))
    L --- T(( ))
    N --- U(( ))
    O --- V(( ))
    O --- W(( ))
    P --- X(( ))
    P --- Y(( ))
    P --- Z(( ))

    T --- a(( ))
    W --- b(( ))
    Y --- c(( ))
    Z --- d(( ))
    Z --- e(( ))

    e --- f(( ))

    classDef zero  fill:LightCoral
    classDef one   fill:SpringGreen
    classDef two   fill:SkyBlue
    classDef three fill:MediumPurple
    classDef four  fill:#b666d2

    class A zero
    class B,C,D,E,F one
    class G,H,J,I,K,L,M,N,O,P two
    class Q,R,S,T,U,V,W,X,Y,Z three
    class a,b,c,d,e four
{{</mermaid>}}
{{</slide>}}

{{<slide title="Хранение и адресация" class="section" id="address" />}}

{{<slide title="Хранение и адресация">}}
Хранение в виде массива
: корень хранится в нулевом элементе и для \\(i\\)-го элемента его дети имеют индексы \\(i + 2^j\\), где \\(j < k_i\\) степени ветвления вершины \\(i\\).
{{</slide>}}

{{<slide title="Хранение и адресация">}}
{{<mermaid class="w-75">}}
graph TD
    A((0))

    A --- B((1))
    A --- C((2))
    A --- D((4))
    A --- E((8))

    C --- F((3))
    D --- G((5))
    D --- H((6))
    E --- J((9))
    E --- I((10))
    E --- K((12))

    H --- L((7))
    I --- M((11))
    K --- N((13))
    K --- O((14))

    O --- P((15))

    classDef zero  fill:LightCoral
    classDef one   fill:SpringGreen
    classDef two   fill:SkyBlue
    classDef three fill:MediumPurple
    classDef four  fill:#b666d2

    class A zero
    class B,C,D,E one
    class F,G,H,J,I,K two
    class L,M,N,O three
    class P four
{{</mermaid>}}
{{</slide>}}

{{<slide title="Хранение и адресация">}}
Left-Child, Right-Sibling (LCRS)

{{<mermaid>}}
graph LR
    A(( ))

    A --> B(( ))
    B -.-> C(( ))
    C -.-> D(( ))
    D -.-> E(( ))

    C --> F(( ))
    D --> G(( ))
    G -.-> H(( ))
    E --> J(( ))
    J -.-> I(( ))
    I -.-> K(( ))

    H --> L(( ))
    I --> M(( ))
    K --> N(( ))
    N -.-> O(( ))

    O --> P(( ))

    classDef zero  fill:LightCoral
    classDef one   fill:SpringGreen
    classDef two   fill:SkyBlue
    classDef three fill:MediumPurple
    classDef four  fill:#b666d2

    class A zero
    class B,C,D,E one
    class F,G,H,J,I,K two
    class L,M,N,O three
    class P four
{{</mermaid>}}
{{</slide>}}

{{<slide title="Хранение и адресация">}}
Left-Child, Right-Sibling (LCRS)

{{<mermaid>}}
graph LR
    A(( ))

    A --> B(( ))
    B -.-> C(( ))
    C -.-> D(( ))
    D -.-> A

    C --> E(( ))
    E -.-> C
    D --> F(( ))
    F -.-> G(( ))
    G -.-> D

    G --> H(( ))
    H -.-> G

    classDef zero  fill:LightCoral
    classDef one   fill:SpringGreen
    classDef two   fill:SkyBlue
    classDef three fill:MediumPurple

    class A zero
    class B,C,D one
    class E,F,G two
    class H three
{{</mermaid>}}
{{</slide>}}

{{<slide title="Биномиальные кучи">}}
{{<equation>}}
(3, 12, 7, 4, 5, 2, 8, 9, 21, 1, 15, 24, 19)
{{</equation>}}
{{<equation class="next">}}
13 = 1 + 4 + 8 = 2^0 + 2^2 + 2^3
{{</equation>}}
{{<equation class="next">}}
(3), (12, 7, 4, 5), (2, 8, 9, 21, 1, 15, 24, 19)
{{</equation>}}
{{</slide>}}

{{<slide title="Биномиальные кучи">}}
{{<mermaid class="w-75">}}
graph TD
    subgraph k = 3
    F((2))
    F --- G((8))
    F --- H((9))
    F --- I((21))
    H --- J((1))
    I --- K((15))
    I --- L((24))
    L --- M((19))
    end
    subgraph k = 2
    B((12))
    B --- C((7))
    B --- D((4))
    D --- E((5))
    end
    subgraph k = 0
    A((3))
    end
{{</mermaid>}}
{{</slide>}}

{{<slide title="Биномиальные кучи">}}
{{<mermaid class="w-75">}}
graph TD
    subgraph k = 3
    F((1))
    F --- G((8))
    F --- H((2))
    F --- I((15))
    H --- J((9))
    I --- K((21))
    I --- L((19))
    L --- M((24))
    end
    subgraph k = 2
    B((4))
    B --- C((7))
    B --- D((5))
    D --- E((12))
    end
    subgraph k = 0
    A((3))
    end
{{</mermaid>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч" class="section" id="binomial-meld" />}}

{{<slide title="Слияние биномиальных куч">}}
{{<mermaid>}}
graph TD
    subgraph k = 1
    O((7))
    O --- P((30))
    end
    subgraph k = 0
    N((4))
    end
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч">}}
{{<mermaid>}}
graph TD
    subgraph k = 1
    A((3))
    A --- N((4))
    end
    classDef first fill:SpringGreen
    class A,B,C,D,E,F,G,H,I,J,K,L,M first
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч">}}
{{<mermaid>}}
graph TD
    subgraph k = 2
    A((3))
    A --- N((4))
    A --- O((7))
    O --- P((30))
    end
    classDef first fill:SpringGreen
    class A,B,C,D,E,F,G,H,I,J,K,L,M first
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч">}}
{{<mermaid>}}
graph TD
    subgraph k = 3
    A((3))
    A --- N((4))
    A --- O((7))
    O --- P((30))
    A --- B((4))
    B --- C((7))
    B --- D((5))
    D --- E((12))
    end
    classDef first fill:SpringGreen
    class A,B,C,D,E,F,G,H,I,J,K,L,M first
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч">}}
{{<mermaid class="w-75">}}
graph TD
    subgraph k = 4
    F((1))
    F --- G((8))
    F --- H((2))
    F --- I((15))
    H --- J((9))
    I --- K((21))
    I --- L((19))
    L --- M((24))
    F --- A((3))
    A --- N((4))
    A --- O((7))
    O --- P((30))
    A --- B((4))
    B --- C((7))
    B --- D((5))
    D --- E((12))
    end
    classDef first fill:SpringGreen
    class A,B,C,D,E,F,G,H,I,J,K,L,M first
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч">}}
Результирующий набор деревьев

{{<equation>}}
\begin{array}{r}
  + \begin{array}{r}
        1101\\
          11
    \end{array}\\
    \hline
    \begin{array}{r}
       10000
    \end{array}
\end{array}
{{</equation>}}

<p class="next">Количество деревьев в лесу размера \(n\)?</p>

{{<equation class="next">}}
\leqslant \lfloor 1 + \log n \rfloor
{{</equation>}}
{{</slide>}}

{{<slide title="Слияние биномиальных куч">}}
Слияние двух деревьев операция константной сложности:
- выбрать минимум из двух корней;
- назначить меньший корень родителем большего;

Слияние двух лесов из \\(n\\) и \\(m\\) элементов равна \\(O(\log \max (n, m))\\).

Учётная стоимость вставки равна \\(O(1)\\).
{{</slide>}}

{{<slide title="Извлечение минимума" class="section" id="binomial-min" />}}

{{<slide title="Извлечение минимума">}}
{{<mermaid class="w-75">}}
graph TD
    subgraph k = 4
    F((1))
    F --- G((8))
    F --- H((2))
    F --- I((15))
    H --- J((9))
    I --- K((21))
    I --- L((19))
    L --- M((24))
    F --- A((3))
    A --- N((4))
    A --- O((7))
    O --- P((30))
    A --- B((4))
    B --- C((7))
    B --- D((5))
    D --- E((12))
    end
    classDef first fill:SpringGreen
    class A,B,C,D,E,F,G,H,I,J,K,L,M first
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Извлечение минимума">}}
{{<mermaid class="w-75">}}
graph TD
    subgraph k = 3
    A((3))
    A --- N((4))
    A --- O((7))
    O --- P((30))
    A --- B((4))
    B --- C((7))
    B --- D((5))
    D --- E((12))
    end
    subgraph k = 2
    I((15))
    I --- K((21))
    I --- L((19))
    L --- M((24))
    end
    subgraph k = 1
    H((2))
    H --- J((9))
    end
    subgraph k = 0
    G((8))
    end
    classDef first fill:SpringGreen
    class A,B,C,D,E,F,G,H,I,J,K,L,M first
    classDef second fill:LightCoral
    class N,O,P second
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи" class="section" id="leftish" />}}

{{<slide title="Левацкие кучи">}}
Ранг вершины
: высота полного двоичного поддерева с корнем в этой вершине.

{{<equation>}}
    r(\varnothing) = 0, \qquad r(v) = 1 + \min\{v_l, v_r\},
{{</equation>}}

<p class="next">Дерево будем называть <em>левацким</em>, если в любой его вершине ранг левого сына не меньше ранга правого сына.</p>
{{</slide>}}

{{<slide title="Левацкие кучи">}}
{{<mermaid>}}
graph TD
    A((3))
    A --- B((3))
    A --- C((2))
    B --- D((3))
    B --- E((2))
    C --- F((2))
    C --- G((1))
    D --- H((2))
    D --- I((2))
    E --- J((1))
    E --- K((1))
    F --- L((2))
    F --- M((1))
    G --- N((1))
    G --- O((0))
    H --- P((1))
    H --- Q((1))
    I --- R((1))
    I --- S((1))
    J --- T((1))
    J --- U((0))
    L --- V((1))
    L --- W((1))
    M --- X((1))
    M --- Y((0))
    N --- Z((1))
    N --- a((0))

    classDef zero opacity:0.3,fill:LightCoral
    class O,U,Y,a zero
    classDef one   fill:SpringGreen
    class G,J,K,M,N,P,Q,R,S,T,V,W,X,Z one
    classDef two   fill:SkyBlue
    class C,E,F,H,I,L two
    classDef three fill:MediumPurple
    class A,B,D three
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
{{<mermaid class="w-25">}}
graph TD
    a0((a0))
    a0 --- A0{A0}
    a0 --- a1((a1))
    a1 --- A1{A1}
    a1 --- a2((a2))
    a2 --- A2{A2}
    a2 --- a3((a3))
    a3 --- A3{A3}
    a3 --- a4(( ))
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
Также будем обозначать через \\(x(A, B)\\) дерево с корнем в вершине \\(x\\) с двумя поддеревьями: \\(A\\) и \\(B\\), левым и правым соответственно.

{{<mermaid>}}
graph TD
    x((x))
    x --- A{A}
    x --- B{B}
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
{{<equation>}}
    \def\meld{\operatorname{meld}}

    \begin{gathered}
        \meld(A, \varnothing) = \meld(\varnothing, A) = A,\\
        \\
        \\
        \meld(x(A, B), y(C, D)) = \begin{cases}
            x(A, \meld(B, y(C, D))), &\text{если } x \leqslant y;\\
            y(C, \meld(D, x(A, B))), &\text{иначе}.
        \end{cases}
    \end{gathered}
{{</equation>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
{{<mermaid class="w-50">}}
graph TD
    subgraph &nbsp;
    y((y))
    y --- C{C}
    y --- D{D}
    end
    subgraph &nbsp;
    x((x))
    x --- A{A}
    x --- B{B}
    end
{{</mermaid>}}
{{<mermaid class="w-50 next">}}
graph TD
    subgraph &nbsp;
    y((y))
    y --- C{C}
    y --- D{"D + x(A, B)"}
    end
    subgraph &nbsp;
    x((x))
    x --- A{A}
    x --- B{"B + y(C, D)"}
    end
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
{{<mermaid class="w-50">}}
graph TD
    subgraph B
    b0((2))
    b0 --- B0{B0}
    b0 --- b1((6))
    b1 --- B1{B1}
    b1 --- b2((7))
    b2 --- B2{B2}
    b2 --- b3((12))
    end
    subgraph A
    a0((1))
    a0 --- A0{A0}
    a0 --- a1((3))
    a1 --- A1{A1}
    a1 --- a2((5))
    a2 --- A2{A2}
    a2 --- a3((8))
    end
    classDef A fill:LightCoral
    class a0,a1,a2,a3,A0,A1,A2 A
    classDef B fill:SpringGreen
    class b0,b1,b2,b3,B0,B1,B2 B
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
{{<mermaid class="w-75">}}
graph TD
    subgraph A + B
    c0((1))
    c0 --- C0{A0}
    c0 --- c1((2))
    c1 --- C1{B0}
    c1 --- c2((3))
    c2 --- C2{A1}
    c2 --- c3((5))
    c3 --- C3{A2}
    c3 --- c4((6))
    c4 --- C4{B1}
    c4 --- c5((7))
    c5 --- C5{B2}
    c5 --- c6((8))
    c6 --- C6(( ))
    c6 --- c7((12))
    end
    subgraph B
    b0((2))
    b0 --- B0{B0}
    b0 --- b1((6))
    b1 --- B1{B1}
    b1 --- b2((7))
    b2 --- B2{B2}
    b2 --- b3((12))
    end
    subgraph A
    a0((1))
    a0 --- A0{A0}
    a0 --- a1((3))
    a1 --- A1{A1}
    a1 --- a2((5))
    a2 --- A2{A2}
    a2 --- a3((8))
    end
    classDef A fill:LightCoral
    class a0,a1,a2,a3,A0,A1,A2,c0,C0,c2,C2,c3,C3,c6 A
    classDef B fill:SpringGreen
    class b0,b1,b2,b3,B0,B1,B2,c1,C1,c4,C4,c5,C5,c7 B
    classDef zero opacity:0.3,fill:LightCoral
    class C6 zero
{{</mermaid>}}
{{</slide>}}

{{<slide title="Левацкие кучи">}}
Осталось развернуть.

<p class="next">Сложность слияния: \(O(r(A) + r(B)) = O(\log n)\).</p>
<p class="next">Все операции сводятся к слиянию, кроме decrease_key.</p>
<p class="next">Дополнительная память.</p>
{{</slide>}}

{{<slide title="Косые кучи" class="section" id="skew" />}}
{{<slide title="Рандомизированные кучи" class="section" id="random" />}}

{{<slide title="Дополнительное чтение" id="further">}}
- Vuillemin, Jean. "A data structure for manipulating priority queues." _Communications of the ACM_. vol. 21, no. 4, 1978, pp. 309–315.
- Fredman, Michael L., and al. "The pairing heap: a new form of self-adjusting heap." _Algorithmica_. vol. 1, no. 1, 1986, pp. 111–129.
- Crane, Clark A. _Linear Lists and Priority Queues as Balanced Binary Trees_ Ph.D. thesis. Department of Computer Science, Stanford University, 1972.
{{</slide>}}

{{<slide title="Дополнительное чтение">}}
- Sleator, Daniel Dominic and Tarjan, Robert Endre. "Self-Adjusting Heaps." _SIAM Journal on Computing_. vol. 15, no. 1, 1986, pp. 52–69.
- Gambin, A. and Malinowski, A. "Randomized Meldable Priority Queues." _Proceedings of the 25th Conference on Current Trends in Theory and Practice of Informatics: Theory and Practice of Informatics (SOFSEM '98)_. Ed. Branislav Rovan, 1998, pp. 344-349.
{{</slide>}}

{{<slide class="clear section" title="Спасибо за внимание" />}}