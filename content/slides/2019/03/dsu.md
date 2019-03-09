---
title: Семейство непересекающихся множеств
description: Мы всем поддерживаем кайф, нам кайф ломают кругом
date: 2019-03-08T14:57:14Z
draft: false
katex: true
mermaid: true
---

{{<slide title="DSU" class="clear" shout="true"/>}}
{{<slide title="Семейство непересекающихся множеств" class="section" />}}

{{<slide title="План" class="toc" id="toc">}}
1. [задача и применение](#problem)
2. [ранговая эвристика](#rank-heuristic)
3. [сжатие путей](#path-compression)
4. [статистики](#statistics)
5. [динамический направленный лес](#ddf)
6. [вариант реализации](#implementation)
{{</slide>}}

{{<slide title="Задача и применение" class="section" id="problem" />}}

{{<slide title="Задача и применение">}}
Дано множество \\(E = \\{x\_i\colon i < n\\}\\) --- _Универсум_.

В каждый момент времени существует разбиение

{{<equation>}}
    \mathbb X = \{X_j \colon j < k\}
{{</equation>}}

такое, что

{{<equation>}}
    \cup \mathbb X = E,
    \quad\text{и}\quad
    X_j \cap X_l = \varnothing
    \quad(i \neq j)
{{</equation>}}
{{</slide>}}

{{<slide title="Задача и применение">}}
На семействе \\(\mathbb X\\) определим 2 операции:

{{<equation>}}
    \mathrm{Equiv}(x, y) =
    \begin{cases}
        1,& \exist\ X\in\mathbb X\colon x, y \in X,\\
        0,& \text{иначе}
    \end{cases}
{{</equation>}}
{{<equation>}}
    \mathrm{Unite}(x, y) =
    \begin{cases}
        \mathbb X,\ \ \;\mathrm{Equiv}(x, y),\\
        \mathbb X \setminus \{X, Y\} \cup \{X \cup Y\},
    \end{cases}
{{</equation>}}
{{</slide>}}

{{<slide title="Задача и применение">}}
Находит применение в решении задач
- построение минимального остова (алгоритм Краскала);
- Offline LCA (алгоритм Таржина);
- геометрический поиск;
- построение графов и деревьев;
{{</slide>}}

{{<slide title="Ранговая эвристика" class="section" id="rank-heuristic" />}}

{{<slide title="Ранговая эвристика">}}
Будем хранить компоненты связанности в виде деревьев. На них определим операцию \\(\mathrm{GetRoot}(x)\\), возвращающую корень дерева, в котором содержится \\(x\\).

Для каждой вершины поставим в соответствие её родителя \\(\mathrm{Parent}(x)\\). Для корней родитель не определён (\\(\varnothing\\)).
{{</slide>}}

{{<slide title="Ранговая эвристика">}}
{{<equation>}}
    \mathrm{Equiv}(x, y) = [\mathrm{GetRoot}(x) = \mathrm{GetRoot}(y)];
{{</equation>}}
{{<equation>}}
    \mathrm{Unite}(x, y) = \begin{cases}
        \mathrm{Parent}(\mathrm{GetRoot}(x)) = \mathrm{GetRoot}(y)],\\
        \mathrm{Parent}(\mathrm{GetRoot}(y)) = \mathrm{GetRoot}(x)];
    \end{cases}
{{</equation>}}

Как выбрать корень нового дерева?
{{</slide>}}

{{<slide title="Ранговая эвристика">}}
Для каждого дерева определим ранг как высота этого дерева минус 1

{{<equation>}}
    r(X) = h(X) - 1.
{{</equation>}}

Тогда в качестве нового корня выберем дерево с большим рангом.

{{<equation>}}
    r(X \cup Y) = \begin{cases}
        r(X) + 1,& r(X) = r(Y),\\
        \max\{r(X), r(Y)\},\\
    \end{cases}
{{</equation>}}
{{</slide>}}

{{<slide title="Ранговая эвристика">}}
{{<equation>}}
    \begin{gathered}
        T(\mathrm{Equiv}) = O(\max\{h(X) \colon X \in \mathbb X\}),\\
        T(\mathrm{Unite}) = O(\max\{h(X) \colon X \in \mathbb X\}),\\
    \end{gathered}
{{</equation>}}

{{<theorem type="Утверждение" class="next">}}
Высота деревьев логарифмически зависит от количества элементов, т.е. \\(w(X) \geqslant 2^{r(X)}\\).
{{</theorem>}}
{{</slide>}}

{{<slide title="Ранговая эвристика">}}
1. \\(r({x}) = 0\\), \\(w({x}) = 1\\).
2. Пусть \\(X\\) и \\(Y\\) такие, что \\(w(X) \geqslant 2^{r(X)}\\) и \\(w(Y) \geqslant 2^{r(Y)}\\).
3. - Если \\(r(X) < r(Y)\\), тогда \\(r(X \cup Y) = r(X)\\), следовательно \\(w(X \cup Y) \geqslant 2^{r(X, Y)}\\).

    - Если \\(r(X) = r(Y)\\), тогда

{{<equation>}}
    w(X \cup Y) = w(X) + w(Y) \geqslant 2^{r(X)} + 2^{r(Y)} = 2^{r(X) + 1} = 2^{r(X \cup Y)}
{{</equation>}}
{{</slide>}}

{{<slide title="Ранговая эвристика">}}
{{<equation>}}
    \begin{gathered}
        T(\mathrm{Equiv}) = O(\log n),\\
        T(\mathrm{Unite}) = O(\log n),\\
    \end{gathered}
{{</equation>}}

Можно не запоминать ранги, используя вместо них рандомизацию. Получим рандомизированный логарифм.
{{</slide>}}

{{<slide title="Сжатие путей" class="section" id="path-compression" />}}

{{<slide title="Сжатие путей">}}
После применения операции \\(\mathrm{GetRoot}(x)\\) выполним операцию \\(\mathrm{Squash}(x, root)\\).

```python
def squash(x, root):
    p = x.parent
    if p != root:
        x.parent = root
        return squash(p, root)
```
{{</slide>}}

{{<slide title="Сжатие путей">}}
{{<equation>}}
    T(\mathrm{GetRoot}) = O(\log^\star n).
{{</equation>}}
{{<equation class="next">}}
    \log^\star 1 = 0,\quad
    \log^\star 2 = 1,\quad
    \log^\star 4 = 2,\quad
    \log^\star 16 = 3,
{{</equation>}}
{{<equation class="next">}}
    \log^\star 65536 = 4,
{{</equation>}}
{{<equation class="next">}}
    \log^\star 2^{65536} = 5,
{{</equation>}}
{{</slide>}}

{{<slide title="Статистики" class="section" id="statistics" />}}

{{<slide title="Статистики">}}
- количество / сумма;
- максимум / минимум;
- цвет / класс;
{{</slide>}}

{{<slide title="Статистики">}}
Храниться только в корнях.

Важно задать правила по которым будет определяться статистика после слияния.
{{</slide>}}

{{<slide title="Динамический направленный лес" class="section" id="ddf" />}}

{{<slide title="Динамический направленный лес">}}
Лес с двумя операциями:
- \\(\mathrm{GetRoot}(x)\\) --- будем хранить корень как статистику;
- \\(\mathrm{AddEdge}(x, y)\\) --- разрешено, если \\(y\\) является корнем и \\(\mathrm{GetRoot}(x) \neq \mathrm{GetRoot}(y)\\).
{{</slide>}}

{{<slide title="Вариант реализации" class="section" id="implementation" />}}

{{<slide title="Вариант реализации">}}
Массив с индексами родителей.

Для корней можно хранить отрицательное число, в котором кодировать ранг или статистику.

Также можно добавлять новые элементы.
{{</slide>}}
