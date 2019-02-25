---
title: Не пишите CSS
description: О том как CSS подвержен второму закону термодинамики. Проблемы, заблуждения и способы их решения. О том, почему для больших проектов утилитарные классы оказываются лучше БЭМ
date: 2019-02-24T10:31:26Z
draft: false
# back: /post/2019/01/hackathon/
---

<style>
.title h2 {
    font-weight: bold;
    text-align: right;
}
.shadow figure:after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background-color: rgba(0, 0, 0, 0.3);
}
#stop-digging h2 {
    position: absolute;
    margin-top: 150px;
}
.cards {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: stretch;
    font-size: 0.7rem;
    font-weight: 300;
    line-height: 1.3;
}
.card {
    width: 23%;
    border: 1px solid slateblue;
}
.card img {
    background: lavender;
}
.card img.person {
    display: block;
    width: 80%;
    border-radius: 100%;
    margin: 10px auto 0;
}
.card h3 {
    margin: 5px 10px 5px;
    padding: 0;
    font-size: 1.4em;
    color: darkslateblue;
}
.card .date {
    margin: 0 10px 5px;
    text-align: right;
    color: dimgrey;
    font-style: italic;
}
.summary {
    margin: 5px 10px;
}
.summary a {
    color: darkslateblue;
}

</style>

{{<slide id="title" class="title clear black"
    cover="../img/road_ends.jpg" cover-alt="Road ends sign" cover-copy="Photo by Lubo Minar on Unsplash"
>}}
<h2>Не пишите CSS<br><small class="next">каждый день</small></h2>
{{</slide>}}

{{<slide id="quick-question" title="Как сверстать?">}}
<style>
.center {
position: absolute;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
align-items: center;
}
.celebrity {
display: flex;
width: 500px;
padding: 1.2rem;
border-radius: 1rem;
border: 1px solid dimgrey;
}
.celebrity .photo {
width: 130px;
height: 130px;
object-fit: scale-down;
border-radius: 50%;
background: black;
}
.celebrity .about {
margin-left: 1.2rem;
font-size: 1rem;
}
.celebrity .name {
margin: 1rem 0 1rem;
padding: 0;
font-size: 2rem;
font-weight: bold;
}
.celebrity p:last-child {
margin-bottom: 0;
}
</style>
<div class="celebrity center">
<img class="photo" src="../img/kharper-li.jpg">
<div class="about">
<h2 class="name">Нелл Харпер Ли</h2>
<p class="short">Американская писательница, автор романа «Убить пересмешника», лауреат пулитцеровской премии.</p>
</div>
</div>
<style>
.answer {
position: absolute;
transform: translate(-50%, 0);
}
.answer-1 { bottom: 30%; left: 15%; color: hotpink; }
.answer-2 { bottom: 48%; left: 15%; color: peru; }
.answer-3 { bottom: 66%; left: 15%; color: chocolate; }
.answer-4 { bottom: 70%; left: 50%; color: tomato; }
.answer-5 { bottom: 66%; left: 85%; color: olive; }
.answer-6 { bottom: 48%; left: 85%; color: teal; }
.answer-7 { bottom: 30%; left: 85%; color: slateblue; }
</style>
<div class="answer answer-1 next">flexbox</div>
<div class="answer answer-2 next">float</div>
<div class="answer answer-3 next">absolute</div>
<div class="answer answer-4 next">inline</div>
<div class="answer answer-5 next">grid</div>
<div class="answer answer-6 next">table</div>
<div class="answer answer-7 next">background</div>
{{</slide>}}

{{<slide id="hello" title="Всем привет!">}}
<img style="float:right;width:20%" src="/images/logo-orig.jpg">
- Бастрыков Евгений
- Программирую с 2013
- Преподаю «Алгоритмы и структуры данных»
- Разрабатываю elma365
<p class="note"><a href="https://vporoshok.me" target="_blank">vporoshok.me</a></p>
{{</slide>}}

