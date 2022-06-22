简单工厂：

在一个类里面建立所有的产品。通过if或者其他条件来判断

```python
class SimpleCarFactory(object):
    """简单工厂
    """
    @staticmethod
    def product_car(name):
        if name == 'mb':
          return Mercedes()
        elif name == 'bmw':
          return BMW()
        elif name == 'mbSUV':
          return MercedesSUV()
        elif name == bmwSUV:
          return BMWSUV()
        else:
          print('error')
          
mb_car = SimpleCarFactory.product_car('mb')
bmw_car = SimpleCarFactory.product_car('bmw')
mb_SUV = SimpleCarFactory.product_car('mbSUV')
bmw_SUV = SimpleCarFactory.product_car('bmwSUV')
```

简单工厂升级版？map可以通过读取设定，只需要自行增加映射关系即可，可以通过读取来实现

```python
class SimpleCarFactory(object):
    """简单工厂
    """
    def __init__():
      self.map = {
        'mb':Mercedes,
        'bmw':BMW,
        'mbSUV':MercedesSUV,
        'bmwSUV':BMWSUV
      }
    
    def product_car(name):
      if name in self.map:
        return self.map[name]
      else:
        print('error')
```

工厂方法

可以通过一个基类建立一类产品，每个产品具体由子类进行构建

```python
import abc

class AbstractFactory(object):
    """抽象工厂
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def product_car(self):
      pass

class MercedesFactory(AbstractFactory):
    """梅赛德斯工厂
    """
    def product_car(self):
      return Mercedes()

class BMWFactory(AbstractFactory):
    """宝马工厂
    """
    def product_car(self):
      return BMW()

mb_car = MercedesFactory().product_car()
bmw_car = BMWFactory().product_car()

```

抽象工厂

工厂方法升级版，一个基类建立多类产品，具体产品仍由子类构建

```python
import abc

class AbstractFactory(object):
    """抽象工厂
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def product_car(self):
      pass
    
    @abc.abstractmethod
    def product_SUV(self):
      pass

class MercedesFactory(AbstractFactory):
    """梅赛德斯工厂
    """
    def product_car(self):
      return Mercedes()
      
    def product_SUV(self):
      return MercedesSUV()

class BMWFactory(AbstractFactory):
    """宝马工厂
    """
    def product_car(self):
      return BMW()
      
    def product_SUV(self):
      return BMWSUV()

mb_car = MercedesFactory().product_car()
bmw_car = BMWFactory().product_car()
mb_SUV = MercedesFactory().product_SUV()
bmw_SUV = BMWFactory().product_SUV()

```

[骑鱼嘚猫的文章](https://www.cnblogs.com/ppap/p/11103324.html)
