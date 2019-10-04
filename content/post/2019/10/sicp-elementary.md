---
title: 'SICP: 1.1 Элементы программирования'
description: Комбинации, переменные, функции и условные выражения
date: 2019-10-04T15:17:31Z
draft: false
categories:
- algorithm
tags:
- sicp
- scheme
toc: true
katex: true
mermaid: true
---

## Префиксная нотация и комбинации

Программа на языке Лисп представляет из себя набор комбинаций (combination) и особых форм (special form). Комбинациями называются кортежи, состоящие из команды и операндов (аргументов):
```scheme
(<op> <arg1> [...<args>])
```

В качестве операции могут выступать базовые арифметические операции, встроенные в язык (+, -, * и /). Например
```scheme
(+ 8 4)
;> 12
```
(здесь и далее ответы интерпретатора пишутся в комментарии, начинающемся с `;>`)
```scheme
(/ 128 8)
;> 16
```

Первое время кажется сложным воспринимать такую запись, где операция предшествует операндам. Такая запись называется префиксной нотацией. Но она оказывается близкой к модели выполнения программ в компьютере и достаточно понятной для человека. Также важной особенностью такой нотации является описание операций с переменным числом операндов:
```scheme
(+ 21 35 12 7)
;> 75
```
К тому же комбинации можно вкладывать друг в друга, образовывая сложные, но однозначные конструкции:
```scheme
(+ (* 3 5) (- 10 6))
;> 19
```

Но большие выражения, записанные в префиксной нотации читаются достаточно тяжело, поэтому применяется так называемая красивая печать (pretty printing), например, выражение
```scheme
(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))
```
можно записать следующим образом:
```scheme
(+ (* 3
      (+ (* 2 4)
         (+ 3 5)))
   (+ (- 10 7)
      6))
```

В общем случае:
```scheme
(<op> arg1
      arg2
      ...)
```

## Имена и окружение

Часто необходимо переиспользовать вычисленный результат. Для этого можно давать имена результатам вычислений с помощью особой формы

```scheme
(define <name> <expr>):
```

Например,
```scheme
(define pi 3.14159)
(define radius 10)
(define circumference (* 2 pi radius))
circumference
;> 62.8318
```

Таким образом можно пошагово строить сложные выражения. Именованные значения сохраняются в окружении. Изначально есть глобальное окружение, помимо него существуют окружения подпрограмм (функций), о которых мы поговорим позже.

## Функции

Помимо именования результатов вычислений, можно также именовать выражения, формируя таким образом функции. Для этого используется специальная форма define:
```scheme
(define (<name> ...<args>) <expr>)
```
Например,
```scheme
(define (square x) (* x x))
(define (sum-of-squares x y)
  (+ (square x) (square y)))
```
Получившиеся функции можно использовать аналогично встроенным в язык операциям.
```scheme
(sum-of-squares 3 4)
;> 25
```

Можно определить вычисление комбинации следующим образом:
1. вычислить все подвыражения комбинации;
2. использовать результат первого подвыражения как функцию, которую применить к оставшимся подвыражениям.

Таким образом можно интерпретировать вычисление выражения
```scheme
(sum-of-squares (+ 1 2) (* 2 2))
```
следующей последовательностью преобразований:
```scheme
(sum-of-squares 3 4)      ; вычисляются все подвыражения
(+ (square 3) (square 4)) ; выполняется подстановка функции
(+ (* 3 3) (* 4 4))       ; выполняется подстановка функции
(+ 9 16)                  ; вычисляются все подвыражения
;> 25                     ; первое подвыражение применяется к остальным
```

Это не то, что реально происходит в интерпретаторе, это упрощённая модель, которой достаточно на текущем этапе. Позже мы рассмотрим случаи, когда такой модели оказывается недостаточно, и рассмотрим другую модель подстановки функций. Но уже из этой модели очевидно то, что подвыражения комбинации вычисляются до вычисления самой операции. Такая модель вычисления называется нормальным порядком вычисления. Также существует альтернативная модель, называемая аппликативным порядком или ленивыми вычислениями, когда подвыражения вычисляются в момент обращения к ним. Тогда вычисление предыдущего выражения можно представить следующей последовательностью:
```scheme
(sum-of-squares (+ 1 2) (* 2 2))
(+ (square (+ 1 2)) (square (* 2 2)))
(+ (* (+ 1 2) (+ 1 2)) (* (* 2 2) (* 2 2)))
```
После чего производится редукция выражений:
```scheme
(+ (* 3 3) (* 4 4))
(+ 9 16)
;> 25
```

