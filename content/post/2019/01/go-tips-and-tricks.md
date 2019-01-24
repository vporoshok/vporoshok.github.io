---
title: Go tips and tricks
description: Подсмотрено, скопировано, проверено. Практики удобного программирования
date: 2019-01-21T17:25:58Z
draft: true
categories:
- develop
tags:
- go
- tips and tricks
toc: true
---

Довольно большая часть моей работы заклчается в написании библиотечного кода. Кода, который будет многократно использоваться другими программистами, в том числе и мной самим. Так что одним из важных критериев кода становится удобство интерфейсов. Некоторые практики, применяемые для интерфейсов библиотек рассмотрены в этой статье.

## Middleware

Концепция middleware появилась, конечно, задолго до go. Однако, именно в go эта концепция достигла своего апогея. Собственно про middleware написано и сказано много. В качестве примера можно рассмотреть middleware для логирования запросов к http-сервису:
```go
func Logging(next http.Handler) http.Handler {

    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("request start: %s", r.URL)
        hext(w, r)
        log.Printf("request end: %s", r.URL)
    })
}
```

По сути это функция, оборачивающая обработчик запроса, то есть декоратор. В таких обёртках удобно делать рутинные задачи, не имеющие привязки исключительно к одному обработчику:
- перехват паник;
- телеметрия (логи / метрики / трейсинг);
- лимитирование (ограничение количества запросов или прерывание запроса по времени);
- проверка авторизации и прав доступа по кукам и заголовкам;
- извлечение информации из запроса;

Последний пункт расширяемый. По факту в запросе имеется контекст, через который можно передавать информацию выше по стеку, таким образом можно не только извлечь информацию из запроса, но и по этой информации извлечь информацию из бд и положить в контекст готовый объект. Но тут есть свои нюансы и священные войны о том для чего можно использовать контекст, а для чего нет.

Главным удобством таких функций является общая сигнатура:
```go
type Middleware func(http.Handler) http.Handler
```
что позволяет легко сделать их объединение (композицию):
```go
func Combine(middlewares ...Middleware) Middleware {

    return func (next http.Handler) http.Handler {
        // let's keep the order as in mathematical functional composition
        for i := len(middlewares) - 1; i >= 0; i-- {
            next = middlewares[i](next)
        }

        return next
    }
}
```

