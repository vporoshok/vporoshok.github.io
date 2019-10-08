---
title: Readme Driven Development
description: Как написать удобную библиотеку
date: 2019-09-03T09:49:41Z
draft: true
categories:
- life-style
tags:
- architect
- checklist
---

{{<blockquote author="Будин А.В.">}}
Технари всегда начинают разговор с «нет», потому что думают о том, как это реализовывать, а тут надо «парить»…
{{</blockquote>}}

В этой статье попробуем разобраться о том, как проектировать программные интерфейсы. Интерфейсы могут быть совершенно разными, однако, есть в них одна общая черта: программисты разрабатывают их для других программистов. И это будет нашим большим плюсом, потому что мы также можем выступать в роли потребителей собственных продуктов. Итак, вы решили разработать библиотеку или сервис. С чего начать?

Один из подходов к проектированию программ был предложен Томом Престоном--Вернером[^1] одним из основателей GitHub. Этот подход называется RDD или Readme Driven Development и предлагает начинать проект с написания одного документа: README.md.

## Мотивация

Я довольно технически настроенный человек. И каждый раз, когда я слышу какую-то проблему / задачу / вопрос, мой мозг начинает искать решение. Можно назвать это моим недостатком. Один знакомый психотерапевт как-то привёл мне пример. Представьте, что рядом с вами ребёнок, пытаясь забить гвоздь, ударил себя по пальцу. Последнее, что поможет ситуации, это объяснение ему, что он не так держал молоток. Эту ситуацию не надо решать аналитически. Но мне довольно трудно оценить ситуацию в целом. Привычка закапываться в детали, когда за мелочами перестаёшь видеть целое.

### Philosophy

Конечно, в первую очередь надо сформулировать задачу, которую будет решать ваша программа. Довольно часто я сам подходил к этой части довольно халатно, мол сервис авторизации, будет делать всё, что связанно с авторизацией. А управление пользователями: создание, приглашение, блокировка --- тоже в этом сервисе будет происходить? На многие вопросы ответы находятся в момент написания или проектирования кода. Таким образом мы подстраиваем интерфейс программы для упрощения её внутреннего устройства. Но потребитель нашей программы не будет смотреть на её внутренности, он будет использовать её как чёрный ящик. И менять форму ящика под содержимое на мой взгляд порочная практика.

В противовес подходу проектирования от реализации часто приводят DDD ([Document-Driven Development](https://gist.github.com/zsup/9434452)). Но полное следование такому подходу приводит к разработке довольно большими итерациями, практически водопадному циклу разработки. Не будем радикалистами. Для этого есть менее строгий подход: RDD или Readme Driven Development. Этот подход говорит о том, что начинать разработку необходимо с написания одного документа: README.md. Этот подход был предложен Томом Престоном--Вернером[^1] одним из основателей GitHub.

Perhaps this project is a reflection of some idea or philosophy.

## Usage

```
Common usage case of this project in a short snippet.
It shouldn't contain all the features of the project.
Short is better than full.
```

## How it works

Architect, conceptions, dependencies. This section should be written after implementation.

## Key features

List of features that may help to decide use this project.

## See also

List of inspiration projects, alternatives, and analogs. Maybe some comparisons if it's important.

## Roadmap

Features to do.

## Ссылки

- https://devzen.ru/episode-0144/
[^1]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
- https://krasimirtsonev.com/blog/article/readme-driven-development
- https://medium.com/@elliotchance/readme-driven-development-3a434b7e253c
- https://deterministic.space/readme-driven-development.html
- https://github.com/matiassingers/awesome-readme
- https://github.com/noffle/art-of-readme#readme
- http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions
