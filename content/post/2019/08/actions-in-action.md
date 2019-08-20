---
title: Действия в действии
description: Различные полезные практики в написании действий
date: 2019-08-20T10:00:06Z
draft: true
categories:
- develop
tags:
- go
- architect
- microservices
- tips and tricks
toc: true
---

В статье [Чистая архитектура на Go]({{<ref "clean-architect">}}) предлагается изолировать бизнес-логику микросервиса в так называемых _Действиях_. В данной статье разбираются различные наработанные практики и подходы по написанию Действий.

## DIContainer

Практически любое действие так или иначе зависит от внешних систем, будь то база данных, файловая система, часы или логер. Всё, что связано с побочными эффектами. Собрать все зависимости в один объект, идея не новая, но в контексте Go несколько кропотливая. Итак, до создания первого действия необходимо описать зависимости. Для этого можно в пакете `action` создать файл `di_container.go` примерно следующего содержания:
```go
package action

import (
	"github.com/jonboulle/clockwork"
	"go.uber.org/zap"
)

// DIContainer is a dependency injection container
type DIContainer interface {
	GetClock() clockwork.Clock
	GetLogger() *zap.Logger
}
```

Две обязательные зависимости — часы и логер, они позволяют не использовать глобальные переменные (для того же логера) и легко тестировать код.

Дальше, при необходимости интерфейс контейнера может расширяться необходимыми сервисами и репозиториями. Например, часто необходимо использовать транзакции при работе с базами данных. Транзакционность тех или иных действий является частью бизнес-логики, но механизм реализации транзакции зависит от драйвера бд, что выходит за пределы зоны ответственности действий, поэтому можно добавить соответствующую зависимость:
```go
type DIContainer interface {
    // ...
    GetTxManager() TxManager
}

// TxManager is a service to wrap part of logic in transaction
type TxManager interface {
    WithTx(context.Context, func(context.Context) error) error
}
```

Или, если необходимо работать с коллекцией каких-то объектов, можно добавить соответствующую зависимость:
```go
type DIContainer interface {
    // ...
    GetUserRepository() UserRepository
}

// UserRepository is a persistence layer of user-objects
type UserRepository interface {
    ListAll(context.Context) ([]model.User, error)
    GetByID(ctx context.Context, id string) (model.User, error)
    GetByEmail(ctx context.Context, email string) (model.User, error)
    // ...
}
```

Описав контейнер зависимостей можно приступить к описанию действий.

## Интерфейс действия

В общем случае действие должно выглядеть как функция, которая принимает контекст исполнения, зависимости и необходимые параметры. Например,
```go
```

## Действие как объект

## Базовое действие

## Несколько точек входа

## Опции
