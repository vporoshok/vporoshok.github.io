---
title: Хеш-таблицы
description: …
date: 2019-03-01T16:43:34Z
draft: false
katex: true
mermaid: true
# back: /post/2018/11/meldable-heaps/
---

<style>
    .red {
        color: red;
    }
</style>

{{<slide title="Хеш-таблицы" class="clear" shout="true"/>}}

{{<slide title="План" class="toc" id="toc">}}
1. [задача и применение](#problem)
2. [неконстантные решения](#non-constant)
3. [хеширование](#hashing)
4. [коллизии](#collision)
5. [анализ сложности с допущениями](#complexity)
6. [без допущений](#real)
{{</slide>}}

{{<slide title="Задача и применение" class="section" id="problem" />}}

{{<slide title="Задача и применение">}}
Есть множество пар \\((k, v)\\) --- ключ-значение. Необходимо построить структуру хранения этих пар так, чтобы на ней были определены операции:
- `set(k, v)`
- `get(k)`
- `delete(k)`
{{</slide>}}

{{<slide title="Неконстантные решения" class="section" id="non-constant" />}}

{{<slide title="Неконстантные решения">}}
<table>
    <col-group>
        <col width="40%">
        <col>
        <col>
        <col>
        <col>
    </col-group>
    <thead>
        <tr>
            <th scope="col">Структура
            <th scope="col"><code>new</code>
            <th scope="col"><code>set</code>
            <th scope="col"><code>get</code>
            <th scope="col"><code>del</code>
    <tbody>
        <tr>
            <th scope="row">Массив
            <td>\(O(n)\)
            <td>\(O(1)\)
            <td class="red">\(O(n)\)
            <td class="red">\(O(n)\)
        <tr class="next">
            <th scope="row">Отсортированный массив
            <td class="red">\(O(n\log n)\)
            <td>\(O(\log n)^\star\)
            <td>\(O(\log n)^\star\)
            <td>\(O(\log n)^\star\)
        <tr class="next">
            <th scope="row">Дерево поиска
            <td>\(O(n)\)
            <td>\(O(\log n)\)
            <td>\(O(\log n)\)
            <td>\(O(\log n)\)
        <tr class="next">
            <th scope="row">Хочется
            <td>\(O(n)\)
            <td>\(O(1)\)
            <td>\(O(1)\)
            <td>\(O(1)\)
</table>
{{</slide>}}

{{<slide title="Хеширование" class="section" id="hashing" />}}

{{<slide title="Хеширование">}}
Выделим массив для хранения пар размера \\(N\\), при этом допустимое множество ключей \\(K\\) такое, что \\(|K| \gg N\\). Определим функциональное отображение

{{<equation>}}
    h\colon K \to N,
{{</equation>}}

с помощью которого будем определять позицию пары. Это отображение называется _хеш-функцией_.
{{</slide>}}

{{<slide title="Коллизии" class="section" id="collision" />}}

{{<slide title="Коллизии">}}
Так как \\(|K| \gg N\\), то существуют \\(k\\) и \\(k^\prime\\) такие, что \\(h(k) = h(k^\prime)\\). Это называется _коллизия_.

<p class="next">То есть две пары с различными ключами претендуют на одну ячейку в массиве.

<p class="next">Также предполагается, что размер \\(K\\) много больше объёма оперативной памяти.
{{</slide>}}

{{<slide title="Методы разрешения коллизий" class="section" />}}

{{<slide title="Прямое связывание">}}
В массиве хранятся указатели на списки, в которых может быть несколько элементов.

![Разрешение коллизий прямым связыванием](../img/chaining.svg)
{{</slide>}}

{{<slide title="Прямое связывание">}}
{{<equation>}}
    T(\mathrm{get})\quad\text{и}\quad T(\mathrm{delete}) = O(n)
{{</slide>}}
{{<equation>}}
    T(\mathrm{set}) = \begin{cases}
        O(1), &\text{ключ без коллизии},\\
        O(n), &\text{иначе}.
    \end{cases}
{{</equation>}}
{{</slide>}}

{{<slide title="Открытая адресация">}}
Определим функцию \\(h(k, i)\\), где \\(i \in \natnums\\) --- номер попытки. При возникновении коллизии будем увеличивать номер попытки.
{{</slide>}}

{{<slide title="Метод линейных проб">}}
{{<equation>}}
    h(k, i) = h(k) + i \mod N
{{</equation>}}

![Разрешение коллизий открытой адресацией с линейными пробами](../img/linear-probe.svg)

**Преимущества:** локальность данных.

**Недостатки:** удаление, рехеширование при переполнении.
{{</slide>}}

{{<slide title="Метод квадратичных проб">}}
{{<equation>}}
    h(k, i) = h(k) + i^2 \mod N
{{</equation>}}
{{<equation>}}
    h(k, i) = h(k, i - 1) + d_{i - 1},
    \quad \text{где} \quad
    d_i = d_{i - 1} + 2, \quad i > 1.
{{</equation>}}

{{<theorem Утверждение>}}
Для \\(i, j < N/2\\) следует, что \\(i^2 \bmod N \neq j^2 \bmod N\\).
{{</theorem>}}
{{</slide>}}

{{<slide title="Общий случай">}}
{{<equation>}}
    h(k, i) = h(k) + g(k)\cdot i \mod N,
{{</equation>}}

где \\(g(k)\\) равномерно распределено.

Для избежания коллизии по попыткам \\(h(k, i) = h(k, j)\\) для \\(i \neq j\\), достаточно, чтобы \\(g(k) \perp N\\). Достаточно чтобы \\(N\\) было простым.
{{</slide>}}

{{<slide title="Анализ сложности" class="section" id="complexity" />}}

{{<slide title="Анализ сложности">}}
Предположим, что \\(h\colon K \to N\\) --- случайная величина с равномерным распределением.
{{</slide>}}

{{<slide title="Прямое связывание">}}
Пусть искомый ключ находится в конце цепочки длинны \\(L\\). Тогда сложность его нахождения равна:

{{<equation>}}
    T(\mathrm{get}) = O(L).
{{</equation>}}

Определим функцию коллизии следующим образом:

{{<equation>}}
    X_{a, b} = P\{h(a) = h(b)\} = \begin{cases}
        1, & h(a) = h(b),\\
        0, & \text{иначе}
    \end{cases}
{{</equation>}}
{{</slide>}}

{{<slide title="Прямое связывание">}}
Перейдём к мат. ожиданию:

{{<equation>}}
    EX_{a, b} = \begin{cases}
        1/N, & a \neq b,\\
        1, & a = b.
    \end{cases}
{{</equation>}}

Тогда

{{<equation>}}
    ET(\mathrm{get}) = O(EL) = O(\sum_{i = 1}^n EX_{k, k_i}) \leqslant O(1 + n/N).
{{</equation>}}
{{</slide>}}

{{<slide title="Метрика хеш-таблицы">}}
Коэффициент \\(\alpha = n / N\\) называется коэффициентом заполнения.

{{<note info>}}
Для метода прямого связывания \\(\alpha\\) может превышать 1, а для открытой адресации --- нет.
{{</note>}}
{{</slide>}}

{{<slide title="Прямое связывание">}}
Обозначим через \\(p_i\\) вероятность того, что потребуется \\(i\\) проб для вставки:

{{<equation>}}
\begin{gathered}
p_1 = \frac{N - n}{N}, \quad
p_2 = \frac{n}{N} \cdot \frac{N - n}{N - 1}, \quad
\ldots, \\[2em]
p_i = \frac{n}{N} \cdot \frac{n - 1}{N - 1} \cdot \frac{n - 2}{N - 2}
\cdot \ldots \cdot \frac{n - i + 1}{N - i + 1}
\cdot \frac{N - n}{N - i + 1}
\end{gathered}
{{</equation>}}
{{</slide>}}

{{<slide title="Прямое связывание">}}
Перейдём к мат. ожиданию:

{{<equation>}}
\begin{gathered}
ET(\mathrm{set}) = \sum_{i = 1}^{n + 1} i \cdot p_i = \\[1em]
= 1 \cdot \frac{N - n}{N} + 2 \cdot \frac{n}{N} \cdot \frac{N - n}{N - 1} +
\ldots + (n + 1)\frac{n}{N} \cdot
\ldots \cdot \frac{N - n + 1}{N - n} = \\[1em]
= \frac{N + 1}{N - (n - 1)}
\end{gathered}
{{</equation>}}
{{</slide>}}

{{<slide title="Прямое связывание">}}
Аналогично можно посчитать мат. ожидание сложности операции `get`

{{<equation>}}
ET(\mathrm{get}) = \frac{1}{n} \sum_{i = 1}^{n} ET(\mathrm{set}_i),
{{</equation>}}

где \\(\mathrm{get}_i\\) --- вставка \\(i\\)-го ключа, то есть

{{<equation>}}
ET(\mathrm{get}) = \frac{N + 1}{n} \sum_{i = 1}^{n} \frac{1}{N - i + 2} =
(N + 1)(H_{N+1} - H_{N-n+1}),
{{</equation>}}

где \\(H_i = \ln i + \gamma\\) --- гармоническая функция (\\(\gamma\\) --- постоянная Эйлера).
{{</slide>}}

{{<slide title="Прямое связывание">}}
Таким образом,

{{<equation>}}
\begin{gathered}
ET(\mathrm{get}) = \frac{\ln(N + 1) - \ln(N - n + 1)}{\alpha} = \\[1em]
= \frac{\ln((N + 1) / (N -n + 1))}{\alpha} = - \frac{\ln(1 - \alpha)}{\alpha}.
\end{gathered}
{{</equation>}}
{{</slide>}}

{{<slide title="К цифрам">}}
\\(\alpha\\) | Общий сл. | Лин. пробы
-------------|-----------|------------
0.1          | 1.05      | 1.06
0.25         | 1.15      | 1.17
0.5          | 1.39      | 1.5
0.75         | 1.85      | 2.5
0.9          | 2.56      | 5.5
0.95         | 3.15      | 10.5
0.99         | 4.66      | ---
{{</slide>}}

{{<slide title="Анализ сложности">}}
Для метода линейных проб получаем

{{<equation>}}
ET(\mathrm{get / set}) = \frac{1 - \alpha/2}{1 - \alpha}
{{</equation>}}
{{</slide>}}

{{<slide title="Без допущений" class="section" id="real" />}}

{{<slide title="Без допущений">}}
\\(h\colon K \to N\\) --- случайные величины.

Пусть \\(\mathscr H = \{h\colon K \to N\}\\) --- некоторое семейство хеш-функций. И пусть существует равномерная вероятностная мера выбора \\(h \in \mathscr H\\).

Для сохранения оценок \\(ET(\mathrm{get / set}) = O(1 + \alpha)\\) необходимо, чтобы

{{<equation>}}
EX_{a, b} = \begin{cases}
    \frac{1}{N}, & a \neq b\\
    1, & a = b.
\end{cases}
{{</equation>}}
{{</slide>}}

{{<slide title="Без допущений">}}
{{<theorem Определение>}}
\\(\mathscr H\\) является _универсальным_, если для случайно выбранной \\(h \in \mathscr H\\) следует, что \\(P[h(a) = h(b), a \neq b] \leqslant \frac{1}{N}\\).
{{</theorem>}}

То есть мы переносим рандомизацию с построения \\(h(k)\\) на выбор \\(h \in \mathscr H\\).
{{</slide>}}

{{<slide title="Без допущений">}}
{{<note info>}}
Семейство \\(\mathscr H\\) должно быть не очень большим, иначе выбор будет долгим и хранение выбранной функции будет занимать много места.
{{</note>}}
{{</slide>}}

{{<slide title="Без допущений">}}
Без ограничения общности будем считать, что \\(K \subset \{0, \ldots, p - 1\}\\), где \\(p\\) --- простое число. Тогда

{{<equation>}}
\mathscr H = \{h_{ab}(k) = ak + b \mod p \mod N \colon a, b \in p, a \neq 0\}.
{{</equation>}}

То есть выбор \\(h\\) сводится к выбору \\(a\\) и \\(b\\).

{{<theorem Утверждение>}}
Такое \\(\mathscr H\\) является универсальным.
{{</theorem>}}
{{</slide>}}
