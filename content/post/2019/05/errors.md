---
title: Полезные приёмы по работе с ошибками в Go
description: Я стою у моря и ищу ответа, вижу исчезает призрачный твой след
date: 2019-05-04T19:12:14Z
draft: false
categories:
- develop
tags:
- go
- architect
- tips and tricks
toc: true
---

Язык Go поощряет использование возвращаемых ошибок, при этом не накладывая больших ограничений на то, что скрывается внутри самой ошибки. Несмотря на многословность, подобную практику можно выгодно использовать. Давайте посмотрим какие удобные способы работы есть с ошибками.

## pkg/errors

Первое, что необходимо включить в свой проект, это библиотеку [github.com/pkg/errors](https://github.com/pkg/errors), которая позволяет быстро конструировать ошибки, а также добавлять контекст и, конечно, стек вызова. Лично у меня пальцы уже автоматом набирают
```go
return errors.WithStack(err)
```

Одной из ключевых особенностей ошибок, созданных с помощью пакета, является то, что у них есть метод [`Cause`](https://godoc.org/github.com/pkg/errors#Cause), позволяющий получить первоначальную ошибку. Так что ниже по тексту будем также имплементировать необходимый интерфейс.

### Разворачивание ошибки

Оборачивание ошибки удобно для получения контекста, но могут возникнуть сложности с получением промежуточного результата. В этом случае поможет небольшой хелпер:
```go
// Cast something from errors in stack
func Cast(err error, cast func(error) bool) bool {
	type causer interface {
		Cause() error
	}

	for {
		if cast(err) {
			return true
		}
		if cause, ok := err.(causer); ok {
			err = cause.Cause()
			continue
		}
		return false
	}
}
```

Этот хелпер является стандартным способом при работе с пакетом `github.com/pkg/errors`. Он последовательно снимает обёртки с ошибки.

## Константные ошибки

Когда речь заходит о библиотеке, оказывается удобным иметь список всех возможных ошибок, которые могут вернуть библиотечные функции. С другой стороны константные ошибки оказываются полезными для универсализации ошибок сторонних библиотек. Так, например, можно абстрагироваться от ошибок драйверов баз данных, введя собственную ошибку `NotFound`. Нет ничего проще чем создать константную ошибку:
```go
// ConstantError is a string with method Error
type ConstantError string

// Error implements error interface
func (ce ConstantError) Error() string {
    return string(ce)
}

const (
    // NotFound means that requested resource is not found
    NotFound ConstantError = "not found"
)
```

Чаще всего рядом с ошибкой нужно хранить дополнительную информацию, ведь нужно понимать что именно не найдено. Это легко сделать с помощью пакета `github.com/pkg/errors`, но ещё удобнее сделать для этого несколько шорткатов:
```go
// New wrapped constant error with message and stacktrace
func (ce ConstantError) New(msg string) error {
    return errors.Wrap(ce, msg)
}

// New wrapped constant error with formated message and stacktrace
func (ce ConstantError) Newf(format string, args ...interface{}) error {
    return errors.Wrapf(ce, format, args...)
}
```

Также можно сделать небольшую обёртку для других ошибок:
```go
type constantErrorWrapper struct {
    ConstantError
    origin error
}

// Wrap external error in constant
func (ce ConstantError) Wrap(err error) error {
    if err == nil {
        return nil
    }
    return errors.WithStack(&constantErrorWrapper{ce, err}, err.Error())
}

func (wrap constantErrorWrapper) Error() string {
    return fmt.Sprintf("%s: %s", wrap.ConstantError.Error(), wrap.origin.Error())
}

func (wrap constantErrorWrapper) Cause() error {
    return wrap.ConstantError
}
```

Благодаря реализованному методу `Cause` соответствующая функция пакета `github.com/pkg/errors` вернёт именно константную ошибку, а не оригинальную, так что обработка ошибки не измениться. К тексту ошибки припишется текст оригинальной ошибки. Кроме того, если понадобится извлечь оригинальную ошибку, можно реализовать следующий хелпер:
```go
func OriginalError(err error) error {
    var orig error
    ok := Cast(err, func(err error) bool {
        wrap, ok := err.(*constantErrorWrapper)
        if ok {
            orig = wrap.origin
        }
        return ok
    })
    if !ok {
        orig = err
    }
    return orig
}
```

## Передача ошибок

Константные ошибки легко обрабатывать, а также конвертировать в ошибки протокола интерфейса сервиса. Для этого можно написать небольшие хелперы:
```go
func HandleHTTPError(w http.ResponseWriter, err error) {
    switch errors.Cause(err) {
    case NotFound:
        http.Error(w, err.Error(), http.StatusNotFound)
    // ...
    default:
        http.Error(w, err.Error(), http.StatusInternalServerError)
    }
}
```

А для протокола gRPC вообще можно реализовать удобные [перехватчики]({{<ref "../01/decorators.md">}}#перехватчики):
```go
func UnaryServerInterceptor(
    ctx context.Context, req interface{},
    info *grpc.UnaryServerInfo, handler grpc.UnaryHandler,
) (interface{}, error) {

    err := handler(ctx, req)
    switch errors.Cause(err) {
    case NotFound:
        return grpc.Error(codes.NotFound, err.Error())
    // ...
    }
    return err
}

func UnaryClientInterceptor(
    ctx context.Context, method string, req, reply interface{},
    cc *grpc.ClientConn, invoker grpc.UnaryInvoker,
    opts ...grpc.CallOption,
) error {

err := invoker(ctx, method, req, reply, cc, grpcOpts...)
    if status, ok := status.FromError(err); ok {
        switch status.Code() {
        case codes.NotFound:
            return NotFound.New(status.Message())
        // ...
        }
    }
    return err
}
```

## Ошибка с данными

Часто для сложных ошибок необходимо также передать какие-то дополнительные данные, например, если ошибка произошла при валидации каких-то входных данных, полезно передать вызывающей стороне: какое поле входных данных содержит ошибку. Тогда можно сделать обёртку над ошибкой:
```go
type errorWithData struct {
    cause error
    data  interface{}
}

// WithData add data to error
func WithData(err error, data interface{}) error {
    return &errorWithData{err, data}
}

func (ewd *errorWithData) Error() string {
    return ewd.cause.Error()
}

func (ewd *errorWithData) Cause() error {
    return ewd.cause
}

// DataFromError extract data from errors in stack if any
func DataFromError(err error) interface{} {
    var data interface{}
    Cast(err, func(err error) bool {
        ewd, ok := err.(*errorWithData)
        if ok {
            data = ewd.data
        }
        return ok
    })

    return data
}
```

Кроме того можно имплементировать методы сериализации (например, `MarshalJSON`), тогда с помощью хелпера можно передавать ошибку в ответе в сериализованном виде.

## panic / recover

Считается, что это не очень хорошая практика, однако, при должной осторожности она позволяет уменьшать количество рутинного кода. Основная идея в том, чтобы не возвращать ошибку, а выкидывать панику с ней, а на верхнем уровне её ловить и возвращать уже в виде ошибки. Важно здесь соблюдать 2 правила:
1. публичные функции не должны паниковать, если это обрабатываемая ошибка;
2. не надо превращать системные паники в ошибки;

Первое правило необходимо для согласованности интерфейсов. Хотя, в нём могут быть исключения, но такие функции надо называть с приставкой `Must`. Второе правило необходимо для того, чтобы сохранить стек вызовов, иначе отладка может превратиться в ад.

И здесь нам тоже поможет пакет `github.com/pkg/errors`. Собственно будем все ошибки перед тем как передавать в панику оборачивать `errors.WithStack`, а на верхнем уровне создадим следующую обёртку:
```go
func DoSomething() (err error) {
    defer func() {
        type causer interface {
            error
            Cause() error
        }
        r := recover()
        if c, ok := r.(causer); ok {
            err = c
        } else {
            panic(r)
        }
    }()

    mustDoSomething()
}
```

Таким образом паники, которые выкинуты нами будут превращены в ошибки, а остальные прокинуты выше. Ярким примером использования такого подхода является стандартный пакет [encoding/json](https://golang.org/src/encoding/json/encode.go#L296).

## Ошибка на классе

Иногда бывает необходимо сохранить интерфейс определённого метода без возвращаемой ошибки, например, для создания итератора удобно иметь метод `Next`, который возвращает `true` или `false`. Если же логика этого метода подразумевает возникновение ошибки, то необходимо сохранить её на уровне класса, так чтобы позже можно было её проверить и обработать. Хороший пример такого подхода можно посмотреть в стандартной библиотеке [bufio](https://godoc.org/bufio#Scanner). Конечно, эту ошибку необходимо будет учитывать в других методах класса, заранее их прерывая.