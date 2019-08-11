----

* [简单介绍](#简单介绍)
* [选项合并](#选项合并)
* [全局混入](#全局混入)
* [合并策略](#合并策略)

----

# 简单介绍

> Mixin提供一种更灵活的方式来预定义组件选项,当组件使用Mixin对象时,预定义的选项将被继承到此组件

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
            
        </div>
        <script type="text/javascript">
            // 创建一个Mixin
            let user_mixin = {
                mounted: function(){
                    // 由于mounted生命周期之后this.$el才会正确赋值,所以需要放在mounted钩子函数中
                    if(this.$el){
                        this.info('root component is mounted')
                    }else{
                        this.info('child component is mounted');
                    }
                },
                methods: {
                    // 简单的消息打印
                    info: function(msg){
                        console.log(msg);
                    }
                }
            }
            // 创建一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: '#app',
                // 混入对象列表
                mixins: [user_mixin]
            });
        </script>
    </body>
</html>
```

# 选项合并

> 目标组件与Mixin选项冲突时,目标组件冲突选项,值为对象的选项内部进行递归合并并以目标组件选项优先,周期钩子内部合并为一个回调数组,因此都会被调用,但混入的周期钩子优先调用,其实合并策略和Vue.extend()一致

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
            当前计数: {{ count }}
        </div>
        <script type="text/javascript">
            // 创建一个Mixin
            let user_mixin = {
                // 会被递归合并,目标组件选项优先
                data: function(){
                    return {
                        count: 0
                    }
                },
                // 会被合并放入数组,顺序调用,此回调优先
                mounted: function(){
                    // 由于mounted生命周期之后this.$el才会正确赋值,所以需要放在mounted钩子函数中
                    if(this.$el){
                        this.info('root component is mounted')
                    }else{
                        this.info('child component is mounted');
                    }
                },
                // 会被递归合并,目标组件选项优先
                methods: {
                    // 简单的消息打印
                    info: function(msg){
                        console.log(msg);
                    }
                }
            }
            // 创建一个Vue实例
            let vm = new Vue({
                // 绑定元素
                el: '#app',
                // 周期钩子
                mounted: function(){
                    alert('虚拟DOM挂载成功!');
                },
                // 混入对象列表
                mixins: [user_mixin],
                // 方法对象
                methods: {
                    // 打印错误消息
                    error: function(msg){
                        console.error(msg);
                    }
                },
                // 数据对象
                data: {
                    count: 10
                }
            });
        </script>
    </body>
</html>
```

# 全局混入

> 支持通过Vue.mixin全局注册混入,但并不推荐因为它将影响之后创建的每一个Vue实例

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
        <div id="app"></div>
        <script type="text/javascript">
            // 创建全局Mixin
            Vue.mixin({
                // 方法对象
                methods: {
                    info: console.log,
                    error: console.error,
                },
                // 周期钩子
                created: function(){
                    this.info('vm instance is created!');
                }
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

# 合并策略

> 支持通过想Vue.config.optionMergeStrategies设置一个方法属性来自定义合并策略,此参数将接收(toVal, fromVal)并需要返回最终合并后的值