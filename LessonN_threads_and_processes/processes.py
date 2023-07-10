"""
ПРОЦЕСС - это абстракция Операционной системы, которая, в общем случае, представляет собой запущенную программу
вместе с необходимыми программе областями памяти и окружением (Runtime), необходимым для выполнения этой программы.
Процесс, в котором выполняется Пайтон-код, содержит также Интерпретатор для выполнения этого кода

ПОТОК - тоже абстрация ОС, явялется неотъемлемой частью процесса: Поток не может существовать вне Процесса,
также как и любой Процесс имеет как минимум 1 Поток (Main Thread)

Выполнение кода программы происходит как раз внутри Потока(ов).
Существуют следующие возможные комбинации:
- 1 Процесс с 1 Потоком (классический скрипт или программа на Пайтоне/любой другом языке, запущенная в операционной системе)
- 1 Процесс с N Потоков (многопоточная программа на Пайтоне/любом другом языке)
- N Процессов, по 1 Потоку в каждом (многопроцессная программа на Пайтоне/любом другом языке)
- N Процессов, по N Потоков в каждом (более сложная форма примера выше)

ВИРТУАЛЬНАЯ ПАМЯТЬ:
- Потоки одного Процесса имеют доступ к ОБЩЕЙ ОБЛАСТИ ВИРТУАЛЬНОЙ ПАМЯТИ, которая принадлежит всему Процессу:
  эта область называетcя HEAP (Куча)
- Каждый Поток имеет свою собственную область памяти, называемую STACK
 (ПРИМЕЧАНИЕ: да-да, это тот самый Стэк, он же "Стэк вызовов", который вы видите слева в Дебаггере)

* Если не уходить в дебри того, как устроена работа с виртуальной памятью конкретно в Пайтоне, то:
-- В Пайтоне ВСЕ ОБЪЕКТЫ хранятся в КУЧЕ
-- Локальные переменные / аргументы функций, которые являют собой ссылки на реальные Объекты, хранятся на СТЭКЕ


Суть наличия Процессов и Потоков в ОС - за счет этих Абстракций реализуется так называемая Многозадачность (так же говорят: Конкурентность).
- Многозадачность: это когда множество запущенных программ работают как бы по-очереди, но в рамках коротких интервалов, c очень быстрым переключением между собой
(чтобы понаблюдать за тем, как переключаются задачи - можете использовать утилиту htop в Линуксе или Диспетчер задач в Windows)
- За счет Многозадачности, даже в Одноядерных системах, Пользователь может редактировать Документ в Word и в это же время слушать Музыку в аудио-плейере
- В Многоядерных системах (любой современный СPU - многоядерный) все еще лучше: Операционная система распределяет ВСЕ запущенные Программы
 (то есть Процессы и Потоки внутри этих процессов) по разным ядрам CPU - за счет этого разные части разных программ могут выполняться
 параллельно друг другу на разных ядрах, в рамках же одного ядра - задачи выполняются "конкурентно" (см. пункт Многозадачность)

Особенность языка Пайтон:
- в Пайтоне с давних времен есть такая штука как GIL - GLOBAL INTERPRETER LOCK.
Если простыми словами, то GIL не позволяет выполняться двум и более различных Потокам параллельно, на разных ядрах CPU.
Естественно, это касается только тех Потоков, которые порождаются из Пайтон-кода и которые выполняют Пайтон-код.

Поэтому, использование многопоточности в Пайтоне - отдельная проблема. Существуют ситуации, когда использование N Потоков
сделает ваш код еще МЕДЛЕННЕЕ, чем если бы он работал в одном Потоке! Однако, в иных случаях использования, зная нюансы того,
как работает GIL, вы можете ускорить вашу программу используя Потоки.

Использование Процессов в Python - есть обходной путь для того, чтобы добиться реальной параллелизма при выполнения Пайтон-кода:
каждый порожденный Процесс имеет свою личную копию Интерпетатора, который в свою очередь имеет свой личный GIL
Однако, многопроцессный подход имеет и ряд минусов:
- Порождение нового Процесса всегда более "дорого" чем порождение Потока (особенно в Windows)
- Разные процессы, даже если они запущенны на одном ПК, имею изолированные друг от друга области Виртуальной памяти
 (в отличие от Потоков, которые "шарят" общую память Процесса, внутри которого они работают)
- Чтобы получть данные (любой Питоновский объект) из одногго Процесса в другом Процессе, эти данные нужно сериализовать

Все вышеописанное - это определенное затраченное время вашей программмы, так называемый Overhead, поэтому нельзя думать,
что использованеи Многопроцесности само по себе дает 100-й Профит :)
"""