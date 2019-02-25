---
title: Применяем рефлексию в go на примере библиотеки chirp
description: Применяем полученные знания о рефлексии для того, чтобы собрать необходимые кусочки запроса в одну структуру
date: 2019-01-06T05:10:16Z
draft: true
categories:
- develop
tags:
- go
- architect
toc: true
---

## Используем рефлексию

Что ж, попробуем что-нибудь соорудить с полученным багажом знаний. Например, решим следующую задачку: при работе с роутером [chi](https://godoc.org/github.com/go-chi/chi) приходится собирать входные данные запроса из кусочков пути, query-параметров, а также самого тела запроса. Также хочется, чтобы обработчик запроса мог работать как с POST-запросом в формате формы, так и с json данными. Ну, и, конечно, все поля хочется провалидировать перед непосредственным выполнением, так что удобно их собрать в одну структуру и на ней развесить тэги валидации. Задача рутинная и не несёт бизнес-логики.

Давайте попробуем автоматизировать эту процедуру. Для этого воспользуемся структурными тэгами. Хочется получить следующий интерфейс использования:
```go
import (
	"net/http"

    "github.com/go-chi/chi"
    "github.com/vporoshok/chirp"
)

func updateUser(w http.ResponseWriter, r *http.Request) {
	var data struct {
		ID       uuid.UUID `url:"id"`
		Name     string    `json:"name"`
		Part     string    `query:"part"`
		Priority uint8     `json:"priority"`
    }

    if err := chirp.Parse(r, &data); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // валидируем данные и выполняем остальные операции
}

func main() {
	router := chi.NewRouter()
    router.Put("/user/{id}/name/{part}", updateUser)
	http.ListenAndServe(":8000", router)
}
```

То есть в структурных тэгах описываем откуда достать данные, а дальше всё делает волшебная функция `Parse`. Поехали!

### Бизнес-логика



### Итерируем по полям структуры

### Присваиваем значения

{{<blockquote author="k8s team" title="Note about space-shuttle code" url="https://news.ycombinator.com/item?id=18772873">}}
```go
// ==================================================================
// PLEASE DO NOT ATTEMPT TO SIMPLIFY THIS CODE.
// KEEP THE SPACE SHUTTLE FLYING.
// ==================================================================
```
{{</blockquote>}}

