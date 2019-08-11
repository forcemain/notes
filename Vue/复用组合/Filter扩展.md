----

* [简单介绍](#简单介绍)
* [参数支持](#参数支持)

----

# 简单介绍

> 支持自定义局部过滤器(组件的filter)和全局过滤器(Vue.filter),且过滤器可通过串联的形式跟在表达式后面

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <!-- 开发环境版本，包含了有帮助的命令行警告 -->
        <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
        <!-- 生产环境版本，优化了尺寸和速度 -->
        <!--<script src="https://cdn.jsdelivr.net/npm/vue"></script>-->
        <title>Vue</title>
        <!-- 自定义的类样式 -->
        <style type="text/css">
            * {
                padding: 0;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div id="app">
            {{ 'limanman'|capitalize }}
        </div>
        <script type="text/javascript">
            // 创建一个过滤器,首字母大写
            Vue.filter('capitalize', function(value){
                if(!value) return '';
                return value.toString().charAt(0).toUpperCase() + value.slice(1);
            })
            // 创建一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: '#app'
            });
        </script>
    </body>
</html>
```

# 参数支持

> 自定义过滤器支持多个参数,第一个参数是过滤器前传递过来的值,从第二个参数开始为可接收的参数

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <!-- 开发环境版本，包含了有帮助的命令行警告 -->
        <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
        <!-- 生产环境版本，优化了尺寸和速度 -->
        <!--<script src="https://cdn.jsdelivr.net/npm/vue"></script>-->
        <title>Vue</title>
        <!-- 自定义的类样式 -->
        <style type="text/css">
            * {
                padding: 0;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div id="app">
            {{ 'limanman'|cut(2, 6) }}
        </div>
        <script type="text/javascript">
            // 创建一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: '#app',
                // 过滤对象
                filters: {
                    // 截取过滤器,接收三个参数,第一个参数是原始数据,后面为过滤器本身的参数
                    cut: function(value, start, length){
                        return value.slice(start, start+length);
                    }
                }
            });
        </script>
    </body>
</html>
```

