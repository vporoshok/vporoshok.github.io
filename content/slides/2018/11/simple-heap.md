---
title: Простая двоичная куча
description: А я угадаю этот минимум за O(1)
date: 2018-11-02T15:00:00Z
draft: false
katex: true
mermaid: true
back: /post/2018/11/simple-heap/
---

<style>
    .slide a {
        background: none;
    }
    .red {
        color: red;
    }
    .slide.section {
        display: flex;
        padding: 0;
        align-items: center;
        justify-content: center;
    }
    .slide.section h2 {
        font-weight: normal;
    }
    .slide.compact pre {
        padding-top: 0;
    }
</style>

{{< slide title="Двоичная куча" class="clear" shout="true" />}}

{{< slide title="План" class="toc" id="toc" >}}
1. [задача и применение](#problem)
2. [куча: определение и базовые операции](#definition)
3. [двоичная куча: определение и индексация](#binary-heap)
4. [реализация базовых операций](#implementation)
5. [другие операции и итераторы](#iterator)
6. [эффективное построение кучи](#initialization)
7. [пирамидальная сортировка](#heap-sort)
{{< /slide >}}

{{< slide title="Задача и применение" class="section" id="problem" />}}

{{< slide title="Задача" >}}
Очередь с приоритетом
: вектор с координатами из линейно упорядоченного множества, на котором определены две операции:
  - добавление элемента
  - извлечение минимума
{{< /slide >}}

{{< slide title="Применение" >}}
- слияние нескольких массивов
- выбор пордяковых статистик
- частичная сортировка данных
- поиск кратчайшего пути
- построение минимального остова графа
{{< /slide >}}

{{< slide title="Решения?" >}}
<table>
    <col-group>
        <col width="40%">
        <col>
        <col>
        <col width="24%">
    </col-group>
    <thead>
        <tr>
            <th scope="col">Структура
            <th scope="col">Построение
            <th scope="col">Добавление
            <th scope="col">Извлечение
    <tbody>
        <tr>
            <th scope="row">Массив
            <td>\(O(1)\)
            <td>\(O(1)\)
            <td class="red">\(O(n)\)
        <tr>
            <th scope="row">Отсортированный массив
            <td class="red">\(O(n\log n)\)
            <td>\(O(\log n)\)
            <td>\(O(1)\)
        <tr class="next">
            <th scope="row">Куча
            <td>\(O(n)\)*
            <td>\(O(\log n)\)
            <td>\(O(\log n)\)
</table>
{{< /slide >}}

{{< slide title="Куча" class="section" id="definition" />}}

{{< slide title="Определение" >}}
Куча (heap)
: дерево, в котором любой элемент не меньше своего родителя.

{{< note "info" >}}
Аналогично можно определить кучу для получения максимума, но в дальнейшем будем рассматривать неубывающую кучу.
{{< /note >}}
{{< /slide >}}

{{< slide title="Пример" >}}
{{< mermaid >}}
graph TD
    A((1))
    A---B((3))
    A---C((2))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((5))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((9))
    H---N((21))
    J---O((10))
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Базовые операции" >}}
На таком дереве несложно реализовать три основные операции, производимые с куче:
- получение минимума (peek);
- извлечение минимума (pop);
- добавление элемента (push);
{{< /slide >}}

{{< slide title="Восстановление свойств кучи" >}}
Аномалия
: нарушение свойства кучи _любой элемент не меньше своего родителя_ в одном из её элементов.

Аномалии могут возникнуть по двум причинам:
- большой элемент оказался слишком высоко в дереве
- маленький элемент оказался слишком низко в дереве
{{< /slide >}}

{{< slide title="Погружение элемента" >}}
{{< mermaid >}}
graph TD
    A((10))
    A---B((3))
    A---C((2))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((5))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((9))
    H---N((21))

    style A fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Погружение элемента" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((3))
    A---C((10))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((5))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((9))
    H---N((21))

    style A fill:lightGreen
    style C fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Погружение элемента" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((3))
    A---C((5))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((10))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((9))
    H---N((21))

    style C fill:lightGreen
    style H fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Погружение элемента" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((3))
    A---C((5))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((9))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((10))
    H---N((21))

    style H fill:lightGreen
    style M fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Извлечение минимума (pop)" >}}
1. сохраним значение корня
2. запишем поверх корня любой листовой элемент
3. удалим этот лист из дерева
4. выполним погружение корня
5. вернём сохранённое значение корня
{{< /slide >}}

{{< slide title="Всплытие элемента" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((3))
    A---C((5))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((9))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((10))
    H---N((21))
    J---O((1))

    style O fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Всплытие элемента" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((3))
    A---C((5))
    A---D((4))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((9))
    D---I((5))
    D---J((1))
    E---K((9))
    E---L((17))
    H---M((10))
    H---N((21))
    J---O((4))

    style J fill:pink
    style O fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Всплытие элемента" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((3))
    A---C((5))
    A---D((1))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((9))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((10))
    H---N((21))
    J---O((4))

    style D fill:pink
    style J fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Всплытие элемента" >}}
{{< mermaid >}}
graph TD
    A((1))
    A---B((3))
    A---C((5))
    A---D((3))
    B---E((4))
    C---F((8))
    C---G((8))
    C---H((9))
    D---I((5))
    D---J((4))
    E---K((9))
    E---L((17))
    H---M((10))
    H---N((21))
    J---O((4))

    style A fill:pink
    style D fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Добавление элемента (push)" >}}
1. добавляем новый элемент листом
2. выполняем всплытие этого элемента
{{< /slide >}}

{{< slide title="Двоичная куча" class="section" id="binary-heap" />}}

{{< slide title="Двоичная куча" >}}
Добавим следующие ограничения:
- степень ветвления всех вершин всех вершин не более \\(2\\)
- глубина всех листьев отличается не более, чем на \\(1\\)
- последний слой заполняется слева направо без пропусков
{{< /slide >}}

{{< slide title="Двоичная куча" >}}
{{< mermaid >}}
graph TD
    A((0))
    A---B((1))
    A---C((2))
    B---D((3))
    B---E((4))
    C---F((5))
    C---G((6))
    D---H((7))
    D---I((8))
    E---J((9))
    E---K((10))
    F---L((11))
    F---M((12))
    G---N((13))
    G---O((14))

    style M opacity:0.2
    style N opacity:0.2
    style O opacity:0.2
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Индексация" >}}
Для \\(i\\)-го узла
- родитель: \\(\lfloor (i - 1) / 2 \rfloor\\)
- левый сын: \\(2i + 1\\)
- правый сын: \\(2i + 2\\)

Высота дерева: \\(\lceil 1 + \log n \rceil\\)
{{< /slide >}}

{{< slide title="Реализация" class="section" id="implementation" />}}

{{< slide title="Реализация" class="compact" >}}
```python
class BinaryHeap:
    _items = []
    def peek(self):
        if len(self._items) > 0:
            return self._items[0]
    def push(self, x):
        self._items.append(x)
        self._sift_up(len(self._items) - 1)
```
{{< /slide >}}

{{< slide title="Реализация" >}}
```python
    def _sift_up(self, i):
        while i > 0:
            j = (i - 1) // 2
            if self._items[j] <= self._items[i]:
                break
            self._swap(i, j)
            i = j
```
{{< /slide >}}

{{< slide title="Реализация" >}}
```python
    def pop(self):
        if len(self._items) > 0:
            x = self._items[0]
            self._swap(0, len(self._items)-1)
            self._items.pop()
            self._sift_down(0)
            return x
```
{{< /slide >}}

{{< slide title="Реализация" >}}
```python
    def _sift_down(self, i):
        while True:
            j = self._min_son(i)
            if not j or self._items[i] <= self._items[j]:
                break
            self._swap(i, j)
            i = j
```
{{< /slide >}}

{{< slide title="Реализация" class="compact" >}}
```python
    def _min_son(self, i):
        l_son = i * 2 + 1
        r_son = i * 2 + 2
        if len(self._items) <= l_son:
            return None
        if len(self._items) <= r_son or self._items[l_son] < self._items[r_son]:
            return l_son
        return r_son
```
{{< /slide >}}

{{< slide title="Оптимизации" >}}
Метод `_min_son` возвращает индекс меньшего сына, если хотя бы один из сыновей существует, отдавая предпочтение правому сыну среди равных
{{< /slide >}}

{{< slide title="Другие операции и итераторы" class="section" id="iterator" />}}

{{< slide title="Другие операции" >}}
- уменьшение ключа (decrease_key)
- удаление (delete)
- слияние (meld)
{{< /slide >}}

{{< slide title="Итераторы" >}}
Динамические указатели на элементы структуры, поддерживаемые самой структурой.

Можно воспользоваться дополнительным массивом, где каждому элементу при вставке выдавать следующую ячейку массива, возвращая в качестве итератора индекс этой ячейки. В значение ячейки необходимо записывать индекс элемента в основном массиве. А рядом с элементом в основном массиве хранить его итератор.
{{< /slide >}}

{{< slide title="Реализация с итераторами" >}}
```python
class BinaryHeapWithIterators:
    _items = []
    _iterators = []

    def peek(self):
        if len(self._items) > 0:
            return self._items[0][0]
```
{{< /slide >}}

{{< slide title="Реализация с итераторами" >}}
```python
    def push(self, x):
        p = len(self._iterators)
        self._iterators.append(len(self._items))
        self._items.append((x, p))
        self._sift_up(len(self._items) - 1)
        return p
```
{{< /slide >}}

{{< slide title="Реализация с итераторами" >}}
```python
    def pop(self):
        if len(self._items) > 0:
            x = self._items[0]
            self._swap(0, len(self._items)-1)
            self._items.pop()
            self._sift_down(0)
            return x[0]
```
{{< /slide >}}

{{< slide title="Реализация с итераторами" >}}
```python
    def decrease(self, p, x):
        i = self._iterators[p]
        self._items[i] = (self._items[i][0] - x, p)
        self._sift_up(i)
```
{{< /slide >}}

{{< slide title="Реализация с итераторами" >}}
```python
    def _swap(self, i, j):
        self._iterators[self._items[i][1]] = j
        self._iterators[self._items[j][1]] = i
        self._items[i], self._items[j] = self._items[j], self._items[i]
```
{{< /slide >}}

{{< slide title="Слияние" >}}
\\[
T(n, m) = O(n \log m)
\\]

Эффективные реализации:
- биномиальная куча
- левацкая или косая куча
- очередь Бродала
{{< /slide >}}

{{< slide title="Эффективное построение кучи" class="section" id="initialization" />}}

{{< slide title="Добавление элементов в пустую кучу" >}}
\\[
T(n) = O\left(\log 1 + \log 2 + \ldots + \log(n - 1)\right) =
\\]
\\[
= O\left(n \left(\frac{\log 1 + \log 2 + \ldots + \log(n - 1)}{n}\right)\right) =
\\]
по неравенству Йенсена:
\\[
= O\left(n \log\left(\frac{1 + 2 + \ldots + n - 1}{n}\right)\right)
= O\left(n \log\left(\frac{n - 1}{2}\right)\right) = O(n \log n).
\\]
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
Будем перестраивать входной массив так, чтобы он начал удовлетворять условиям кучи.

Пусть дан массив начальных элементов \\((4, 2, 12, 83, 45, 3, 21, 67, 11, 32, 37, 9, 1, 15, 7)\\)
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((12))
    B---D((83))
    B---E((45))
    C---F((3))
    C---G((21))
    D---H((67))
    D---I((11))
    E---J((32))
    E---K((37))
    F---L((9))
    F---M((1))
    G---N((15))
    G---O((7))
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((12))
    B---D((83))
    B---E((45))
    C---F((3))
    C---G((7))
    D---H((67))
    D---I((11))
    E---J((32))
    E---K((37))
    F---L((9))
    F---M((1))
    G---N((15))
    G---O((21))

    style G fill:lightGreen
    style O fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((12))
    B---D((83))
    B---E((45))
    C---F((1))
    C---G((7))
    D---H((67))
    D---I((11))
    E---J((32))
    E---K((37))
    F---L((9))
    F---M((3))
    G---N((15))
    G---O((21))

    style F fill:lightGreen
    style M fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((12))
    B---D((83))
    B---E((32))
    C---F((1))
    C---G((7))
    D---H((67))
    D---I((11))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((3))
    G---N((15))
    G---O((21))

    style E fill:lightGreen
    style J fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((12))
    B---D((11))
    B---E((32))
    C---F((1))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((3))
    G---N((15))
    G---O((21))

    style D fill:lightGreen
    style I fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((12))
    B---D((11))
    B---E((32))
    C---F((1))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((3))
    G---N((15))
    G---O((21))

    style D fill:lightGreen
    style E fill:lightGreen
    style F fill:lightGreen
    style G fill:lightGreen
    style H fill:lightGreen
    style I fill:lightGreen
    style J fill:lightGreen
    style K fill:lightGreen
    style L fill:lightGreen
    style M fill:lightGreen
    style N fill:lightGreen
    style O fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((1))
    B---D((11))
    B---E((32))
    C---F((3))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((12))
    G---N((15))
    G---O((21))

    style C fill:lightGreen
    style D fill:lightGreen
    style E fill:lightGreen
    style F fill:lightGreen
    style G fill:lightGreen
    style H fill:lightGreen
    style I fill:lightGreen
    style J fill:lightGreen
    style K fill:lightGreen
    style L fill:lightGreen
    style M fill:lightGreen
    style N fill:lightGreen
    style O fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((2))
    A---C((1))
    B---D((11))
    B---E((32))
    C---F((3))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((12))
    G---N((15))
    G---O((21))

    style B fill:lightGreen
    style C fill:lightGreen
    style D fill:lightGreen
    style E fill:lightGreen
    style F fill:lightGreen
    style G fill:lightGreen
    style H fill:lightGreen
    style I fill:lightGreen
    style J fill:lightGreen
    style K fill:lightGreen
    style L fill:lightGreen
    style M fill:lightGreen
    style N fill:lightGreen
    style O fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((1))
    A---B((2))
    A---C((3))
    B---D((11))
    B---E((32))
    C---F((4))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((12))
    G---N((15))
    G---O((21))

    style A fill:lightGreen
    style B fill:lightGreen
    style C fill:lightGreen
    style D fill:lightGreen
    style E fill:lightGreen
    style F fill:lightGreen
    style G fill:lightGreen
    style H fill:lightGreen
    style I fill:lightGreen
    style J fill:lightGreen
    style K fill:lightGreen
    style L fill:lightGreen
    style M fill:lightGreen
    style N fill:lightGreen
    style O fill:lightGreen
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
{{< mermaid >}}
graph TD
    A((x))
    A---B{α}
    A---C{β}
{{< /mermaid >}}

\\(\alpha\\) и \\(\beta\\) являются кучами
{{< /slide >}}

{{< slide title="Эффективное построение кучи" >}}
Для \\(k\\)-го (снизу) слоя будет произведено не более чем \\(n / 2^k\\) операций погружения. При этом каждая операция погружения будет иметь сложность \\(O(k)\\).
\\[
T(n) = \sum\_{k = 0}^{\log n} \frac{n}{2^k} O(k) = O\left(\sum\_{k = 0}^{\log n} \frac{n}{2^k} k\right)
= O\left(n \sum\_{k = 0}^{\log n} \frac{k}{2^k} k\right) \leqslant
\\]
\\[
\leqslant O\left(n \sum\_{k = 0}^{\infty} \frac{k}{2^k} \right) = O(nc) = O(n)
\\]
{{< /slide >}}

{{< slide title="Рекурентная формула" >}}
\\[
T(1) = 1 \quad\text{и}\quad T(h) \leqslant O(2T(h - 1) + ch),
\\]
\\(h\\) --- высота преобразуемого дерева, \\(c\\) --- некоторая константа
\\[
T(h) \leqslant O(c(2^{h + 1} - h - 2)) \leqslant O(c2^{h + 1}) \leqslant O(2cn).
\\]
{{< /slide >}}

{{< slide class="section" title="Пирамидальная сортировка" id="heap-sort" />}}

{{< slide title="Пирамидальная сортировка" >}}
{{< mermaid >}}
graph TD
    A((21))
    A---B((2))
    A---C((3))
    B---D((11))
    B---E((32))
    C---F((4))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((12))
    G---N((15))
    G---O((1))

    style O fill:lightGreen, opacity:0.5
    style A fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Пирамидальная сортировка" >}}
{{< mermaid >}}
graph TD
    A((2))
    A---B((11))
    A---C((3))
    B---D((21))
    B---E((32))
    C---F((4))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((12))
    G---N((15))
    G---O((1))

    style O fill:lightGreen, opacity:0.5
    style A fill:yellow
    style B fill:yellow
    style D fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Пирамидальная сортировка" >}}
{{< mermaid >}}
graph TD
    A((15))
    A---B((11))
    A---C((3))
    B---D((21))
    B---E((32))
    C---F((4))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((9))
    F---M((12))
    G---N((2))
    G---O((1))

    style O fill:lightGreen, opacity:0.5
    style N fill:lightGreen, opacity:0.5
    style A fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Пирамидальная сортировка" >}}
{{< mermaid >}}
graph TD
    A((3))
    A---B((11))
    A---C((4))
    B---D((21))
    B---E((32))
    C---F((9))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((15))
    F---M((12))
    G---N((2))
    G---O((1))

    style O fill:lightGreen, opacity:0.5
    style N fill:lightGreen, opacity:0.5
    style A fill:yellow
    style C fill:yellow
    style F fill:yellow
    style L fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Пирамидальная сортировка" >}}
{{< mermaid >}}
graph TD
    A((12))
    A---B((11))
    A---C((4))
    B---D((21))
    B---E((32))
    C---F((9))
    C---G((7))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((15))
    F---M((3))
    G---N((2))
    G---O((1))

    style O fill:lightGreen, opacity:0.5
    style N fill:lightGreen, opacity:0.5
    style M fill:lightGreen, opacity:0.5
    style A fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Пирамидальная сортировка" >}}
{{< mermaid >}}
graph TD
    A((4))
    A---B((11))
    A---C((7))
    B---D((21))
    B---E((32))
    C---F((9))
    C---G((12))
    D---H((67))
    D---I((83))
    E---J((45))
    E---K((37))
    F---L((15))
    F---M((3))
    G---N((2))
    G---O((1))

    style O fill:lightGreen, opacity:0.5
    style N fill:lightGreen, opacity:0.5
    style M fill:lightGreen, opacity:0.5
    style A fill:yellow
    style C fill:yellow
    style G fill:pink
{{< /mermaid >}}
{{< /slide >}}

{{< slide title="Задания" id="exercises" >}}
1. Реализуйте кучу с итераторами, переиспользующую свободные ячейки массива итераторов. Напишите тест, позволяющий проверить, что при многократном цикле push-pop память структуры не растёт.
2. Реализуйте конструктор, принимающий массив данных и преобразующий их в кучу за линейное время.
3. Реализуйте пирамидальную сортировку.
{{< /slide >}}

{{< slide title="Дополнительное чтение" id="further" >}}
1. Ryan Hayward, Ryan, and McDiarmid, Colin. "Average Case Analysis of Heap Building." _Journal of algorithms_, vol. 12, no. 1, 1991, pp. 126–153.
2. Atkinson, M.D., Sack, J.-R., Santoro, N., and Strothotte, T. "Min-max heaps and generalized priority queues." _Programming techniques and Data structures. Comm. ACM_, vol. 29, no. 10, 1986, pp. 996–1000.
3. Brodal, Gerth S. "Worst-Case Efficient Priority Queues." _Proc. 7th Annual ACM-SIAM Symposium on Discrete Algorithms_, 1996, pp. 52–58.
{{< /slide >}}

{{< slide title="Ссылки" id="bibliography" >}}
1. Вирт, Никлаус. _Алгоритмы и структуры данных. Новая версия для Оберона_. Перевод Ткачев, Ф. В., М.: ДМК Пресс, 2016.
2. Асанов, М. О., Баранский, В. А., и Расин, В. В. _Дискретная математика: графы, матроиды, алгоритмы_. 2-е издание, СПб.: Издательство «Лань», 2010.
{{< /slide >}}

{{< slide class="clear section" title="Спасибо за внимание" />}}