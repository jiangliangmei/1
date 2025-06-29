#第一题
class Car:
    """汽车类，包含品牌和速度属性，以及加速、刹车方法"""

    def __init__(self, brand):
        """
        初始化汽车对象
        :param brand: 汽车品牌
        """
        self.brand = brand
        self.speed = 0  # 初始速度为0

    def accelerate(self, m):
        """
        加速方法，速度增加m次，每次增加10
        :param m: 加速次数
        """
        if m <= 0:
            print("加速次数需大于0")
            return

        self.speed += m * 10
        print(f"{self.brand} 加速 {m} 次，当前速度：{self.speed} km/h")

    def brake(self, n):
        """
        刹车方法，速度减少n次，每次减少10，不低于0
        :param n: 刹车次数
        """
        if n <= 0:
            print("刹车次数需大于0")
            return

        # 计算刹车后速度，确保不低于0
        self.speed = max(0, self.speed - n * 10)
        print(f"{self.brand} 刹车 {n} 次，当前速度：{self.speed} km/h")

    def get_current_speed(self):
        """获取当前速度"""
        return self.speed



#第二题
# 创建Car实例
my_car = Car("宝马")
print(f"汽车品牌：{my_car.brand}，初始速度：{my_car.speed} km/h")

# 调用加速方法
my_car.accelerate(3)  # 加速3次，速度增加30
my_car.accelerate(2)  # 再加速2次，速度增加20

# 调用刹车方法
my_car.brake(4)  # 刹车4次，速度减少40
my_car.brake(2)  # 再刹车2次，速度减少20（不低于0）

# 输出最终速度
final_speed = my_car.get_current_speed()
print(f"\n最终速度：{final_speed} km/h")




#第三题
class ElectricCar(Car):
    """电动汽车类，继承自Car类，新增电量属性和充电方法"""

    def __init__(self, brand):
        """
        初始化电动汽车对象
        :param brand: 汽车品牌
        """
        super().__init__(brand)  # 调用父类构造方法
        self.battery = 0  # 初始电量为0

    def charge(self, times=1):
        """
        充电方法，电量增加times次，每次增加20，不超过100
        :param times: 充电次数，默认为1次
        """
        if times <= 0:
            print("充电次数需大于0")
            return

        # 计算充电后电量，确保不超过100
        self.battery = min(100, self.battery + times * 20)
        print(f"{self.brand} 充电 {times} 次，当前电量：{self.battery}%")

    def get_current_battery(self):
        """获取当前电量"""
        return self.battery