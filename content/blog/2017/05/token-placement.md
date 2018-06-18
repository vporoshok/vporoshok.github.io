---
title: Ещё раз о безопасности или где хранить токен
description: CSRF атаки и способы защиты
date: 2017-05-28T17:33:45Z
categories:
- develop
tags:
- CSRF
- PHP
- security
- web
cover:
  image: /blog/2017/05/img/pink_door.jpg
  caption: '"Pink sweet jail" by [@pinksweet](https://busy.org/@pinksweet)'
  style: normal
toc: true
---

В очередной раз встал вопрос о том где и как хранить токен авторизации. Первое что приходит в голову это cookie. Итак, давайте сделаем простенький сайт со странице авторизации и использованием cookie для определения пользователя, а затем попробуем его поломать. Использовать мы будем [CSRF](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29) атаку. Об этих атаках написано уже немало статей, небольшой список будет в конце. В данном посте хочется добавить практики в эти объяснения на пальцах.
Для удобства используем репозиторий с тегами эволюции проекта https://github.com/vporoshok/csrf-test. По ходу описания будут встречаться ссылки вида [#init](https://github.com/vporoshok/csrf-test/tree/init), содержащие в себе имя тега и ссылку на его слепок. Вы можете склонировать себе репозиторий и переключаться между тегами:
```sh
$ git clone git@github.com:vporoshok/csrf-test.git
$ git checkout init
```

## Начало