И нормальный, и аппликативный порядки приводят к одинаковому результату, если все подвыражения корректно вычислимы, однако, это не всегда так (см. Упражнение 1.5).

## Условные выражения и предикаты

Для полноценного языка программирования не хватает ещё одного класса выражений: условного ветвления. Лисп предоставляет два вида условных выржений:
```scheme
(cond (<pred> <expr>)
      (<pred> <expr>)
      ...
     [(else <expr>)]))
```
и, в случае двух веток:
```scheme
(if <pred> <expr> <expr>)
```
Через `<pred>` обозначается предикат, выражение, результатом которого может быть либо ложь (`#f`), либо любое другое значение, которое будет интерпретироваться как истина (`#t`). Результатом таких выражений будет результат первого выражения с верным предикатом. Например, можно выразить функцию модуля числа следующим образом:
```scheme
(define (abs x)
    (if (< x 0)
        (- x)
        x))
```
или
```scheme
(define (abs x)
    (cond ((< x 0) (- x))
          (else x)))
```

Условные выражения являются специальными формами. При этом вычисляются только те предикаты и выражения, которые необходимы (все предикаты до первого истинного и выражение, следующее за истинным предикатом). То есть условные выражения имеют аппликативный порядок вычисления.

Базовыми предикатами являются >, < и =. Помимо них есть ещё 3 логических выражения:
```scheme
(and ...<preds>)
(or ...<preds>)
(not <pred>)
```

Выражения `and` и `or` являются особыми формами, потому что в первом случае вычисляются предикаты до первого ложного, а во втором до первого истинного. Выражения же `not` можно интерпретировать как обычную функцию.

{{<note info>}}
Кстати, при вычислении комбинаций первым пунктом является «вычислить все подвыражения». Это можно применить как к аргументам функции, так и к самой функции. Например, функцию модуля можно записать следующим образом:
```scheme
(define (abs x) ((if (< x 0) - +) x))
```

Подумайте как это можно интерпетировать. Какой будет последовательность преобразований выражения `(abs 5)`? `(abs -5)`?
{{</note>}}

## Пример: вычисление квадратного корня методом Ньютона

