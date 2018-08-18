---
title: Property-based testing
description: Тестируй не вход и выход, а свойства
date: 2018-06-12T16:09:44Z
categories:
- develop
tags:
- testing
- go
cover:
  image: /post/2018/06/img/properties.jpg
  caption: “The symmetrical apartment units with orange doors in Osaka“ by Tim Easley on Unsplash
  style: normal
toc: true
emoji: true
---

Сегодня хотелось бы рассмотреть такой подход к тестированию как property-based тесты, или, по-русски говоря, тесты основанные на свойствах. Раньше, когда я слышал это название, то думал, что это способы тестирования свойств классов, в смысле [property](https://docs.python.org/3/library/functions.html?property). А при учёте того, что я [слышал](https://devzen.ru/episode-0049/) [об этом](https://devzen.ru/episode-0099/) [исключительно](https://devzen.ru/episode-0134/) [в подкасте](https://devzen.ru/episode-0150/) [DevZen](https://devzen.ru/episode-0166/), где за этими словами следовали слова: haskell, scala и erlang, то не особо вдавался в подробности. Однако, на [выпуске](https://devzen.ru/episode-0190/) про [TLA+](http://lamport.azurewebsites.net/tla/tla.html) эта тема меня всё же зацепила, так что я пошёл гуглить и читать. И вот теперь окончательно дозрев, готов поделиться тем, что сумел найти и понять.

## Простой пример

Итак, первое, что нужно понимать, property-based тесты используют подход чёрного ящика. При этом они запускаются в достаточно больших количествах и должны быть воспроизводимы, так что будет хорошо тестировать чистую функцию. Таким образом самое подходящее место для их применения это модульные тесты.
Для начала соорудим наш чёрный ящик. Пусть это будет банальный [FizzBuzz](https://habr.com/post/278867/)
```go
package fizzbuzz

import (
	"strconv"
	"strings"
)

// FizzBuzz return "Fizz" for 3*n number, "Buzz" for 5*n number,
// "FizzBuzz" for 15*n number and number as string otherwise.
func FizzBuzz(n int) string {
	res := strings.Builder{}
	if n%3 == 0 {
		res.WriteString("Fizz")
	}
	if n%5 == 0 {
		res.WriteString("Buzz")
	}
	if res.Len() == 0 {
		res.WriteString(strconv.Itoa(n))
	}

	return res.String()
}
```

Теперь попробуем его потестировать. Собственно первое, что приходит на ум, это использовать [Table-driven tests](https://www.youtube.com/watch?v=ndmB0bj7eyw&t=2497s), например:
```go
package fizzbuzz

import (
	"strconv"
	"testing"
)

func TestFizzBuzzCases(t *testing.T) {
	cases := []struct {
		input  int
		output string
	}{
		{
			input:  2,
			output: "2",
		},
		{
			input:  12,
			output: "Fizz",
		},
		{
			input:  25,
			output: "Buzz",
		},
		{
			input:  60,
			output: "FizzBuzz",
		},
	}

	for _, c := range cases {
		t.Run(strconv.Itoa(c.input), func(t *testing.T) {
			t.Parallel()

			res := FizzBuzz(c.input)
			if res != c.output {
				t.Errorf("expected %q but got %q", c.output, res)
			}
		})
	}
}
```

Но очевидно, что подобный тест, это некоторое лукавство, ведь по факту мы не проверили правильность поведения нашего кода, мы просто сопоставили 4 пары входов и выходов. То есть этот тест лишь показывает, что наш код корректно обрабатывает 4 случая. Что будет с другими входными данными, мы предсказать не можем. Вот тут-то к нам на помощь и приходят тесты, основанные на свойствах. На свойствах нашего чёрного ящика. Давайте попробуем сформулировать эти свойства:
1. Если на вход нашей коробке подать любое число, кратное 3, то ответ должен начинаться со слова **Fizz**;
2. Если на вход подать число, кратное 5, то ответ должен заканчиваться на слово **Buzz**;
3. Если на вход подать число не кратное ни 3, ни 5, то коробка должна вернуть это же число в виде строки;

«Но ведь это же и есть условия задачи!» - воскликните вы и будете правы. По сути мы хотим проверить то, что наша коробочка удовлетворяет поставленным перед ней условиям. По сути, формализация этих требований в код и будет тестом, основанным на свойствах, правда для того, чтобы правильно этот тест запустить, надо будет перебрать все возможные входные данные (в нашем случае это int64, то есть каких-то 19 с половиной квинтиллионов) и для каждого из них проверить выполнение перечисленных свойств. С одной стороны это будет вполне исчерпывающее доказательство того, что чёрный ящик работает как надо, с другой - а не слишком ли высокая цена за доказательство? Конечно, компьютеры очень мощны, чтобы перемолотить это за каких-нибудь 20 минут, но что делать с чёрными ящиками от нескольких переменных?

Выход был предложен создателями библиотеки для тестирования кода на Haskell: [QuickCheck](https://begriffs.com/posts/2017-01-14-design-use-quickcheck.html). Можно запускать не всё, но много. Случайным образом. То есть, если рандомизированно выбирать входные параметры и проверять свойства, да к тому же сделать это достаточно много раз, то тоже будет хорошо. Этот подход снискал своих поклонников да так, что эта библиотека была портирована практически на все живые языки программирования. Например, в том же go [порт входит в стандартную библиотеку тестирования](https://godoc.org/testing/quick). Однако, в отличии от всего остального языка этот порт уж слишком магический и неочевидный, поэтому воспользуемся более многословной библиотекой: https://github.com/leanovate/gopter
```go
package fizzbuzz

import (
	"math"
	"strconv"
	"strings"
	"testing"

	"github.com/leanovate/gopter"
	"github.com/leanovate/gopter/gen"
	"github.com/leanovate/gopter/prop"
)

func TestFizzBuzzProperties(t *testing.T) {
	properties := gopter.NewProperties(nil)

	properties.Property("Start with Fizz for all multiples of 3", prop.ForAll(
		func(i int) bool {
			result := FizzBuzz(i * 3)
			return strings.HasPrefix(result, "Fizz")
		},
		gen.IntRange(1, math.MaxInt32/3),
	))

	properties.Property("Ends with Buzz for all multiples of 5", prop.ForAll(
		func(i int) bool {
			result := FizzBuzz(i * 5)
			return strings.HasSuffix(result, "Buzz")
		},
		gen.IntRange(1, math.MaxInt32/5),
	))

	properties.Property("Int as string for all non-divisible by 3 or 5", prop.ForAll(
		func(number int) bool {
			result := FizzBuzz(number)
			parsed, err := strconv.ParseInt(result, 10, 64)
			return err == nil && parsed == int64(number)
		},
		gen.IntRange(1, math.MaxInt32).SuchThat(func(v interface{}) bool {
			return v.(int)%3 != 0 && v.(int)%5 != 0
		}),
	))

	properties.TestingRun(t)
}
```

Для каждого свойства будет запущено 100 случайных тестов и, если свойство не выполнится, тест будет провален.

## Генератор

Но это, конечно, детский пример, давайте рассмотрим что-то посложнее, что-то, что будет принимать на вход не примитивные типы. Например, функция выделения минимального подпокрытия.

> На вход подаётся семейство множеств, из него надо выделить минимальное подсемейство такое, что объединение множеств оригинального семейства совпадало с объединением множеств результата.

Эта задача относится к классу NP-полных задач и решается чаще всего методом линейного программирования, либо можно решить задачу приближённо, используя жадный алгоритм. Поэтому само решение я не буду приводить, потому как пост совсем не о том.

Итак, у нас есть чёрный ящик, который на вход принимает семейство множеств и на выходе отдаёт семейство множеств. Давайте начнём со свойств, которые мы хотим проверить:
1. Результат должен покрывать то же множество, что и исходное семейство;
2. Мощность результата не должна превышать мощность входного семейства;
3. Результат должен быть подсемейством входного семейства, то есть каждое множество результата должно содержаться во входном семействе;

Можно придумать ещё свойства, но проблема не в этом. Проблема в том, что входным параметром является сложная структура. Как же нам выбрать случайным образом 100 покрытий? Для этого надо написать собственный генератор. По сути генератор это функция, которая по заданным параметрам генерирует некоторую случайную структуру. Среди параметров передаётся генератор случайных чисел, инициированный специальным образом, так что используя этот генератор мы можем получить случайную, но воспроизводимую структуру данных. Что ж, давайте напишем генератор:
```go
package coverage

import (
	"github.com/leanovate/gopter"
)

func CoverageGen(mod uint32, count uint32) gopter.Gen {
	return func(params *gopter.GenParameters) *gopter.GenResult {
		coverage := make([][]uint32, count)

		for i := range coverage {
			n := int(uint64(mod/3) + params.NextUint64()%uint64(mod/3))
			set := make(map[uint32]struct{}, n)
			coverage[i] = make([]uint32, 0, n)
			for len(set) < n {
				x := uint32(params.NextUint64() % uint64(mod))
				if _, ok := set[x]; !ok {
					coverage[i] = append(coverage[i], x)
					set[x] = struct{}{}
				}
			}
		}

		return gopter.NewGenResult(coverage, CoverageShrinker)
	}
}

type coverageShrink struct {
	coverage [][]uint32
}

func CoverageShrinker(coverage interface{}) gopter.Shrink {

	shrink := coverageShrink{coverage.([][]uint32)}

	return shrink.Next
}

func (cs *coverageShrink) Next() (interface{}, bool) {
	cs.coverage = cs.coverage[:len(cs.coverage)/2]
	if len(cs.coverage) == 0 {

		return nil, false
	}

	return cs.coverage, true
}
```

Для удобства параметризуем наш генератор модулем кольца, ограничевающим универсальное множество, а также числом множеств генерируемого семейства.

Всё бы ничего, но разбираться в том что пошло не так в случае покрытия, состоящего из сотен, а то и тысяч множеств, занятие не сильно воодушевляющее, так что на помощь нам приходит механизм сужения входных данных, так называемый shrinking. Если на каком-то сгенерированном наборе мы получим невыполнение свойства, то фреймворк попытается с помощью переданного shrinker'а уменьшить входные данные до тех пор, пока ошибка повторяется. Для простоты я написал шринкер, который просто обрезает множества в конце оригинального списка. Итоговый тест выглядит следующим образом:
```go
package coverage

import (
	"bytes"
	"encoding/binary"
	"testing"

	"github.com/leanovate/gopter"
	"github.com/leanovate/gopter/prop"
)

func TestCoverageProperties(t *testing.T) {
	properties := gopter.NewProperties(nil)

	properties.Property("Output is a coverage", prop.ForAll(
		func(coverage [][]uint32) bool {
			universe := universeOfCoverage(coverage)
			result := universeOfCoverage(GetMinimalSubcoverage(coverage))

			for item := range universe {
				if _, ok := result[item]; !ok {

					return false
				}
			}

			return true
		},
		CoverageGen(20, 20),
	))

	properties.Property("Length of output less or equal length of input", prop.ForAll(
		func(coverage [][]uint32) bool {
			result := GetMinimalSubcoverage(coverage)

			return len(coverage) >= len(result)
		},
		CoverageGen(200, 200),
	))

	properties.Property("Every output set must be in input", prop.ForAll(
		func(coverage [][]uint32) bool {
			coverageAsBytes := coverageToBytes(coverage)
			result := GetMinimalSubcoverage(coverage)

			for _, set := range result {
				if !isInCoverage(set, coverageAsBytes) {
					t.Log(set)

					return false
				}
			}

			return true
		},
		CoverageGen(200, 200),
	))

	properties.TestingRun(t)
}

func universeOfCoverage(coverage [][]uint32) map[uint32]struct{} {
	universe := map[uint32]struct{}{}
	for _, set := range coverage {
		for _, item := range set {
			universe[item] = struct{}{}
		}
	}

	return universe
}

func coverageToBytes(coverage [][]uint32) [][]byte {
	res := make([][]byte, len(coverage))
	for i := range res {
		res[i] = setToBytes(coverage[i])
	}

	return res
}

func isInCoverage(set []uint32, coverageAsBytes [][]byte) bool {
	setAsBytes := setToBytes(set)

	for _, item := range coverageAsBytes {
		if bytes.Equal(setAsBytes, item) {

			return true
		}
	}

	return false
}

func setToBytes(set []uint32) []byte {
	buf := bytes.Buffer{}
	binary.Write(&buf, binary.LittleEndian, set)

	return buf.Bytes()
}

func CoverageGen(mod uint32, count uint32) gopter.Gen {
	return func(params *gopter.GenParameters) *gopter.GenResult {
		coverage := make([][]uint32, count)

		for i := range coverage {
			n := int(uint64(mod/3) + params.NextUint64()%uint64(mod/3))
			set := make(map[uint32]struct{}, n)
			coverage[i] = make([]uint32, 0, n)
			for len(set) < n {
				x := uint32(params.NextUint64() % uint64(mod))
				if _, ok := set[x]; !ok {
					coverage[i] = append(coverage[i], x)
					set[x] = struct{}{}
				}
			}
		}

		return gopter.NewGenResult(coverage, CoverageShrinker)
	}
}

type coverageShrink struct {
	coverage [][]uint32
}

func CoverageShrinker(coverage interface{}) gopter.Shrink {

	shrink := coverageShrink{coverage.([][]uint32)}

	return shrink.Next
}

func (cs *coverageShrink) Next() (interface{}, bool) {
	cs.coverage = cs.coverage[:len(cs.coverage)/2]
	if len(cs.coverage) == 0 {

		return nil, false
	}

	return cs.coverage, true
}
```

Вот собственно и вся магия.

## Что почитать (посмотреть)

- Очень крутой доклад, где на пальцах объясняется весь подход: https://www.youtube.com/watch?v=shngiiBfD80&t=446s
- Отличная статья, откуда я спёр пример про минимальное подпокрытие: http://blog.jessitron.com/2013/04/property-based-testing-what-is-it.html
- Оригинальная статья про рандомизированные тесты на haskell QuickCheck: http://www.eecs.northwestern.edu/~robby/courses/395-495-2009-fall/quick.pdf
- Хорошее описание методологий тестирования от ScalaCheck: http://www.scalatest.org/user_guide/property_based_testing
