flask-skeleton
==============

每开始一个Flask项目总是要重复做一些代码结构上的规划和写一些相同的代码，
flask-skeleton的目的是想把这些重复的事情都先统一做成脚手架，
在以后的API服务开发过程中只需clone下来就可以直接开始写业务代码。



## 运行

建议使用virtualenv创建虚拟环境。

    pip install -r requirements.txt
    python apiserver.py

## Demo

demo示例展示MySQL操作和异步执行任务，查看demo示例请先确认`settings.py`中数据库配置`MYSQL_URL`是你当前环境的配置，
导入demo示例的sql文件`v0.0.1.sql`后即可调用接口。

**增**

    curl -X POST \
      http://localhost:5000/demo/records \
      -H 'content-type: application/json' \
      -d '{
	        "caller": "demo",
	        "notify_engine":"tof",
	        "notify_method": "send_email",
	        "send_to": ["axiaoxin"],
	        "title": "hello",
	        "content": "this is content."
        }'

**查**

    curl -X GET \
      'http://localhost:5000/demo/records?order_by=created_at&order_type=asc'

**改**

    curl -X PUT \
      http://localhost:5000/demo/records/1 \
      -H 'content-type: application/json' \
      -d '{
    	"caller": "demo",
    	"notify_engine":"tof",
    	"notify_method": "send_email",
    	"send_to": ["ashinchen"],
    	"title": "i am title",
    	"content": "this is content too."
    }'

**删**

    curl -X DELETE \
      http://localhost:5000/demo/records/1


**异步任务示例**

    curl -X POST \
        'http://localhost:5000/demo/entry'
        -H 'content-type:application/json'
        -d '{
            "caller": "demo",
            "notify_engine":"tof",
            "notify_method": "send_email",
            "send_to": ["ashinchen"],
            "title": "i am title",
            "content":"this is content."
        }'


**修改配置**

默认会使用`settings.py`中的配置，新增配置按照[decouple](https://github.com/henriquebastos/python-decouple)写法。
修改已有的默认配置不必修改代码，在`app`根目录创建一个`.env`文件，参考.env.example写上修改后的配置即可。

**装饰器**

在demo的`routes.py`中会为`handlers.py`中的函数注册装饰器，这些装饰器不是必须的，
但是在使用时需要注意其注册顺序，按列表顺序注册，先注册的先执行。

使用`register_decorators_on_module_funcs`方法可以自动为一个模块文件中的方法注册装饰器

`pw_auto_manage_connect`: 确保在使用peewee时都先connect，最后close。如果想查看实际执行的sql可以修改`settings.py`中的`LOG_PEEWEE_SQL=True`

`cached`: 根据settings中的配置缓存GET请求的结果，如果不想使用自动缓存功能可以修改`settings.py`中的`CACHED_CALL=False`
`log_func_call`: 记录发生调用的函数名、参数、执行时间，如果不想记录到日志可以修改`settings.py`中的`LOG_FUNC_CALL=False`

cached装饰器在`settings.py`中的`CACHED_CALL=True`且被装饰的函数的执行时间大于`CACHED_OVER_EXEC_MILLISECONDS`毫秒时，
会缓存GET请求返回的结果，下次同样的GET请求到来时使用缓存返回结果，缓存过期时间为`CACHED_EXPIRE_SECONDS`秒。

**日志**

日志内容会按日志级别分开保存到不同的文件，你可以在`settings.py`中修改`LOG_PATH`来改变日志文件存放的位置。
日志文件以`SERVICE_NAME`-日志级别命名。

需要记录日志时，使用`utils.log`中对应的方法即可，好处是如果你配置了`SENTRY_DSN`在warning级别以上的日志会被自动被sentry捕获。

**返回JSON命名风格**

如果你的API需要统一JSON字段的命名风格，可以修改`settings.py`中的`JSON_KEYCASE`来动态改变。

默认支持的命名风格有：`camelcase`, `capitalcase`, `constcase`, `lowercase`, `pascalcase`, `pathcase`, `sentencecase`, `snakecase`, `spinalcase`, `titlecase`, `trimcase`, `uppercase`, `alphanumcase`

    camelcase('foo_bar_baz') # => "fooBarBaz"
    camelcase('FooBarBaz') # => "fooBarBaz"
    capitalcase('foo_bar_baz') # => "Foo_bar_baz"
    capitalcase('FooBarBaz') # => "FooBarBaz"
    constcase('foo_bar_baz') # => "FOO_BAR_BAZ"
    constcase('FooBarBaz') # => "_FOO_BAR_BAZ"
    lowercase('foo_bar_baz') # => "foo_bar_baz"
    lowercase('FooBarBaz') # => "foobarbaz"
    pascalcase('foo_bar_baz') # => "FooBarBaz"
    pascalcase('FooBarBaz') # => "FooBarBaz"
    pathcase('foo_bar_baz') # => "foo/bar/baz"
    pathcase('FooBarBaz') # => "/foo/bar/baz"
    sentencecase('foo_bar_baz') # => "Foo bar baz"
    sentencecase('FooBarBaz') # => "Foo bar baz"
    snakecase('foo_bar_baz') # => "foo_bar_baz"
    snakecase('FooBarBaz') # => "_foo_bar_baz"
    spinalcase('foo_bar_baz') # => "foo-bar-baz"
    spinalcase('FooBarBaz') # => "-foo-bar-baz"
    titlecase('foo_bar_baz') # => "Foo Bar Baz"
    titlecase('FooBarBaz') # => " Foo Bar Baz"
    trimcase('foo_bar_baz') # => "foo_bar_baz"
    trimcase('FooBarBaz') # => "FooBarBaz"
    uppercase('foo_bar_baz') # => "FOO_BAR_BAZ"
    uppercase('FooBarBaz') # => "FOOBARBAZ"
    alphanumcase('_Foo., Bar') # =>'FooBar'
    alphanumcase('Foo_123 Bar!') # =>'Foo123Bar'

**JSON参数验证**

使用[cerberus](https://github.com/pyeve/cerberus)进行json参数验证，
所有验证的`validator_schemas`统一存放在对应的蓝图目录下。

**异步任务**

使用celery做异步调用，需要rabbitmq（broker）和redis（backend）服务。

rabbitmq创建vhost

    ./rabbitmqctl add_user username password
    ./rabbitmqctl set_user_tags username administrator
    ./rabbitmqctl add_vhost vhostname
    ./rabbitmqctl set_permissions -p vhostname username ".*" ".*" ".*"

运行worker：`celery worker -A apis.demo.handlers.celery --loglevel=debug -Q send_email`


## 代码结构说明

所有api以blueprint方式按业务目录存放在apis中，在apiserver.py中统一注册。

每一个业务api中，routes.py存放url路由信息，views.py做业务处理，handlers.py存放可复用代码，validator_schemas.py统一存放json验证schema供view使用

使用flask-script编写的快捷命令统一写在manage.py中。

所有model放在models中，每个model内实现一些常用方法，方法内不管理数据库连接，在业务代码中使用`peewee_mysql`上下文管理器来统一处理。

定时任务采用celery beat实现，统一放在`periodic_tasks`目录下

所有依赖的服务都统一放在services.py中。

通用工具类函数统一放在utils下

部署相关的文件、配置等统一放在deploy下。

sqls文件中存放每一个版本涉及到的所有增量sql

## TODO:

- utils
    - statsd
- 更新deploy目录的内容
- 文档
- tests
    - unittest
    - benchmark
