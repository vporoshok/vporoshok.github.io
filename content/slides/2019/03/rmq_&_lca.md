---
title: Задачи RMQ и LCA
description: Катастрофически западает солнце
date: 2019-03-09T04:07:12Z
draft: false
katex: true
mermaid: true
---

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

{{<mermaid class="next">}}
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
    C --- F(( ))
    C --- G{ }
    F --- H{ }
    F --- I{ }
    F --- J(( ))
    J --- K{ }
    J --- L{x}
    J --- M{ }

    classDef zero  fill:tomato
    classDef one   fill:darkorange
    classDef two   fill:gold
    classDef three fill:chartreuse
    classDef four  fill:turquoise

    class A,B zero
    class C,E one
    class F,H,I two
    class J,K three
    class L four
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
