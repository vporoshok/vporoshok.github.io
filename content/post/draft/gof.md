---
title: Приемы объектно-ориентированного проектирования. Паттерны проектирования
description:
date: 2018-06-18T05:22:23Z
draft: true
categories:
- book
tags:
- architect
toc: true
---

links
* http://www.mindmapinspiration.com/how-to-convert-text-to-mind-map-paul-foreman/

Эту книгу я купил несколько лет назад. Когда у меня на столе её увидел мой друг Ваня, он сказал: «Не советую тебе её читать сейчас, многие начинающие программисты слишком серьёзно воспринимают то, что в ней написано, а потом во всём видят шаблоны, пытаясь впихнуть фабрики и одиночки куда ни попадя». Тогда я просто пролистал книгу, посмотрел какие шаблоны и подходы есть вообще. Некоторые мне стали понятны, некоторые не зацепились в голове. Позже, когда я читал другие книги, ссылающиеся на эту, я читал из неё конкретные главы. Иногда, думая над устройством какого-нибудь модуля, подглядывал в поисках похожего решения. В общем, пользовался как справочником. Теперь, похоже пришло время прочитать её целиком, закрепить всё в своей голове.

## Глава 1. Введение в паттерны проектирования

> Дизайн должен, с одной стороны, соответствовать решаемой задаче, с другой --- быть общим, чтобы удалось учесть все требования, которые могут возникнуть в будущем.

Фраза, в своей неоднозначности достойная юридического документа. Сколько копий сломано о такой вот баланс между сферическим конём в вакууме и жёстко вбитыми костылями. Именно эту фразу я мог пропустить, именно о ней меня предупреждал Ваня. Но, к слову, несмотря на кучу историй про фанатиков, с безумством в глазах рисующих UML-диаграммы 8-уровневой иерархии наследования, я их ни разу не встречал. Возможно потому что был далёк от так называемого кровавого энтерпрайза. Хотя порой замечал у себя излишне фанатичные настроения. И тут хочется процитировать [Роба Пайка](https://go-proverbs.github.io): «Clear is better than clever».

В целом, во введении к первой главе даются общие идеи «за всё хорошее и против всего плохого». Многие тривиальные, но некоторые заслуживают внимания. Как минимум эту главу я бы рекомендовал прочитать новичкам в программировании, причём не раз. Вот некоторые цитаты:

> ...обеспечить «правильный», то есть в достаточной мере гибкий и пригодный для повторного использования дизайн, с первого раза очень трудно, если вообще возможно.

---

> ..._не нужно_ решать каждую новую задачу с нуля.

> Проектировщик, знакомый с паттернами, может сразу же применять их к решению новой задачи, не пытаясь каждый раз изобретать велосипед.

но при этом:

> ...паттерны проектирования — лишь малая часть того, что необходимо знать специалисту в этой области.

---

> Увы, у нас нет привычки записывать свой опыт на благо другим людям да и себе тоже.

---

> ...можно улучшить качество документации и сопровождения существующих систем, позволяя явно описать взаимодействия классов и объектов, а также причины, по которым система была построена так, а не иначе.

При этом не обязательно использовать шаблоны программирования, качество документации улучшается в сотни раз, если в ней написаны причины, по которым было принято то или иное решение.

> В издание не включено описание паттернов, имеющих отношение к параллельности, распределенному программированию и программированию систем реального времени.

По некоторым есть книги, которые я подумываю прочитать, перечитать и разобрать здесь, например У. Фокин «Распределенные алгоритмы».

### 1.1 Что такое паттерн проектирования

В целом предлагается под паттерном понимать следующую совокупность:
* Имя;
* Задача;
* Решение;
* Результаты;

Ну, и, конечно,

> Здесь под паттернами проектирования понимается _описание взаимодействия объектов и классов, адаптированных для решения общей задачи проектирования в конкретном контексте._

## Глава 3. Порождающие паттерны

### Паттерн Factory Method

> _Соединяет параллельные иерархии._ В примерах, которые мы рассматривали до сих пор, фабричные методы вызывались только **создателем**. Но это совершенно необязательно: клиенты тоже могут применять фабричные методы, особенно при наличии параллельных иерархий классов.

В качестве примера приводится вынесение функциональности трансформации графического объекта (перемещение, масштабирование и вращение) в отдельный интерфейс. При этом каждый графический объект имеет метод, возвращающий свой «манипулятор» (объект, реализующий этот интерфейс). При этом метод на базовом классе может возвращать настоящий базовый манипулятор (не быть абстрактным), реализующий трансформации, подходящие для большинства графических объектов. В то же время, если потребуется подменить манипулятор для сложного объекта (например, текст), можно переопределить этот метод именно для этого графического объекта. Таким образом, получается 2 параллельные иерархии классов: графических объектов и манипуляторов.