Функции, описанные выше очень похожи на математическое понятие отображений и функций. Но, как быть с функциями, выходящими за рамки элементарных арифметических операций? Как, например, добиться от компьютера вычисления квадратного корня? Вообще, в современных компьютерах на аппаратном уровне вшита возможность вычисления экспоненты числа через приближение рядом Тейлора. Имея экспоненту легко вычислить любую степень числа, в том числе и дробную, например, 1/2. Но представим, что нам достался компьютер, который не умеет считать экспоненту, а корень нам надо посчитать. Для этого воспользуемся [методом Ньютона](https://ru.wikipedia.org/wiki/Метод_Ньютона) приближённого вычисления значения функции.

{{<note info "Вкратце">}}
Для нахождения корня функции можно воспользоваться итеративным процессом приближения. Пусть нам дана функция \\(f\colon \mathbb R \to \mathbb R\\) и нам необходимо найти её корень. Выберем \\(x\_0\\) --- некоторое значение, близкое к нулю функции. Вычислим \\(x\_{i+1}\\) как корень касательной \\(f\\) в точке \\(x\_i\\).
\\[
  x_{i+1} = x_i - \frac{f(x_i)}{f^\prime(x_i)}
\\]
<figure>
  <img src="https://upload.wikimedia.org/wikipedia/ru/e/e0/Newton_ex.PNG"/>
  <figcaption><h4>График последовательных приближений</h4></figcaption>
</figure>
{{</note>}}

В нашем случае мы хотим найти квадратный корень числа \\(a\\), то есть при каком значении \\(x\\) функция \\(x^2\\) будет равна \\(a\\) или, другими словами, необходимо найти корень функции \\(f(x) = x^2 - a\\). Для функции \\(f\\) производная в любой точке равна \\(f^\prime(x) = 2x\\), поэтому следующий шаг можно выразить следующей формулой:
{{<equation>}}
  x_{i+1} = x_i - \frac{f(x_i)}{f^\prime(x_i)} = x_i - \frac{x_i^2 - a}{2x_i} = \frac{x_i^2 + a}{2x_i} = \frac{x_i + \frac{a}{x_i}}{2}
{{</equation>}}
или, немного, перефразировав, можно говорить, что \\(x\_{i+1}\\) можно вычислить как среднеарифметическое между \\(x\_i\\) и \\(\frac{a}{x\_i}\\).
```scheme
(define (imporve x a)
  (average x (/ a x)))
```
где
```scheme
(define (average a b)
  (/ (+ a b) 2))
```

Не спешите хвататься за рекурсию, для начала надо понять, когда же остановиться? Для этого определим ещё одну функцию, в которой будем сравнивать квадрат вычисленного значения с исходным числом, корень которого мы пытаемся найти:
```scheme
(define (good-enough? x a)
  (< (abs (- (square x) a)) 0.001))
```

Наконец, можно определить функцию итеративного вычисления квадратного корня:
```scheme
(define (sqrt-iter x a)
  (if (good-enough? x a)
      x
      (sqrt-iter (improve x a) a)))
```

Для упрощения, предположим, что начальная оценка любого корня будет равна единице:
```scheme
(define (sqrt x)
  (sqrt-iter 1.0 x))
```

Проверим:
```scheme
(sqrt 9)
;> 3.00009155413138
(sqrt (+ 100 37))
;> 11.704699917758145
(sqrt (+ (sqrt 2) (sqrt 3)))
;> 1.7739279023207892
(square (sqrt 1000))
;> 1000.000369924366
```

Этот пример показывает как сложные программы органично разбиваются на простые функции и их комбинирование, а также то, как выразить циклический (итеративный) процесс без использования особых конструкций, а с помощью рекурсии, для которой достаточно возможности вызывать функцию.

## Процедуры как абстракции типа «черный ящик»

Итак, мы получили желаемый результат: функция `sqrt x` вычисляет значение квадратного корня числа. При этом алгоритм вычисления разбит на небольшие функции, связанные следующей иерархией:
{{<mermaid class="align-center" alt="Функциональная декомпозиция программы sqrt">}}
graph TD
  A(sqrt)
  A --- B(sqrt-iter)
  B --- C(good-enough?)
  B --- D(improve)
  C --- E(square)
  C --- F(abs)
  D --- G(average)
{{</mermaid>}}

Важной особенностью такой декомпозиции является то, что каждый элемент, каждая функция имеет определённую задачу, область ответственности. Каждая функция может быть переписана с сохранением интерфейса без необходимости переписывать всю программу. Например, можно переписать функцию `good-enough?`, что предлагается сделать в упражнении 1.7. И для функции `sqrt-iter` ничего не измениться, для неё функция `good-enough?` является чёрным ящиком, чем-то, куда передаются два числа и получается ответ: Да или Нет. Для функции `sqrt-iter` совершенно неважно --- как этот ответ будет получен. Например, следующие две функции `square` неотличимы для внешнего наблюдателя:
```scheme
(define (square1 x) (* x x))

(define (square2 x)
  (exp (* 2 (log x))))
```

Мы как бы скрываем внутреннее устройство функции от вызывающей стороны. Но это, конечно, лукаво, ведь внутренние части нашей программы доступны снаружи: все функции `sqrt-iter`, `good-enough?` и так далее доступны везде в нашей программе. Давайте спрячем их. Для этого нам потребуется понимание зоны видимости.

### Локальные имена

Функция скрывает от вызывающей стороны своё внутреннее устройство. Это также означает, что снаружи недоступны внутренние данные и их имена. Так функции
```scheme
(define (square1 x) (* x x))

(define (square2 y) (* y y))
```
совершенно неотличимы снаружи. Внутренние или локальные имена оказываются приоритетнее внешних. Например, следующая программа
```scheme
(define x 5)

(define (square x) (* x x))

(square 10)
```
Вернёт 100, а не 25. Потому что `x` внутри функции `square` переписан и уже не равен внешней константе `x`. равной 5.

Это позволяет нам также создать локальные определения и функции:
```scheme
(define (square x)
  (define (double x) (+ x x))
  (exp (double (log x))))
```

То есть мы объявили функцию `double` внутри функции `square` и она стала доступна в этом блоке выполнения. А снаружи она будет недоступна, не будет существовать за пределами функции `square`. Давайте используя такой подход «спрячем» вспомогательные функции внутри `sqrt`:
```scheme
(define (sqrt a)
  (define (good-enough? x)
    (< (abs (- (square x) a)) 0.001))
  (define (improve x)
    (average x (/ a x)))
  (define (sqrt-iter x)
    (if (good-enough? x)
        x
        (sqrt-iter (improve x))))
  (sqrt-iter 1.0))
```

Также внутри функции `sqrt` можно изолировать определения функций `abs`, `square` и `average`. В дальнейшем такая блочная структура найдёт широкое применение в рамках примеров этой книги.

## Упражнения

Упражнения представлены в курсе https://repl.it/classroom/invite/cTpCI6u