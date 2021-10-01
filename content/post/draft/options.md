---
title: Опции вызова функции
description: Open up inside, make me want you, make me want to
date: 2021-04-09T12:38:53Z
draft: true
categories:
- develop
tags:
- go
- architect
- tips and tricks
toc: true
---

Одним из частых комментариев на моих ревью является фраза: «Давай сделаем это опцией». Часто это предложение пугает разработчиков. Действительно, если следовать оригинальному примеру, то добавить опцию оказывается довольно муторным делом. Но часто опции можно ввести намного проще и лаконичнее. Давайте разбираться.

## «Классические» опции

Пожалуй, самая известная статья про функциональные опции вышла в блоге Дэйва Чейни в 2014 году [Functional options for friendly APIs
](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis). Эта статья является обобщением статьи Роба Пайка [Self-referential functions and the design of options](https://commandcenter.blogspot.com/2014/01/self-referential-functions-and-design.html). В статье рабираются различные способы конфигурирования при вызове функций, их плюсы и минусы. Как самое оптимальное решение приводится реализация конфигурации в виде функциональных опций следующего вида:
```go
func NewServer(addr string, options ...func(*Server)) (*Server, error) {
	l, err := net.Listener("tcp", addr)
	if err != nil {
		return nil, err
	}
	srv := Server{Listener: l}

	for _. opt := range options {
		opt(&srv)
	}
	return &srv, nil
}

func main() {
	timeout := func(srv *Server) {
		srv.Timeout = 60 * time.Second
	}
	tls := func(srv *Server) {
		config := loadTLSConfig()
		srv.Listener = tls.NewListener(srv.Listener, &config)
	}
	srv, _ := NewServer("", timeout, tls)
}
```

Позже опции перестали быть функциональными, потому что «программисты боятся функций» (?!), а для закрытия имплементации опции превратились и вовсе вот в такое:
```go
// dialOptions configure a Dial call. dialOptions are set by the DialOption
// values passed to Dial.
type dialOptions struct {
	// ...
}
// DialOption configures how we set up the connection.
type DialOption interface {
	apply(*dialOptions)
}

// funcDialOption wraps a function that modifies dialOptions into an
// implementation of the DialOption interface.
type funcDialOption struct {
	f func(*dialOptions)
}

func (fdo *funcDialOption) apply(do *dialOptions) {
	fdo.f(do)
}

func newFuncDialOption(f func(*dialOptions)) *funcDialOption {
	return &funcDialOption{
		f: f,
	}
}

// WithWriteBufferSize determines how much data can be batched before doing a
// write on the wire. The corresponding memory allocation for this buffer will
// be twice the size to keep syscalls low. The default value for this buffer is
// 32KB.
//
// Zero will disable the write buffer such that each write will be on underlying
// connection. Note: A Send call may not directly translate to a write.
func WithWriteBufferSize(s int) DialOption {
	return newFuncDialOption(func(o *dialOptions) {
		o.copts.WriteBufferSize = s
	})
}
```

Такая реализация не позволяет создавать опции за пределами пакета с конструктором

## Опции конструктора

## Опции метода

### Метод-конструктор

### Метод-действие

### Снова декораторы
