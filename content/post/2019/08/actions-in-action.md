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
// action/login.go
package action

import (
    "context"
)

// Login find user, check password and return authentication token
func Login(
    ctx context.Context, di DIContainer, email, password string,
) (token string, err error) {

    // ...
}
```

## Действие как объект

Конечно, часто одной функции оказывается мало для реализации действия, кроме того, возникает множество промежуточных данных, которые необходимо сохранять между шагами. Так что удобно сделать структуру со всеми необходимыми полями, а логику разбить на методы, привязанные к этой структуре, выделив метод точки входа `Do`
```go
type LoginAction struct {
    di   DIContainer
    user model.User
    cert []byte
    key  []byte
}

// Login find user, check password and return authentication token
func Login(
    ctx context.Context, di DIContainer, email, password string,
) (token string, err error) {

    act := &LoginAction{
        di: di,
    }

    return act.Do(ctx, email, password)
}

func (act *LoginAction) Do(
    ctx context.Context, email, password string,
) (string, error) {

    user, err := act.di.GetUserRepository().GetByEmail(ctx, email)
    if err != nil {
        return "", err
    }
    act.user = user
    if err := act.checkPassword(password); err != nil {
        return "", err
    }
    if err := act.getSecrets(ctx); err != nil {
        return "", err
    }
    // ...
}

func (act *LoginAction) checkPassword(password string) error {
    // ...
}
```

## Базовое действие

Удобно также оказывается выделить базовое действие, от которого «наследовать» остальные. Например, можно добавить в виде свойства логер определить метод его инициализации:
```go
// action/base_action.go
package action

import (
    "context"

    "go.uber.org/zap"
)

type BaseAction struct {
    di     DIContainer
    logger *zap.SugaredLogger
}

func (act *BaseAction) Init(ctx context.Context, di DIContainer, instance interface{}) {
    act.di = di
    actName := reflect.TypeOf(instance).Elem().Name()
    act.logger = LoggerWithTraceID(ctx, di.GetLogger()).Named(actName).Sugar()
}
```

Где функция `LoggerWithTraceID` аннотирует логер идентификатором запроса. Тогда обычное действие можно записать так:
```go
func Login(
    ctx context.Context, di DIContainer, email, password string,
) (token string, err error) {

    act := new(LogginAction)
    act.Init(ctx, di, act)

    return act.Do()
}
```

## Несколько точек входа

## Опции