Концепция таких промежуточных перехватчиков настолько прижилась, что практически каждый сторонний роутер в том или ином виде предоставляет удобные механизмы для их использования. Например, в chi можно объявлять перехватчики глобальные для данного уровня дерева путей с помощью метода [Use](https://godoc.org/github.com/go-chi/chi#Mux.Use) или специфичные для конкретного пути --- [With](https://godoc.org/github.com/go-chi/chi#Mux.With).

Аналогичные механизмы есть и в grpc, только там они называются [перхватчиками (interceptors)](https://godoc.org/google.golang.org/grpc#UnaryInterceptor). Но можно ли расширить эту концепцию дальше, за пределы http и grpc сервисов?

## Общий случай

По сути перехватчики являются декораторами функций. Решающим фактором в перехватчиках является общая сигнатура. Таким образом можно реализовать свой слой декораторов, не привязанный к транспортному уровню. Для начала определим собственную сигнатуру. На практике нам достаточно передавать вверх по стеку контекст запроса, а возвращать только ошибку:
```go
type Handler func(context.Context) error
type Middleware func(Handler) Handler
```

На таких функциях также легко реализовать функцию композицию по аналогии с вышеприведённой. Такие декораторы удобно использовать для
- телеметрии (логи / метрики / трейсинг);
- обработки ошибок (retry / backoff);
- ограничения (времени / частоты / конкурентности);

## Замыкания

Но чаще всего функции бизнес-логики принимают что-то помимо контекста, а также возвращают что-то помимо ошибки. Давайте рассмотрим в качестве примера следующую задачу: дана директория с фотографиями, необходимо посчитать среднюю освещённость по всем фотографиям. Саму бизнес-логику мы писать не будем, предположим, что у нас есть уже написанная функция, которая принимает на вход путь до файла, а возвращает среднюю освещённость фотографии.
```go
func ProcessFile(ctx context.Context, path string) (float64, error) {
    // ...
}
```

И пусть у нас есть список файлов, которые необходимо обработать, но обработку каждого файла хочется покрыть метриками, прерывать обработку, если прошло больше 5 секунд без результата, а также повторить попытку при ошибке. Если у нас уже есть необходимые декораторы и функция `Combine`, то код может выглядеть примерно так:
```go
var exposition float64
for _, path := range paths {
    err := Combine(
        // Повторяем 3 раза в случае ошибки
        Retry(3),
        // Логируем время начала и конца обработки
        Logger(log.New(os.Stderr, path, log.LstdFlags)),
        // Ограничиваем время выполнения
        Timout(5 * time.Second),
    )(func(ctx context.Context) error {
        fileExposition, err := ProcessFile(ctx, path)
        if err != nil {

            return err
        }
        exposition += fileExposition

        return nil
    })(context.Background())
    if err != nil {
        log.Fatal(err)
    }
}

log.Printf("average exposition is %.4f", exposition / len(paths))
```

При этом, для внутренних декораторов можно делать обмен данными через контекст. Например, декоратор `Retry` может класть в контекст номер попытки, который будет логироваться в декораторе `Logger`. С другой стороны композицию декораторов можно было вообще определить за пределами цикла, если `Logger` будет брать сообщение из контекста. Предположим, что мы вынесли код всех декораторов и вспомогательный функции в отдельный модуль под названием `wrap`, тогда код можно переписать следующим образом:
```go
processWrapper := wrap.Combine(
    // Повторяем 3 раза в случае ошибки
    wrap.Retry(3),
    // Логируем время начала и конца обработки
    wrap.Logger(log.New(os.Stderr, "", log.LstdFlags)),
    // Ограничиваем время выполнения
    wrap.Timout(5 * time.Second),
)

var exposition float64
for _, path := range paths {
    err := processWrapper(func(ctx context.Context) error {
        fileExposition, err := ProcessFile(ctx, path)
        if err != nil {

            return err
        }
        exposition += fileExposition

        return nil
    })(wrap.ContextWithTarget(context.Background(), path))
    if err != nil {
        log.Fatal(err)
    }
}

log.Printf("average exposition is %.4f", exposition / len(paths))
```

Таким образом, используя некоторый базовый набор декортаторов, можно практически декларативно описывать окружение бизнес-логики.

## Прямые вызовы

Лично для меня, не смотря на математическое образование, читать такие обратные вызовы, то есть когда обработчик передаётся в декоратор, который возвращает декорированный обработчик, в который уже передаётся контекст, достаточно сложно. Поэтому я предпочитаю более прямой способ записи:
```go
func WithLogging(ctx context.Context, logger *log.Logger, next Handler) error {

    return Logging(logger)(next)(ctx)
}
```

Что позволяет более вызывать декоратор следующим образом:
```go
err := wrap.WithLogging(ctx, logger, func(ctx context.Context) error {
    // ...
})
```

Или можно по аналогии с `http.HandlerFunc` определить метод `Apply` на декораторе:
```go
type Handler func(context.Context) error
type Middleware func(Handler) Handler

func (mw Middleware) Apply(ctx context.Context, handler Handler) error {

    return mw(handler)(ctx)
}
```

После чего вызов будет выглядеть так:
```go
err := wrap.Logging(logger).Apply(ctx, func(ctx context.Context) error {
    // ...
})
```

Или пример с обработкой файлов:
```go
var exposition float64
for _, path := range paths {
    ctx := wrap.ContextWithTarget(context.Background(), path)
    err := processWrapper.Apply(ctx, func(ctx context.Context) error {
        fileExposition, err := ProcessFile(ctx, path)
        if err != nil {

            return err
        }
        exposition += fileExposition

        return nil
    })
    if err != nil {
        log.Fatal(err)
    }
}
```

Что на мой взгляд читает несколько легче.
