---
title: Задачи RMQ и LCA
description: Катастрофически западает солнце
date: 2019-03-09T04:07:12Z
draft: false
katex: true
mermaid: true
---

<style>
    .w-25 {
        width: 25%;
        margin-left: auto;
        margin-right: auto;
    }
</style>

{{<equation class="hidden">}}
    \gdef\rmq{\mathop{\mathrm{rmq}}}
    \gdef\lca{\mathop{\mathrm{lca}}}
    \gdef\new{\mathop{\mathrm{new}}}
{{</equation>}}

{{<slide title="Задачи RMQ и LCA" class="clear" shout="true"/>}}

{{<slide title="План" class="toc" id="toc">}}
1. [задача и применение](#problem)
2. [RMQ -> LCA](#rmq_to_lca)
3. [offline LCA](#offline_lca)
4. [online RMQ](#online_rmq)
5. [±1 RMQ](#pm_one_rmq)
6. [LCA -> ±1 RMQ](#lca_to_pm_one_rmq)
{{</slide>}}

{{<slide title="Задача и применение" class="section" id="problem" />}}

{{<slide title="Задача и применение">}}
RMQ (range minimum query) Выбор наименьшего элемента в отрезке индексов.

**Дано:** \\(A = \\{a\_k \colon k < n \\}\\).

**Операции:**
- \\(\rmq(i, j) = \min\\{a\_k \colon i \leqslant k \leqslant j\\}\\).
{{</slide>}}

{{<slide title="Задача и применение">}}
LCA (less common ancestor) Выбор ближайшего общего предка.

**Дано:** дерево.

**Операции:**
- \\(\lca(u, v) = w\\) такое, что \\(u \ll w\\), \\(v \ll w\\) и для любого \\(t \ll w\\) следует, что либо \\(u \not\ll t\\), либо \\(v \not\ll t\\).
{{</slide>}}

{{<slide title="Задача и применение">}}
{{<mermaid>}}
graph TD
    A(( ))
    A --- B(( ))
    A --- C((w))
    A --- D(( ))
    B --- E(( ))
    C --- F(( ))
    C --- G(( ))
    C --- H(( ))
    D --- I(( ))
    F --- J((u))
    F --- K(( ))
    H --- L((v))
{{</mermaid>}}
{{</slide>}}

{{<slide title="Задача и применение">}}
Применение:
- суффиксное дерево;
- суффиксный массив;
- поиск по образцу;
- поисковые индексы;
{{</slide>}}

{{<slide title="RMQ -> LCA" class="section" id="rmq_to_lca" />}}

{{<slide title="RMQ -> LCA">}}
Для элементов массива \\(A\\) определим
- ключ: \\(k(a\_k) = k\\);
- приоритет: \\(p(a\_k) = a\_k\\);

Построим декартово дерево (\\(O(n)\\)):
- дерево поиска по ключам;
- куча по приоритету;
{{</slide>}}

{{<slide title="RMQ -> LCA">}}
{{<equation>}}
    \{9, 8, 12, 3, 5, 7, 17\}
{{</equation>}}

{{<mermaid clear="true" class="next">}}
graph TD
    A((3))
    A --- B((8))
    A --- C((5))
    B --- D((9))
    B --- E((12))
    C --- F(( ))
    C --- G((7))
    G --- H(( ))
    G --- I((17))
{{</mermaid>}}
{{</slide>}}

{{<slide title="Offline LCA" class="section" id="offline_lca" />}}

{{<slide title="Offline LCA">}}
Пусть все запросы известны заранее

{{<equation>}}
    (x_1, y_1), (x_2, y_2), \ldots, (x_m, y_m)
{{</equation>}}

Найдём все ответы за один проход по дереву (Tarjan).
1. Для каждой вершины выпишем все пары, с её участием.
2. Будем использовать post-order обход.
3. По мере обхода будем строить DDF.
{{</slide>}}

{{<slide title="Offline LCA">}}
{{<mermaid>}}
graph TD
    A(( ))
    A --- B{ }
    A --- C(( ))
    A --- D{ }
    C --- E{ }
    C --- F{ }
    C --- G(( ))
    C --- H{ }
    G --- I{ }
    G --- J{x}
    G --- K{ }
    G --- L{ }

    classDef zero  fill:tomato
    classDef one   fill:darkorange
    classDef two   fill:gold
    classDef three fill:chartreuse

    class A,B zero
    class C,E,F one
    class G,I two
    class J three
{{</mermaid>}}
{{</slide>}}

{{<slide title="Offline LCA">}}
При рассмотрении вершины \\(x\\) пройдёмся по всем парам с её участием.

Рассмотрим только те пары, где вторая вершина \\(y\\) уже просмотрена.

Решением этой пары будет корень дерева, содержащего \\(y\\).
{{</slide>}}

{{<slide title="Offline LCA">}}
Сложность предпросчёта будет

{{<equation>}}
    O(nm\log^\star n) \approx O(nm)
{{</equation>}}
{{</slide>}}

{{<slide title="Online RMQ" class="section" id="online_rmq" />}}

{{<slide title="Online RMQ">}}
Можно подсчитать результат для всех возможных запросов

{{<equation>}}
    T(\new) = O(n^2),\qquad T(\rmq) = O(1), \qquad M = O(n^2).
{{</equation>}}

Можно оставить только столбцы с номерами вида \\(2^k\\)

{{<equation>}}
    T(\new) = O(n\log n),\qquad T(\rmq) = O(1), \qquad M = O(n\log n).
{{</equation>}}
{{</slide>}}

{{<slide title="Online RMQ">}}
\\(\rmq(i, j)\\)
- \\(j - i = 2^k\\) --- результат уже есть в таблице
- выберем \\(k = \max\\{\ell \colon j - i > 2^\ell\\}\\), возьмём из таблицы \\(\rmq(i, i + 2^k)\\) и \\(\rmq(j - 2^k, j)\\). Выберем из них минимум.
{{</slide>}}

{{<slide title="±1 RMQ" class="section" id="pm_one_rmq" />}}

{{<slide title="±1 RMQ">}}
Добавим ограничение: \\(|a\_k - a\_{k+1}| = 1\\) для \\(k < n - 1\\).

{{<equation>}}
    \{35, 34, 33, 34, 35, 34, 35, 36, 37, \ldots\}
{{</equation>}}
{{</slide>}}

{{<slide title="±1 RMQ">}}
Разобьём \\(A\\) на блоки \\(B_\ell\\) размера \\(b\\):

{{<equation>}}
    A = B_1 + B_2 + \ldots + B_{\lceil n/b \rceil}.
{{</equation>}}

{{<equation>}}
    m_\ell = \min(B_\ell)
{{</equation>}}

Логарифмическая таблица:

{{<equation>}}
    T(\new) = O(n\frac{n}{b} + \frac{n}{b}\log\frac{n}{b}),
    \qquad
    M = O(\frac{n}{b}\log\frac{n}{b}).
{{</equation>}}
{{</slide>}}

{{<slide>}}
Запросы \\(\rmq(i, j)\\) делятся на 2 типа:
- \\(i\\) и \\(j\\) лежат в одном блоке;

![Запрос RMQ внутри блока](../img/in_block.svg)

- \\(i\\) и \\(j\\) лежат в разных блоках:

![Запрос RMQ с головой, телом и хвостом](../img/head-tail.svg)
{{</slide>}}

{{<slide title="±1 RMQ">}}
Сигнатура блока:

{{<equation>}}
    \{35, 34, 33, 34, 35, 34, 35, 36, 37\}
{{</equation>}}
{{<equation>}}
    (35, 00110111)
{{</equation>}}

Построим таблицы для всех сигнатур: \\(2^{b - 1} \times b \times b\\)
{{</slide>}}

{{<slide title="±1 RMQ">}}
Итого расход по памяти:

{{<equation>}}
    \underbrace{2^{b-1} b^2}_{\mathclap\text{куб таблиц по сигнатурам}} +
    \overbrace{\frac{n}{b}\log\frac{n}{b}}^{\mathclap\text{логарифмическая таблица}} +
    \underbrace{\frac{n}{b}\log b}_{\mathclap\text{соответствие сигнатур}}
{{</equation>}}
{{</slide>}}

{{<slide title="±1 RMQ">}}
Итого расход по памяти:

{{<equation>}}
    2^{b-1} b^2 + \frac{n}{b}\log\frac{n}{b} + \frac{n}{b}\log b
    = 2^{b-1} b^2 + \frac{n}{b}\log n.
{{</equation>}}

При \\(b = \frac{\log n}{2}\\):

{{<equation>}}
    O(\sqrt n \log^2 n + n) \approx O(n)
{{</equation>}}
{{</slide>}}

{{<slide title="LCA -> ±1 RMQ" class="section" id="lca_to_pm_one_rmq" />}}

{{<slide title="LCA -> ±1 RMQ">}}
{{<mermaid>}}
graph TD
    A((3))
    A --- B((8))
    A --- C((5))
    B --- D((9))
    B --- E((12))
    C --- F((14))
    C --- G((7))
{{</mermaid>}}
{{</slide>}}

{{<slide title="LCA -> ±1 RMQ">}}
{{<mermaid clear="true" class="w-25">}}
graph TD
    A((3))
    A --- B((8))
    A --- C((5))
    B --- D((9))
    B --- E((12))
    C --- F((14))
    C --- G((7))
{{</mermaid>}}

{{<equation>}}
    3 \to 8 \to 9 \to 8 \to 12 \to 8 \to 3 \to 5 \to 14 \to 5 \to 7 \to 5 \to 3
{{</equation>}}
{{</slide>}}

{{<slide title="LCA -> ±1 RMQ">}}
{{<mermaid clear="true" class="w-25">}}
graph TD
    A((3))
    A --- B((8))
    A --- C((5))
    B --- D((9))
    B --- E((12))
    C --- F((14))
    C --- G((7))
{{</mermaid>}}

{{<equation>}}
    9 \to 8 \to 12 \to 8 \to 3 \to 5 \to 14 \to 5 \to 7
{{</equation>}}
{{</slide>}}

{{<slide title="LCA -> ±1 RMQ">}}
{{<mermaid clear="true" class="w-25">}}
graph TD
    A((3))
    A --- B((8))
    A --- C((5))
    B --- D((9))
    B --- E((12))
    C --- F((14))
    C --- G((7))
{{</mermaid>}}

{{<equation>}}
    9 \to 8 \to 12 \to 8 \to 3 \to 5 \to 14 \to 5 \to 7
{{</equation>}}

Рассмотрим последовательность глубин:

{{<equation>}}
    3 \to 2 \to 3 \to 2 \to 1 \to 2 \to 3 \to 2 \to 3
{{</equation>}}
{{</slide>}}

{{<slide title="LCA -> ±1 RMQ">}}
{{<mermaid clear="true" class="w-25">}}
graph TD
    A((3))
    A --- B((8))
    A --- C((5))
    B --- D((9))
    B --- E((12))
    C --- F((14))
    C --- G((7))

    classDef zero  color:tomato
    classDef one   color:steelblue
    classDef two   color:blueviolet

    class E zero
    class C one
    class A two
{{</mermaid>}}

{{<equation>}}
    9 \to 8 \to \textcolor{tomato}{12} \to 8 \to \textcolor{blueviolet}{3} \to \textcolor{steelblue}{5} \to 14 \to \textcolor{steelblue}{5} \to 7
{{</equation>}}

Рассмотрим последовательность глубин:

{{<equation>}}
    3 \to 2 \to \textcolor{tomato}{3} \to 2 \to \textcolor{blueviolet}{1} \to \textcolor{steelblue}{2} \to 3 \to \textcolor{steelblue}{2} \to 3
{{</equation>}}
{{</slide>}}
