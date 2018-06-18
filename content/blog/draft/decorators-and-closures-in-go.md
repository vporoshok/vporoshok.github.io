---
title: Декораторы и замыкания в Go
description: Об использовании функций в функциях с замыканиями и прочим
date: 2018-06-14T11:25:23
draft: true
categories:
- develop
tags:
- go
- architech
---

# Декораторы и замыкания в Go

Для чего можно применять декораторы и замыкания:

- метрики / логи / трейсы;
- расширение контекста;
- абстрагирование от имплементации;
- setup / teardown;
- generics https://medium.com/capital-one-developers/closures-are-the-generics-for-go-cb32021fb5b5;
- panic / recover;

Примеры из общепринятых библиотек:

- gRPC / HTTP middleware;
- boltDB transaction;
- backoff;
