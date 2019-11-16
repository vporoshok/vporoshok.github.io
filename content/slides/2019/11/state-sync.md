---
title: Синхронизация состояния в распределённых системах
description: Распределённые системы имеют кучу подводных граблей, о которых часто забывают или не задумываются. Синхронизация состояния сама по себе нетривиальная задача, которой посвящены многие работы. А уж если состояние распределено по системе…
date: 2019-11-16T12:24:33Z
draft: true
mermaid: true
---

<style>
.middle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>

{{<slide id="title" title="Синхронизация состояния в распределённых системах" class="clear section black"/>}}

{{<slide id="hello" title="Всем привет!">}}
- Бастрыков Евгений
- Программирую с 2013
- Преподаю «Алгоритмы и структуры данных»
- Разрабатываю QuickBPM
<p class="note"><a href="https://vporoshok.me" target="_blank">vporoshok.me</a></p>
{{</slide>}}

{{<slide title="План" class="toc" id="toc">}}
1. [кеш во внешнем сервисе](#redis)
2. [кеш внутри сервиса](#local)
3. [шардирование](#sharding)
{{</slide>}}

{{<slide shout="true" title="Не используйте, если можете" />}}

{{<slide title="Кеш во внешнем сервисе" class="section" id="redis" />}}

{{<slide title="Кеш во внешнем сервисе">}}
<center class="middle">
Распределённая = Конкурентная
</center>
{{</slide>}}

{{<slide title="Кеш во внешнем сервисе">}}
Идеален, если
- чистые данные
- не меняются
- подготовка занимает время/ресурсы
{{</slide>}}

{{<slide title="Кеш во внешнем сервисе">}}
Проблемы:
<ul>
- гонка на создании <span class="next">(трата ресурсов)</span>
<li>гонка на обновление <span class="next">(атомарное обновление: inc/dec/CAS)</span>
<li class="next">гонка создания и обновления
</ul>
{{</slide>}}

{{<slide title="Кеш во внешнем сервисе">}}
{{<mermaid>}}
sequenceDiagram
    participant Client 1
    participant A
    participant Redis
    participant B
    participant Client 2
    Client 1->>+A: Get
    Note right of A: Prepare
    Client 2->>+B: Inc
    B->>Redis: Inc
    Redis->>B: Not found
    B->>-Client 2: OK
    A->>Redis: Set
    A->>-Client 1: OK
{{</mermaid>}}
{{</slide>}}

{{<slide title="Локи" class="clear section black" />}}

{{<slide title="Кеш во внешнем сервисе">}}
Проблемы:
- гонка на создании (трата ресурсов)
- гонка на обновление (атомарное обновление: inc/dec/CAS)
- гонка создания и обновления (блокировки)
{{</slide>}}

{{<slide>}}
```lua
local c = redis.call("HGET", KEYS[1], ARGV[1])
if c == nil or tonumber(c) <= -tonumber(ARGV[2]) then
    redis.call("HDEL", KEYS[1], ARGV[1])
    return 0
end
redis.call("HINCRBY", KEYS[1], ARGV[1], ARGV[2])
local updatedCount = redis.call("HGET", KEYS[1], ARGV[1])
return tonumber(updatedCount)
```
{{</slide>}}

{{<slide title="Кеш внутри сервиса" class="section" id="redis" />}}

{{<slide title="Кеш внутри сервиса">}}
Почему?
- Не просто данные
- Нагрузка на сеть
{{</slide>}}

{{<slide title="Кеш внутри сервиса">}}
Что можно делать?
- Создавать
- Читать
- ~~Менять~~
- Инвалидировать
{{</slide>}}

{{<slide title="Кеш внутри сервиса">}}
Оповещение об инвалидации:
- gossip
- message queue
- key-value
{{</slide>}}

