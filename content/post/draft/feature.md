---
title: Работа над фичей
description: No, I'm not dead – I'm just sleeping
date: 2021-07-14T00:11:47+0400
draft: true
categories:
- develop
tags:
- tutorial
- work
- management
toc: true
---

Добавление или изменение функционала является обычно преобладающим по объёму и сложности типом задач. Если это не так, то скорее всего это уже не разработка, а поддержка или выживание.

### О важности документации

Обычно жизненный цикл продукта можно разделить на три этапа:
1. **Исследование.** Редко, когда в продукт сразу вкладывают большие ресурсы. Чаще всего начинается всё с маленькой группы людей (то, что с подачи Джеффа Безоса стали называть [Two-Pizza Team](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/two-pizza-teams.html)). На этой стадии создаётся корневой функционал продукта, то что станет его конкурентным преимуществом. В этот период много времени должно уходить на проектирование, потому как это фундамент будущего продукта. На этой стадии можно переписать значительную часть кодовой базы, если оказывается, что текущая архитектура не позволяет оптимально реализовать требования.
2. **Основной период.** В этот период продукт уже выходит на рынок и у него появляются реальные пользователи. Эти пользователи предлагают улучшения и находят баги. В этот период продукт активно развивается, наращивается функционал. Но фундамент, заложенный на первом этапе трогается редко, часто из-за накопленной кодовой базы, или от того, что в каждый момент времени в разработке есть новый функционал, привязанный к текущей архитектуре, так что невозможно просто остановиться и исправить корневые ошибки.
3. **Поддержка.** Далее возможны два варианта развития продукта: запрос на новый функционал отсутствует либо текущий продукт не может удовлетворить имеющийся запрос. Первый случай возможен из-за схлопнувшейся ниши, либо из-за сильного конкурента, захватившего рынок. Второй случай может оказаться отправной точкой для нового продукта, который вберёт в себя экспертизу текущего продукта, но окажется избавлен от некоторых ключевых недостатков.

При переходах от этапа к этапу обычно сильно меняется команда. Возможно, что некоторая корневая часть команды будет сохраняться, но основная часть чаще всего будет новой. При этом важнейшим ресурсом для такой смены команды является документация. Документация должна отвечать на следующие вопросы:
- Какой функционал реализуется в продукте?
- Какие задачи решает тот или иной участок кода?
- Почему выбрано то или иное решение?
- Рассматривались ли альтернативные варианты решения и, если да, то почему были отклонены?
- Какие участки кода затрагиваются определённым сценарием пользования?
- Какие сущности создаются и/или изменяются в рамках сценария пользования?
- Как проверить корректность работы сценария пользования?
- Как система должна вести себя в граничных условиях?

Ответы на эти вопросы должны закладываться в рамках проработки функционала и фиксироваться для дальнейшего использования. Если это не делается, то последующие изменения продукта будут вызывать всё больше сложностей, всё больше времени будет уходить на восстановление контекста работы. Помните картинку про состояние потока и как легко из него выбивает сообщение в чате? Так вот, чем меньше документации, тем более хрупким становится это состояние потока.

## Функционал

Для начала давайте отделим задачи-фичи от всех остальных задач. Критерий на самом деле тут только один:

{{<blockquote>}}
Добавление или изменение функционала всегда сопровождается изменением пользовательской документации.
{{</blockquote>}}

При этом нужно помнить, что пользователями системы являются не только клиенты, но отделы внутри компании:
- внедрение и сопровождение;
- бизнес-аналитики и визионеры;
- администраторы и операторы;

Таким образом, если в проект вводится новая метрика для аналитики использования имеющегося функционала, это новый функционал, который должен быть зафиксирован в документации.

Задачи на добавление или изменения функционала должны проходить следующие стадии.

### Постановка



### Аналитика

### Проектирование

### Согласование

### Декомпозиция

### Реализация

### Документация

### Ревью изменений

### Тестирование и приёмка

### Особенности больших фич

### Изменения поведения существующих фич

Прохождение по этому чек-листу позволит избежать лишних итераций и ненужной работы при выполнении задачи.

- **Получить и описать исходную проблему.** Часто задачи формулируются как некоторое решение, пришедшее в голову Автору задачи. Иногда решение поставленной задачи в другом виде уже реализовано в системе или предложенное решение идёт в разрез с концепциями платформы. Для дальнейшей работы над задачей необходимо исходная постановка задачи. Постановка может быть сформулирована как несоответствие поведения системы описанному в справке (ошибка), либо содержать бизнес-сценарий, который предполагается решать с помощью доработки.
- **Пользовательский сценарий.** Имея формализованную исходную проблему, необходимо описать и согласовать с автором задачи пользовательский сценарий. Сценарий должен описывать действия пользователя в системе после выполнения задачи, для решения описанного в исходной проблеме бизнес-сценария. Пользовательский сценарий может быть существующим тест-кейсом (ошибка), либо превратиться в него.
- **Проработка архитектуры.** Для любых изменений необходимо проработать архитектуру решения. Она должна отвечать на следующие вопросы:
    - Какие сервисы затрагивают изменения?
    - Какие сущности добавляются/изменяются/удаляются?
    - Где хранятся новые сущности?
    - Какие сценарии системы добавляются/изменяются/удаляются?
    - Как передаётся управления между сервисами во время выполнения новых или изменённых сценариев?
- **Проработка интерфейса.** Любое изменение в системе (кроме технического долга и инфраструктурных) в каком-то виде изменяет пользовательский интерфейс системы. Это может быть frontend, API или TS SDK. Решение задачи всегда следует начинать с проработки видимых пользователю изменений. Для API изменения необходимо задокументировать в виде swagger-описания, для TS SDK в виде d.ts описания, а для frontend'а в виде прототипа со стабами. Создав описание изменений интерфейса необходимо согласовать его с Автором. Согласование лучше всего проводить в виде созвона, в результате которого собрать фидбэк и предложения по улучшению. Применив фидбэк согласовать конечный вариант, внести его в Пользовательский сценарий и Архитектуру.
- **Оценка и декомпозиция.** После согласования пользовательского сценария, архитектуры и интерфейса задачу можно брать в работу, предварительно оценив. Если оценка неочевидна или больше 8 исторических точек, то необходимо выделить отдельные задачи «исследования», в рамках которых проработать рисковые или неопределённые моменты.
- **Описание изменений.** В процессе выполнения задачи необходимо формировать файл с изменениями doc/changes/TEAM-XXX new feature.md. В этом файле по мере внесения изменений необходимо фиксировать добавленные/изменённые/удалённые сущности с описанием причин изменений. Данный файл позволит вовремя найти отклонение от начальной Архитектуры, а также позволит ускорить ревью кода.

