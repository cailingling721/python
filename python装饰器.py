# https://foofish.net/python-decorator.html （理解python装饰器）
# https://www.zhihu.com/question/26930016 (python教程的回答)
# https://segmentfault.com/a/1190000007837364 （python装饰器执行顺序迷思）

## 装饰器的定义 ##
def decorator_a(func):
    print('Get in decorator_a' # 这里就是为了看执行顺序
    def inner_a(*args, **kwargs): # *args, **kwargs就是f的参数列表，这里的f函数没有传参数的话，我们写上也不影响，建议都写上 
        print('Get in inner_a') # 增加新的功能
        return func(*args, **kwargs) # 保留原有的功能
    return inner_a # 装饰器的返回值是一个函数，这个函数是经过包装的。

def decorator_b(func):
    print('Get in decorator_b')
    def inner_b(*args, **kwargs):
        print('Get in inner_b')
        return func(*args, **kwargs)
    return inner_b

@decorator_b
@decorator_a
def f(x):
    print('Get in f')
    return x * 2

f(1) # 函数调用，这时候才会执行装饰器内部返回的函数，如果不调用的话就不会执行装饰器返回的包装函数 ##

## 上述代码的执行顺序 ##
# 上面代码的等效于 decorator_b(decorator_a(f(x)))
# 代码的执行顺序是从内到外


## 上述代码运行结果的输出 ##
# 上面代码先定义里两个函数: decotator_a, decotator_b;
# 这两个函数实现的功能是，接收一个函数作为参数然后返回创建的另一个函数，在这个创建的函数里调用接收的函数(文字比代码绕人)。
# 最后定义的函数f 采用上面定义的 decotator_a, decotator_b 作为装饰函数。
# 在当我们以1为参数调用装饰后的函数f后， decotator_a, decotator_b 的顺序是什么呢?
# 实际上运行的结果如下:
# Get in decorator_a
# Get in decorator_b
# Get in inner_b
# Get in inner_a
# Get in f


## 函数和函数调用的区别 ##
# 上面的例子中 f 称之为函数， f(1) 称之为函数调用，后者是对前者传入参数进行求值的结果。
# 在Python中函数也是一个对象，所以 f 是指代一个函数对象，它的值是函数本身， f(1) 是对函数的调用.
# 同样地，拿上面的decorator_a 函数来说，它返回的是个函数对象inner_a ，这个函数对象是它内部定义的。
# 在 inner_a 里调用了函数 func ，将 func 的调用结果作为值返回。


## 装饰器函数在被装饰函数定义好后立即执行 ##
def decorator_a(func):
    print('Get in decorator_a')
    def inner_a(*args, **kwargs):
        print('Get in inner_a')
        return func(*args, **kwargs)
    return inner_a

@decorator_a
def f(x):
    print('Get in f')
    return x * 2

## method 1 ##
@decorator_a
def f(x):
    print('Get in f')
    return x * 2

## method 2 ##
def f(x):
    print('Get in f')
    return x * 2

f = decorator_a(f)

# 所以，当解释器执行这段代码时， decorator_a 已经调用了，它以函数 f 作为参数， 返回它内部生成的一个函数;
# 所以此后 f 指代的是 decorater_a 里面返回的 inner_a;
# 所以当以后调用 f 时，实际上相当于调用 inner_a ,传给 f 的参数会传给 inner_a;
# 在调用 inner_a 时会把接收到的参数传给 inner_a 里的 func 即 f;
# 最后返回的是 f 调用的值，所以在最外面看起来就像直接再调用 f 一样.


## 重新梳理执行顺序 ##
# 当解释器执行下面这段代码时，实际上按照从下到上的顺序已经依次调用了 decorator_a 和 decorator_b ，这时会输出对应的 Get in decorator_a 和 Get in decorator_b 。 
# 这时候 f 已经相当于 decorator_b 里的 inner_b 。但因为 f 并没有被调用，所以 inner_b 并没有调用，依次类推 inner_b 内部的 inner_a 也没有调用，所以 Get in inner_a 和 Get in inner_b 也不会被输出。

@decorator_b
@decorator_a
def f(x):
    print('Get in f')
    return x * 2

# 然后最后一行当我们对 f 传入参数1进行调用时，inner_b 被调用了，它会先打印 Get in inner_b;
# 然后在 inner_b 内部调用了 inner_a 所以会再打印 Get in inner_a;
# 然后再 inner_a 内部调用的原来的 f, 并且将结果作为最终的返回。