Начнём с простейшего сайта на php состоящего из двух страниц [#init](https://github.com/vporoshok/csrf-test/tree/init):
```php
<?php
    session_start();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $_SESSION['email'] = $_POST['email'];
        header('Location: /form.php');
        exit();
    }
?>
<form method="post">
    <input name="email">
    <button>Login</button>
</form>
```

За исключением отсутствия проверки пароля это вполне обычная ситуация для сайтов, когда мы просто записываем введённый email в сессию пользователя. Сессия же связывается с браузером с помощью cookie.
```php
<?php
    session_start();
    $sender = $_SESSION['email'];
    if (strlen($sender) === 0) {
        http_response_code(401);
        echo('Unauthorized');
        exit();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $message = $_POST['message'];
        $receiver = $_POST['receiver'];
        echo("Send $message to $receiver");
    }
?>
<p>Hello, <?php echo($sender) ?>!</p>
<form method="post">
    <input name="message" placeholder="message"><br>
    <input name="receiver" placeholder="receiver"><br>
    <button>Send</button>
</form>
```

Здесь мы проверяем залогинен ли пользователь (то есть есть ли в связанной с ним сессии email), и, если есть, то предоставляем ему формочку для отправки сообщения другому пользователю.
Теперь, что бы запустить проект используем docker-compose со следующим конфигом:
```yaml
version: '2'

services:
  my:
     image: php:7.0-apache
     volumes:
       - ./my:/var/www/html
     ports:
       - "4000:80"
```

Конечно, первые два файла кладутся в папку my, которая и подключается к контейнеру. Стартуем приложение через
```sh
$ docker-compose up
```
открываем в браузере http://localhost:4000/form.php получаем ошибку, заходим на [login](http://localhost:4000/login.php), вводим почту, всё. Теперь наш браузер авторизован на сайте и мы можем пользоваться формой.

## Зловред

Добавим в наш проект зловредный сайт, который разместим в папке bad и на другом домене: localhost:4001 [#bad](https://github.com/vporoshok/csrf-test/tree/bad). Для CSRF атаки нам не потребуется серверная часть, создадим простую html-страничку:
```html
<form id="form" method="post" action="http://localhost:4000/form.php">
    <input name="message" value="some spam"/>
    <input name="receiver" value="bob@mail.com"/>
</form>
<script>
    var form = document.getElementById('form');
    form.submit();
</script>
```

Вот такой примитивной страничкой мы можем рассылать спам от имени несчастного пользователя. Добавим в docker-compose описание зловредного сайта:
```yaml
  bad:
     image: nginx
     volumes:
       - ./bad:/usr/share/nginx/html
     ports:
       - "4001:80"
```

И снова выполним `docker-compose up`. Теперь, если вы залогинены на сайте http://localhost:4000/ и зайдёте на сайт http://localhost:4001/, то от вашего имени будет выполнена отправка спама ни в чём неповинному Бобу. Конечно, такую html-страницу лучше всего поместить в скрытый iframe, чтобы вы ничего не заподозрили.

## CSRF-токен

Так как же защититься от такой атаки? Может быть не хранить авторизационный токен в cookie? Нет, мы не ищем лёгких путей. Используем CSRF-токены [#token](https://github.com/vporoshok/csrf-test/tree/token)! Есть несколько вариантов работы с ними, мы будем использовать следующий:
- При запросе к странице с формой будем генерировать новый токен, состоящий из времени запроса, email из сессии и подписи с помощью секрета, который известен только серверу. Получившийся токен мы кладём в скрытое поле формы.
- При получении данных формы мы валидируем токен и, если он не подходит по формату, привязан к другому пользователю или неверно подписан, то выдаём ошибку. Если прошло больше 10 минут с момента формирования токена, просим отправить повторно, сохранив данные формы.

```php
<?php
    const SECRET = "SOME SECRET";
    session_start();
    $sender = $_SESSION['email'];
    if (strlen($sender) === 0) {
        http_response_code(401);
        echo('Unauthorized');
        exit();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $token = $_POST['csrf_token'];
        $tokenSplit = explode(':', $token);
        if (count($tokenSplit) !== 3 || $tokenSplit[1] !== $sender) {
            http_response_code(400);
            echo('Bad CSRF token');
            exit();
        }
        $token = sprintf('%s:%s:', $tokenSplit[0], $tokenSplit[1]);
        $hash = sha1($token . SECRET);
        if ($hash !== $tokenSplit[2]) {
            http_response_code(400);
            echo('Bad CSRF token');
            exit();
        }
        if (time() - intval($tokenSplit[0]) > 600) {
            echo('CSRF token expired. Please try again');
        } else {
            $message = $_POST['message'];
            $receiver = $_POST['receiver'];
            echo("Send $message to $receiver");
            $message = '';
            $receiver = '';
        }
    }
    $token = sprintf('%d:%s:', time(), $sender);
    $token .= sha1($token . SECRET);
?>
<p>Hello, <?php echo($sender) ?>!</p>
<form method="post">
    <input type="hidden" name="csrf_token" value="<?php echo($token) ?>">
    <input name="message" placeholder="message" value="<?php echo($message) ?>"><br>
    <input name="receiver" placeholder="receiver" value="<?php echo($receiver) ?>"><br>
    <button>Send</button>
</form>
```

## CORS заголовки

Что же теперь делать злоумышленнику? Попытаться как-то украсть CSRF-токен. Например, следующим образом [#stealToken](https://github.com/vporoshok/csrf-test/tree/stealToken):
```html
<form id="form" method="post" action="http://localhost:4000/form.php">
    <input name="message" value="some spam"/>
    <input name="receiver" value="bob@mail.com"/>
</form>
<script>
    var req = new XMLHttpRequest();
    req.open('GET', 'http://localhost:4000/form.php');
    req.addEventListener('readystatechange', e => {
        if (req.readyState !== req.DONE) {
            return;
        }
        var div = document.createElement('div');
        div.innerHTML = req.responseText;
        var input = div.querySelector('input[name="csrf_token"]');
        if (input == null) {
            return;
        }
        var form = document.getElementById('form');
        form.appendChild(input);
        form.submit();
    });
    req.send();
</script>
```

Но такой запрос не выполнится, потому что браузер сделав запрос проверит в нём наличие заголовков [Access-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS). И если сайту злоумышленника доступ не разрешён, то ответ не вернётся в javascript. Более того, если мы посмотрим на логи нашего сервера, то увидим следующее:
```log
my_1   | 172.19.0.1 - - [28/May...+0000] "GET /form.php HTTP/1.1" 401 426 "http://localhost:4001/" "Mozilla/.../603.1.30"
```
Запрос поступил, но вернул 401 ошибку. Погодите, но ведь в браузере есть связанная с сессией cookie! Для того чтобы браузер передал ещё и cookie, необходимо добавить следующую строчку в скрипт:
```js
req.open('GET', 'http://localhost:4000/form.php');
req.withCredentials = true;
req.addEventListener('readystatechange', e => {...
```
Но к таким запросам предъявляется ещё больше требований по заголовкам. Итак, наш сайт кажется вполне защищённым от CSRF-атак. Но подождите, скажете вы, ведь если у злоумышленника не получилось даже запросить страницу с сайта по cookie, а у нас, например, очень умный фронтенд, а сервер предоставляет JSON REST API, так может нам эти свистопляски с CSRF токенами не нужны?

## Проверка данных вместо заголовков

Действительно, ведь мы защищаемся от атаки обычной формой, которая по стандарту не может передавать json. Что ж давайте попробуем: уберём проверку по CSRF-токену, а данные будем принимать исключительно в виде [#json](https://github.com/vporoshok/csrf-test/tree/json).
```php
<!-- login.php -->
<?php
    session_start();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $dataRaw = file_get_contents('php://input');
        $data = json_decode($dataRaw, true);
        var_dump($data);
        $_SESSION['email'] = $data['email'];
        header('Location: /form.php');
        exit();
    }
?>
<form name="login">
    <input name="email">
    <button>Login</button>
</form>
<script>
    var form = document.forms.namedItem('login');
    form.addEventListener('submit', e => {
        e.preventDefault();
        var email = form.querySelector('input[name="email"]');
        var data = {
            email: email.value
        };
        var req = new XMLHttpRequest();
        req.open('POST', '/login.php');
        req.setRequestHeader('Content-Type', 'application/json');
        req.addEventListener('readystatechange', e => {
            if (req.readyState !== req.DONE) {
                return;
            }
            if (req.status === 200) {
                window.location = '/form.php';
            }
        });
        req.send(JSON.stringify(data));
    });
</script>
```
```php
<!-- form.php -->
<?php
    session_start();
    $sender = $_SESSION['email'];
    if (strlen($sender) === 0) {
        http_response_code(401);
        echo('Unauthorized');
        exit();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $dataRaw = file_get_contents('php://input');
        $data = json_decode($dataRaw, true);
        $message = $data['message'];
        $receiver = $data['receiver'];
        echo("Send $message to $receiver");
    }
?>
<p id="state"></p>
<form name="send">
    <input name="message" placeholder="message"><br>
    <input name="receiver" placeholder="receiver"><br>
    <button>Send</button>
</form>
<script>
    var form = document.forms.namedItem('send');
    var state = document.getElementById('state');
    form.addEventListener('submit', e => {
        e.preventDefault();
        var message = form.querySelector('input[name="message"]');
        var receiver = form.querySelector('input[name="receiver"]');
        var data = {
            message: message.value,
            receiver: receiver.value
        };
        var req = new XMLHttpRequest();
        req.open('POST', '/form.php');
        req.setRequestHeader('Content-Type', 'application/json');
        req.addEventListener('readystatechange', e => {
            if (req.readyState !== req.DONE) {
                return;
            }
            if (req.status === 200) {
                state.innerHTML = `Send ${message.value} to ${receiver.value}`;
                message.value = '';
                receiver.value = '';
            }
        });
        req.send(JSON.stringify(data));
    });
</script>
```

## Опасность не уходит

Усложнили клиент, хотя если всё это обильно полить каким-нибудь фреймворком, то получится вполне хорошо. Однако! Есть тут стандарт https://www.w3.org/TR/html-json-forms/, по которому надежда на то, что json исключительно прерогатива xhr может не оправдаться. Он, конечно, отменён, но кто может ручаться, что завтра его не вернут? Более того, если не проверять Content-Type, то можно нарваться на такую ситуацию: http://pentestmonkey.net/blog/csrf-xml-post-request. Модифицируем нашего зловреда [#textPlain](https://github.com/vporoshok/csrf-test/tree/textPlain):
```html
<form id="form" method="post" action="http://localhost:4000/form.php" enctype="text/plain">
    <input name='{"equals":"' value='", "message": "SPAM", "receiver": "bob@mail.com"}'>
</form>
<script>
    var form = document.getElementById('form');
    form.submit();
</script>
```

Такие дела. Есть способы от такого защититься такие, как, например, всегда проверять Content-Type, требовать наличия заголовка X-Requested-With или X-CSRF-Token. Так или иначе все эти способы сводятся к тому, чтобы убедиться, что запрос сделан именно через xhr, а не обычной формой.
Давайте теперь посмотрим с другой стороны. К нашему api вполне вероятно будет обращаться не только наш фронтенд, но, например, скрипты или вы сами через консоль. И вот здесь таскание cookie выглядит уже совсем малопривлекательным. Есть, конечно, такие инструменты как https://httpie.org/ с сессиями, но почему бы не передавать авторизационный токен явно в заголовке Authorization?

## Выводы
- если у вас тонкий клиент, тогда использование cookie и защита её с помощью csrf токена просто необходима;
- если у вас толстый клиент, а серверная часть предоставляет исключительно JSON REST API, не стоит усложнять себе жизнь вознёй с cookie. Отдавайте авторизационный токен явно в ответе сервера, на клиенте храните его в localStorage или sessionStorage, и при каждом запросе устанавливайте заголовок Authorization с этим токеном.

## Полезные ссылки
- Отличная статья, не теряющая своей актуальности. Рассматривает три типа уязвимостей: MITM, CSRF и XSS. Продвигает OAuth (en) http://sitr.us/2011/08/26/cookies-are-bad-for-you.html
- В статье рассматриваются некоторые способы защиты от CSRF атак (ru) https://habrahabr.ru/post/318748/
- Ещё один разбор применения токенов (ru) https://learn.javascript.ru/csrf
