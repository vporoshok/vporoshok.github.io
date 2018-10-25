---
title: Цикл статей про Angular
description: Оглавление статей
date: 2018-04-08T07:24:33Z
categories:
- develop
tags:
- tutorial
- angular
- typescript
- rxjs
- toc
---

Мы начали использовать [Angular](https://angular.io/) (в то время Angular 2) на одном из проектов нашей компании примерно в сентябре 2016 года. Тогда он только вышел из беты. За плечами у нас не было опыта использования никакого фреймворка, разве что [Backbone](http://backbonejs.org/), но фреймворком его можно назвать лишь с натяжкой. Проект же требовал довольно развесистого веб-приложения. Мы немного пощупали [Ember](https://emberjs.com/), посмотрели на [React](https://reactjs.org/), даже попытались воспользоваться Backbone+[Marionette](https://marionettejs.com/), но в итоге остановились на Angular. Порой он причинял нам боль, порой мы упирались в совершенно необъяснимое поведение. С трудом перешли на 4 версию, чуть менее кроваво на 5. Но, несмотря на все трудности, я ни разу не пожалел об этом выборе.

И вот теперь, спустя более чем 2,5 года, хочется собрать воедино то, чему мы научились за это время. Вообще, у Angular прекрасная документация на официальном сайте, но в ней раскрываются далеко не все тонкости его использования, не говоря уже о тонкостях смежных инструментов, таких как [RxJS](http://reactivex.io/rxjs/), [Zone.js](https://github.com/angular/zone.js/) и [Angular-CLI](https://github.com/angular/angular-cli). Также некоторые моменты упоминаются лишь вскользь, скрывая подробности. Многие вещи находились нами в задачах на GitHub, в обсуждениях на Stack Overflow, в комментариях к статьям на различных ресурсах. Находилось, терялось, находилось заново, тонуло в истории чатов, порой устаревало и портило нам кровь при обновлении. Так что было решено сделать цикл статей, посвящённых этому замечательному фреймворку и всему, что с ним связано.

Это заголовочный пост, в котором я буду собирать ссылки на остальные посты и на который буду из них ссылаться. Этот цикл статей вряд ли будет связан и его не надо воспринимать как этакую блог-книгу, хотя буду стараться и в этом направлении тоже. А пока вот примерное оглавление этого цикла:

* **Первый проект** — создаём новый проект и разбираемся что там и для чего.
* **Компоненты, сервисы и модули** — что такое компоненты, директивы, сервисы, каналы и модули. Когда что использовать.
* **Язык шаблонов** — по сути переизложение того, что есть в официальной документации, только на русском.
* **Пишем свою структурную директиву** — директивы, меняющие разметку.
* **Канал он же Pipe** — что такое чистые каналы и от чего они пачкаются. Передача параметров и прочее.
* **Достучаться до потомка** — различные способы получать вложенные элементы.
* **Ренедерер и различные указатели** — почему и для чего существуют все эти `ElementRef` и `TemplateRef`, почему не вернуть нормальный `HTMLElement`.
* **Шаблонное программирование** — передача шаблонов, контексты и оутлеты.
* **Формоформирование** — о том как строить формы, валидировать, обрабатывать, инициировать, очищать и прочее.
* **Пишем свой контрол** — напишем свой `select` с древовидной структурой, поиском, фильтрацией и валидацией.
* **Роутинг** — где и как прописывать роутинг, как передавать параметры, ленивая подгрузка, гварды и иже с ними.
* **Модули** — хитрости написания и подключения модуля.
* **Внедрение зависимостей** — о том как работает внедрение зависимостей, как подменять и расширять системные сервисы.
* **Грузите апельсины бочками** — или о том как обмениваться информацией между различными компонентами.
* **Пишем свой декоратор** — изучаем такую фичу TypeScript как декоратор.
* **Больше стектрейсов, длинных и красных** — о том что такое `Zone.js`, откуда у него растут ноги и как его можно применять.
* **Хитрости и рецепты использования RxJS** — набор полезных рецептов, когда реактивное программирование решает задачу просто и красиво.

Постараюсь писать по статье в неделю, но не обещаю. Также возможно, что выходить статьи будут не по указанному порядку. Пишите предложения о том какие темы вы бы хотели увидеть ещё.