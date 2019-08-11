----

* [创建Vue实例](#创建Vue实例)
* [数据与方法](#数据与方法)
* [实例生命周期钩子](#实例生命周期钩子)

----

# 创建Vue实例

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
    </head>
    <body>
        <script type="text/javascript">    
            // 任何应用以一个根new Vue作为入口,通常用vm(ViewModel)变量来表示Vue实例
            let vm = new Vue({
                
            })
        </script>
    </body>
</html>
```

* 任何Vue应用都是通过根new Vue实例作为入口及可选的,嵌套的,可复用的组件树构成,其实组件树中的每个组件都是Vue实例,同样可以接受相同的[选项对象](https://cn.vuejs.org/v2/api/#%E9%80%89%E9%A1%B9-%E6%95%B0%E6%8D%AE)

# 数据与方法

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
    </head>
    <body>
        <div id="app">
            <!-- 以文本插值的方式将clicks与数据对象的clicks属性绑定 -->
            <span id="clicks">{{ clicks }}</span>
        </div>
        <script type="text/javascript">    
            // 实例化一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: "#app",
                // 数据对象
                data: {
                    clicks: 1
                }
            })
            
            // 定时每秒将vm.clicks值自增1
            setInterval(function(){
                vm.clicks += 1;
            }, 1000)
        </script>
    </body>
</html>
```

* Vue实例创建时会自动将数据对象中的所有属性抽象化为包含setter/getter特性的同名方法,当属性值发生改变时会自动触发视图更新(其实就是在setter特性中完成视图更新操作)
* 需要注意的是只有首次Vue实例化时数据对象data中的属性才会被抽象化为包含getter/setter特性的同名方法,后期在实例或数据对象顶层新增的属性是不会被抽象化的,也就是说不会响应式

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
    </head>
    <body>
        <div id="app"></div>
        <script type="text/javascript">    
            let data = {
                clicks: 0
            };
            // 实例化一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: '#app',
                // 数据对象
                data: data
            })
            
            // 实例属性vm.$el其实就是document.getElementById("app")
            document.write('实例属性vm.$el == document.getElementById("app") '
                           + (vm.$el == document.getElementById('app'))
                           + '<br>')
            // 实例属性vm.$data其实就是data
            document.write('实例属性vm.$data == data '
                           + (vm.$data == data )
                           + '<br>')
            // 需要注意的是此处并非将clicks属性抽象化为包含getter/setter特性的同名方法,而是为其值改变事件新增自定义逻辑
            // clicks必须在data中预先定义
            vm.$watch('clicks', function(n, o){
                document.write('vm.clicks属性值被设置为: ' + n + '<br>');
            })
            setTimeout(function(){
                vm.clicks += 1; 
            }, 3000);
        </script>
    </body>
</html>
```

* Vue实例自身也提供也一些以$开头的[实例属性](https://cn.vuejs.org/v2/api/#%E5%AE%9E%E4%BE%8B%E5%B1%9E%E6%80%A7)和[实例方法](https://cn.vuejs.org/v2/api/#%E5%AE%9E%E4%BE%8B%E6%96%B9%E6%B3%95-%E6%95%B0%E6%8D%AE)
* vm.$el表示原生元素对象,vm.\$data表示数据对象,vm.\$watch支持为已存在的数据对象属性添加自定义变更逻辑

# 实例生命周期钩子

> Vue实例在创建到销毁整个生命周期如设置数据监听,编译模版,将实例挂载到DOM并在数据发生变化时更新DOM等,提供了一系列生命周期钩子的函数,使得用户可以在不同阶段添加自己代码

![lifecycle](VUE 实例.assets/image-20190103145631418-6498591.png)

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
    </head>
    <body>
        <div id="app"></div>
        <script type="text/javascript">    
            // 实例化一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: '#app',
                // 数据对象
                data: {
                    clicks: 0
                },
                // Vue实例被创建后执行如下钩子
                created: function(){
                    document.write('Vue实例初始化完毕,' 
                                   + JSON.stringify(this.$data)
                                   + '中的属性被抽象化为包含setter/getter特性的同名方法'
                                   + '<br>')
                }
            })
        </script>
    </body>
</html>
```

* 需要注意的是不要在生命周期钩子函数中使用箭头函数,由于箭头函数中没有this,将向上作用域查找可能导致调用错误