{{<slide id="toc" title="План" class="toc">}}
1. [Исторический экскурс и семантическая вёрстка](#history)
2. [Проблемы CSS](#troubles-1)
3. [OOCSS и БЭМ](#oocss)
4. [Проблемы контейнеров](#troubles-2)
5. [Препроцессоры](#preprocessors)
6. [Проблемы препроцессоров](#troubles-3)
7. [Как перестать писать CSS?](#stop-digging)
8. [Что дальше?](#next)
{{</slide>}}

{{<slide id="history" title="Исторический экскурс<br>и семантическая вёрстка" class="section black"
    cover="../img/spiral.jpg" cover-alt="Spiral staircase" cover-copy="Photo by Jenny Marvin on Unsplash"
/>}}

{{<slide title="Сначала был HTML">}}
HTML 3.2 (1997)
```html
<img align="right" src="alice.jpg" />
<font face="Arial" size="4" color="firebrick">
    Похоже на экспорт Word'а
</font>
```
{{</slide>}}

{{<slide title="CSS 1.0 (1996)" shout="true" />}}

{{<slide title="Семантическая верстка">}}
```latex
\section{Семантическая вёрстка}
\begin{definition}
    \emph{Семантической} вёрсткой называется разметка
    смысла текста, а не его \textit{оформления}.

    Таким образом оформление отделяется, и может быть
    изменено независимо от содержимого.
\begin{definition}
```
{{</slide>}}

{{<slide id="troubles-1" title="Проблемы CSS" class="section black"
    cover="../img/hole.jpg" cover-alt="Hole in floor" cover-copy="Photo by Quinten de Graaf on Unsplash"
/>}}

{{<slide title="Проблемы CSS">}}
Что хорошо для книги не всегда хорошо для сайта

Книги не расширяются и не изменяются после публикации

Сайты превращаются в порталы, расширяют функциональность, эволюционируют и меняют дизайн
{{</slide>}}

{{<slide title="Проблемы CSS">}}
<ul>
<li>Неоднозначность решения;
<li class="next">Глобальное пространство имён;
<li class="next">Сложность селекторов и определение веса;
<li class="next">Отсутствие наследования;
<li class="next">Влияние оформления контейнера на оформление содержимого;
</ul>
{{</slide>}}

{{<slide title="Сложность селекторов">}}
{{<columns class="two">}}
```css
.blue {
    background: blue;
}
.red {
    background: red;
}
```

```html
<div class="red blue"></div>
```
{{</columns>}}
<style>
.redblue {
position: absolute;
bottom: 120px;
right: 200px;
width: 200px;
height: 200px;
background: red;
}
</style>
<div class="redblue next"></div>
{{</slide>}}

{{<slide title="Специфичность и вес селекторов">}}
```css
input[type~="checkbox"].checkbox + label:before {/*...*/}

[class^="icon-"], [class*=" icon-"] {/*...*/}
```
{{</slide>}}

{{<slide title="Проблема чистого листа"
    cover="../img/blank.jpg" cover-alt="Blank wall prepared to be colored" cover-copy="Photo by rawpixel on Unsplash"
>}}
<ul>
<li>количество компонентов слишком велико
<li class="next">когда надо универсализировать компонент или разделить?
<li class="next">объём CSS растёт геометрически
<li class="next">редизайн в итоге становится практически невозможным
</ul>
{{</slide>}}

{{<slide id="oocss" title="OOCSS и БЭМ" class="section black shadow"
    cover="../img/raspberry.jpg" cover-alt="Raspberry" cover-copy="Photo by Fancycrave on Unsplash"
/>}}

{{<slide title="Object-Oriented CSS">}}
- объект --- повторяющийся компонент;
- объект становится namespace'ом для селекторов;
- отделение формы от оформления;
- объект не должен влиять на оформление содержимого;
{{</slide>}}

{{<slide title="Блок\_\_Элемент\_Модификатор</span>">}}
- блок --- минимальная единица построения интерфейса;
- блоки можно вкладывать друг в друга;
- элементы существуют только внутри блока;
- элементы можно вкладывать друг в друга, но не отражать эту структуру в именах;
- стилизация с помощью модификаторов;
{{</slide>}}

{{<slide title="Какие проблемы решены">}}
- Неоднозначность решения;
- ~~Глобальное пространство имён~~ __уникальные имена__;
- ~~Сложность селекторов и определение веса~~ __один класс__;
- ~~Отсутствие наследования~~ __модификаторы__;
- Влияние оформления контейнера на оформление содержимого;
- __Проблема чистого листа__;
{{</slide>}}

{{<slide title="Страница новостей">}}
<div class="cards">
<article class="card">
<img src="../img/landscape.svg">
<h3>Милиционер спас котёнка</h3>
<div class="date">14 февраля 2019</div>
<p class="summary">Стриптизёр Алексей в форме милиционера шёл по вызову для поздравления одинокой девушки Оксаны, когда увидел плачущего мальчика… <a href="#">Читать далее</a>
</article>
<article class="card">
<img src="../img/landscape.svg">
<h3>Кроты на льду</h3>
<div class="date">12 февраля 2019</div>
<p class="summary">Так решил назвать свой дебютный короткометражный фильм Андрей Шмятушкин. Критики отзываются о картине весьма положительно… <a href="#">Читать далее</a>
</article>
<article class="card">
<img src="../img/landscape.svg">
<h3>iVibro X</h3>
<div class="date">12 февраля 2019</div>
<p class="summary">Компания DuneHills представили новую модель виброфона iVibro X. Главным нововведением этой модели стала система по распознаванию лица пользователя и автоматическая подстройка… <a href="#">Читать далее</a>
</article>
<article class="card">
<img src="../img/landscape.svg">
<h3>Очень старая новость</h3>
<div class="date">04 июля 2018</div>
<p class="summary">Серьёзно, это такая старая новость, что я и забыл о чём она, так что непонятно чего вы тут ожидали увидеть… <a href="#">Читать далее</a>
</article>
</div>
{{</slide>}}

{{<slide title="Страница событий">}}
<div class="cards">
<article class="card">
<img src="../img/landscape.svg">
<h3>Концерт Василия Незадвыгина</h3>
<div class="date">24 февраля 2019</div>
<p class="summary">Неподражаемый Василий Незадвыгин выступит с новой программой «Мне бы не задвинуть»… <a href="#">Читать далее</a>
</article>
<article class="card">
<img src="../img/landscape.svg">
<h3>Опера «На краю ионизатора»</h3>
<div class="date">25 февраля 2019</div>
<p class="summary">Переосмысление роли интернета вещей и возобновляемых источников питания в новой постановке театра роботов-пылесосов… <a href="#">Читать далее</a>
</article>
<article class="card">
<img src="../img/landscape.svg">
<h3>Последний день зимы</h3>
<div class="date">28 февраля 2019</div>
<p class="summary">На главной площади города состоится прощание с зимой. В программе будет синхронный танец средств по уборке снега, а также… <a href="#">Читать далее</a>
</article>
<article class="card">
<img src="../img/landscape.svg">
<h3>Выставка горшечных растений</h3>
<div class="date">04 июля 2019</div>
<p class="summary">Вы что серьёзно это читаете? Ладно, подойдите после доклада и скажите «я прочитал»… <a href="#">Читать далее</a>
</article>
</div>
{{</slide>}}

{{<slide title="Страница авторов">}}
<div class="cards">
<article class="card">
<img class="person" src="../img/person.svg">
<h3>Котейко Л.И.</h3>
<p class="summary">Людмилу с детства интересовали кошки. Но просто содержать кошку было мало, так что Людмила стала писать статьи про кошек. Кошки в каждый дом!
</article>
<article class="card">
<img class="person" src="../img/person.svg">
<h3>Репейников В.И.</h3>
<p class="summary">Василий — профессионал своего дела. Больше всего он любит журналистские расследования, бывает прицепится как репей…
</article>
<article class="card">
<img class="person" src="../img/person.svg">
<h3>Бастрыков Е.С.</h3>
<p class="summary">Евгений чуть было не стал графоманом, но после того как устроился в нашу газету стал выручать редакцию в те дни, когда новостей совсем нет.
</article>
<article class="card">
<img class="person" src="../img/person.svg">
<h3>Апостроф П.П.</h3>
<p class="summary">Пётр очень серьёзно относится к своей работе и оттачивает свои статьи до последней минуты, отдавая их редактору буквально перед отдачей в печать. Но в его статьях ещё ни разу не нашли ни единой ошибки!
</article>
</div>
{{</slide>}}

{{<slide title="Страница партнёров">}}
<div class="cards">
<article class="card">
<img class="partner" src="../img/logo.svg">
<h3>Лебеди и паравозы</h3>
</article>
<article class="card">
<img class="partner" src="../img/logo.svg">
<h3>Translit inc.</h3>
</article>
<article class="card">
<img class="partner" src="../img/logo.svg">
<h3>Банк «Покрытие»</h3>
</article>
<article class="card">
<img class="partner" src="../img/logo.svg">
<h3>Театр роботов-пылесосов</h3>
</article>
</div>
{{</slide>}}

{{<slide title="Новые требования">}}
- Авторов разместить по 5 в строке, потому как у них карточки поменьше.
- У новостей сделать синюю полоску сверху.
{{</slide>}}

{{<slide title="Добавим модификаторов">}}
```html
<div class="card-item card-item_wide card-item_shadowed
card-item_rulled card-item_with-footer card-item_hot
card-item_starred”>
```
{{</slide>}}

{{<slide id="troubles-2" title="Проблемы контейнеров" class="section black shadow"
    cover="../img/containers.jpg" cover-alt="Containers" cover-copy="Photo by Tim Easley on Unsplash"
/>}}

{{<slide title="Проблемы контейнеров">}}
- имена контейнеров должны быть уникальными;
- семантические контейнеры увеличивают дублирование кода;
- проблема чистого листа лишь усугубляется;
{{</slide>}}

{{<slide id="preprocessors" title="          Препроцессоры" class="section"
    cover="../img/fragile.jpg" cover-alt="Five stack of stone fragments" cover-copy="Photo by Ryan Stone on Unsplash"
/>}}

{{<slide title="Какие проблемы решаются">}}
- Неоднозначность решения;
- Глобальное пространство имён;
- Сложность селекторов и определение веса;
- ~~Отсутствие наследования~~ __mixin__;
- Влияние оформления контейнера на оформление содержимого;
- ~~Проблема чистого листа~~ __const__;
{{</slide>}}

{{<slide id="troubles-3" title="Проблемы препроцессоров" class="section black"
    cover="../img/blue_wall.jpg" cover-alt="Blue wall with chaos of wires" cover-copy="Photo by Khara Woods on Unsplash"
/>}}

{{<slide title="Проблемы препроцессоров">}}
- где заканчивается примесь и начинается класс наследника?
- имя примеси редко говорит обо всём, что она делает
- примесей может стать слишком много
- изменение примеси может привести к неожиданным эффектам
- переменные не решают проблемы чистого листа
{{</slide>}}

{{<slide id="stop-digging" title="Как перестать писать CSS?" class="section black shadow"
    cover="../img/lake.jpg" cover-alt="A men looks at the lake" cover-copy="Photo by Joshua Earle on Unsplash"
/>}}

{{<slide title="Утилитарные классы">}}
```html
<div class="p-2 my-1 d-f w-25">
    <p class="bg-success">
        ...
    </p>
</div>
```
{{</slide>}}

{{<slide title="Преимущества">}}
- однозначность решений;
- глобальное пространство имён больше не является проблемой;
- селекторы как и в БЭМ это только класс;
- нет проблемы чистого листа;
- не нужно писать CSS;
- объём CSS не увеличивается;
- классов мало и их поведение очевидно;
{{</slide>}}

{{<slide title="Компоненты<br>Utility-first" shout="true" />}}

{{<slide id="next" title="Что дальше?" class="section black"
    cover="../img/road.jpg" cover-alt="Long road through desert" cover-copy="Photo by salvatore ventura on Unsplash"
/>}}

{{<slide title="Что дальше?">}}
- SMACSS;
- стили без классов (normalize.css);
- сетка (grids / flexbox);
- тема (custom-properties / препроцессоры с их переменными);
- документация (KSS);
{{</slide>}}

{{<slide title="Почитать">}}
- https://frontstuff.io/in-defense-of-utility-first-css
- https://adamwathan.me/css-utility-classes-and-separation-of-concerns/
- https://css-irl.info/a-year-of-utility-classes/
{{</slide>}}

{{<slide id="questions" title="Вопросы?" shout="true" />}}

{{<slide id="thanks" title="Спасибо за внимание!" class="section" />}}
