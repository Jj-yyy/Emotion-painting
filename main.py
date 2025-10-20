from p5 import *
import random

# 全局变量
images = {}
selected_emotion = None
painting_started = False
teardrops = []  # 存储眼泪粒子
sparks = []  # 存储火花粒子
happy_bubbles = []  # 存储快乐气泡粒子
calm_ripples = []  # 存储平静波纹粒子

# 快乐气泡粒子类
class HappyBubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)  # 左右轻微摆动
        self.vy = random.uniform(-3, -1.5)  # 向上浮动
        self.yellow = random.randint(200, 255)
        self.orange = random.randint(150, 255)
        self.size = random.randint(15, 35)
        self.alpha = 200  # 初始透明度
        self.lifetime = random.randint(20, 35)  # 生命周期
        self.age = 0
        self.wobble = random.uniform(0, 360)  # 摆动相位
        
    def update(self):
        # 向上浮动，带有左右摆动
        self.wobble += random.uniform(5, 15)
        self.x += self.vx + sin(radians(self.wobble)) * 0.5
        self.y += self.vy
        # 速度逐渐减缓
        self.vy *= 0.98
        self.age += 1
        # 逐渐消失
        self.alpha = 200 * (1 - self.age / self.lifetime)
        # 尺寸逐渐增大（膨胀效果）
        self.size = self.size * 1.02
        
    def display(self):
        if self.alpha > 0:
            no_stroke()
            # 外层光晕
            fill(self.yellow, self.orange, 0, int(self.alpha * 0.3))
            circle((self.x, self.y), self.size * 1.3)
            # 主气泡
            fill(self.yellow, self.orange, 50, int(self.alpha))
            circle((self.x, self.y), self.size)
            # 内层高光
            fill(255, 255, 200, int(self.alpha * 0.6))
            circle((self.x - self.size * 0.2, self.y - self.size * 0.2), self.size * 0.4)
            
    def is_dead(self):
        return self.age >= self.lifetime or self.y < -50

# 眼泪粒子类
class Teardrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blue_shade = random.randint(150, 255)
        self.alpha = 150  # 初始透明度
        self.speed = random.uniform(1, 3)  # 下落速度
        self.size_w = random.randint(8, 15)
        self.size_h = random.randint(12, 25)
        self.lifetime = random.randint(30, 60)  # 生命周期（帧数） - 减半，更快消散
        self.age = 0
        
    def update(self):
        # 向下移动
        self.y += self.speed
        self.age += 1
        # 逐渐消失（透明度降低）
        self.alpha = 150 * (1 - self.age / self.lifetime)
        
    def display(self):
        if self.alpha > 0:
            fill(50, 100, self.blue_shade, int(self.alpha))
            ellipse((self.x, self.y), self.size_w, self.size_h)
            
    def is_dead(self):
        return self.age >= self.lifetime or self.y > 600

# 火花粒子类
class Spark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(2, 6)  # 向外扩散速度
        self.vx = self.speed * cos(radians(self.angle))
        self.vy = self.speed * sin(radians(self.angle))
        self.red = random.randint(200, 255)
        self.orange = random.randint(100, 200)
        self.size = random.randint(5, 12)
        self.alpha = 180  # 初始透明度
        self.lifetime = random.randint(15, 35)  # 生命周期 - 减半，更快消散
        self.age = 0
        self.shape = random.choice(['circle', 'rect'])  # 随机形状
        
    def update(self):
        # 向外扩散移动
        self.x += self.vx
        self.y += self.vy
        # 速度衰减（摩擦力）
        self.vx *= 0.95
        self.vy *= 0.95
        self.age += 1
        # 逐渐消失
        self.alpha = 180 * (1 - self.age / self.lifetime)
        # 尺寸逐渐缩小 - 加快缩小速度
        self.size = max(2, self.size * 0.93)
        
    def display(self):
        if self.alpha > 0:
            no_stroke()
            # 颜色从亮橙到深红渐变
            color_shift = self.age / self.lifetime
            r = int(self.red - color_shift * 50)
            g = int(self.orange * (1 - color_shift))
            fill(r, g, 0, int(self.alpha))
            
            if self.shape == 'circle':
                circle((self.x, self.y), self.size)
            else:
                rect(self.x, self.y, self.size, self.size * 1.5)
                
    def is_dead(self):
        return self.age >= self.lifetime

# 平静波纹粒子类
class CalmRipple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.green = random.randint(150, 220)
        self.blue = random.randint(180, 230)
        self.size = random.randint(10, 20)
        self.max_size = self.size + random.randint(60, 100)
        self.alpha = 120  # 初始透明度
        self.lifetime = random.randint(25, 40)  # 生命周期
        self.age = 0
        self.expand_speed = random.uniform(1.5, 3)
        
    def update(self):
        # 波纹扩散
        self.size += self.expand_speed
        self.age += 1
        # 逐渐消失
        self.alpha = 120 * (1 - self.age / self.lifetime)
        
    def display(self):
        if self.alpha > 0:
            # 绘制多层同心圆
            for i in range(3):
                layer_alpha = self.alpha * (1 - i * 0.25)
                layer_size = self.size + i * 8
                if layer_alpha > 0:
                    no_fill()
                    stroke(100, self.green, self.blue, int(layer_alpha))
                    stroke_weight(2 - i * 0.5)
                    circle((self.x, self.y), layer_size)
            no_stroke()
            
    def is_dead(self):
        return self.age >= self.lifetime or self.size >= self.max_size

def setup():
    size(800, 600)
    global images
    images["happy"] = load_image("assets/happy.png")
    images["sad"] = load_image("assets/sad.png")
    images["angry"] = load_image("assets/angry.png")
    images["calm"] = load_image("assets/calm.png")
    text_align("CENTER")

def draw():
    global selected_emotion, teardrops, sparks, happy_bubbles, calm_ripples

    if selected_emotion is None:
        # 显示选择界面 - 每帧刷新背景
        background(255)
        fill(0)  # 设置文字颜色为黑色
        text("Select your emotion", width / 2, 50)
        
        # 居中显示四个情绪图片
        # 计算起始x坐标使其居中 (4个图片，每个120宽，间距40)
        total_width = 4 * 120 + 3 * 40  # 4个图片 + 3个间距
        start_x = (width - total_width) / 2
        x = start_x
        
        for emotion, img in images.items():
            image(img, x, 200, 120, 120)
            fill(0)  # 确保文字是黑色
            text(emotion, x + 60, 340)
            x += 160  # 120(图片宽) + 40(间距)
    else:
        # 绘画模式 - 根据情绪类型处理背景
        # Happy 和 Calm 模式：使用半透明白色淡化背景，让粒子逐渐消失
        if selected_emotion == "happy" or selected_emotion == "calm":
            no_stroke()
            fill(255, 255, 255, 25)  # 半透明白色，逐渐淡化旧内容
            rect(0, 0, width, height)
        
        # 只在顶部显示提示文字和返回按钮
        no_stroke()
        fill(255)  # 白色背景条
        rect(0, 0, width, 70)
        fill(0)  # 设置文字颜色为黑色
        text(f"Painting with emotion: {selected_emotion}", width / 2, 30)
        
        # 绘制圆形返回按钮（简约风）
        button_x = 30  # 左上角位置
        button_y = 30
        button_radius = 22  # 圆形半径
        
        # 按钮阴影
        no_stroke()
        fill(0, 0, 0, 20)
        circle((button_x + 2, button_y + 2), button_radius * 2)
        
        # 按钮主体（柔和的灰色圆圈）
        fill(240, 240, 245)
        circle((button_x, button_y), button_radius * 2)
        
        # 按钮边框
        no_fill()
        stroke(200, 200, 210)
        stroke_weight(1.5)
        circle((button_x, button_y), button_radius * 2)
        
        # 绘制返回箭头（<- 形状）
        no_fill()
        stroke(100, 100, 120)
        stroke_weight(2.5)
        # 箭头线条
        line(button_x - 8, button_y, button_x + 6, button_y)
        # 箭头尖端（两条短线组成 <）
        line(button_x - 8, button_y, button_x - 3, button_y - 5)
        line(button_x - 8, button_y, button_x - 3, button_y + 5)
        
        no_stroke()
        
        # 如果是 sad 模式，更新和绘制眼泪粒子
        if selected_emotion == "sad":
            # 更新所有眼泪
            for tear in teardrops:
                tear.update()
                tear.display()
            # 移除已经消失的眼泪
            teardrops[:] = [tear for tear in teardrops if not tear.is_dead()]
        
        # 如果是 angry 模式，更新和绘制火花粒子
        if selected_emotion == "angry":
            # 更新所有火花
            for spark in sparks:
                spark.update()
                spark.display()
            # 移除已经消失的火花
            sparks[:] = [spark for spark in sparks if not spark.is_dead()]
        
        # 如果是 happy 模式，更新和绘制快乐气泡
        if selected_emotion == "happy":
            # 更新所有气泡
            for bubble in happy_bubbles:
                bubble.update()
                bubble.display()
            # 移除已经消失的气泡
            happy_bubbles[:] = [bubble for bubble in happy_bubbles if not bubble.is_dead()]
        
        # 如果是 calm 模式，更新和绘制平静波纹
        if selected_emotion == "calm":
            # 更新所有波纹
            for ripple in calm_ripples:
                ripple.update()
                ripple.display()
            # 移除已经消失的波纹
            calm_ripples[:] = [ripple for ripple in calm_ripples if not ripple.is_dead()]

def mouse_pressed():
    global selected_emotion
    
    if selected_emotion is None:
        # 在选择界面，检查点击了哪个情绪图片
        # 使用与draw函数相同的居中计算
        total_width = 4 * 120 + 3 * 40
        start_x = (width - total_width) / 2
        x = start_x
        
        for emotion, img in images.items():
            if x < mouse_x < x + 120 and 200 < mouse_y < 320:
                selected_emotion = emotion
                background(255)  # 清空画布，准备绘画
            x += 160
    else:
        # 在绘画界面，检查是否点击了圆形返回按钮
        button_x = 30
        button_y = 30
        button_radius = 22
        # 计算鼠标到按钮中心的距离
        distance = ((mouse_x - button_x) ** 2 + (mouse_y - button_y) ** 2) ** 0.5
        if distance <= button_radius:
            selected_emotion = None  # 返回选择界面
            teardrops.clear()  # 清空眼泪粒子
            sparks.clear()  # 清空火花粒子
            happy_bubbles.clear()  # 清空快乐气泡
            calm_ripples.clear()  # 清空平静波纹
            background(255)  # 清空画布

def mouse_dragged():
    global selected_emotion
    # 只有选了情绪才可以绘画
    if selected_emotion is not None:
        draw_brush(mouse_x, mouse_y)

def draw_brush(x, y):
    global selected_emotion
    no_stroke()

    if selected_emotion == "happy":
        # 快乐效果 - 创建向上浮动的明亮气泡
        global happy_bubbles
        # 创建主气泡
        happy_bubbles.append(HappyBubble(x, y))
        # 偶尔创建额外的小气泡
        if random.random() < 0.4:
            happy_bubbles.append(HappyBubble(x + random.randint(-15, 15), y + random.randint(-10, 10)))
    elif selected_emotion == "sad":
        # 眼泪效果 - 创建会逐渐消失的眼泪粒子
        global teardrops
        # 创建主眼泪
        teardrops.append(Teardrop(x, y))
        # 偶尔创建额外的小水滴
        if random.random() < 0.3:
            teardrops.append(Teardrop(x + random.randint(-10, 10), y + random.randint(5, 15)))
    elif selected_emotion == "angry":
        # 愤怒效果 - 创建会逐渐消散的火花粒子
        global sparks
        # 创建中心爆裂火花
        for i in range(random.randint(6, 12)):
            sparks.append(Spark(x, y))
    elif selected_emotion == "calm":
        # 平静效果 - 创建逐渐扩散消失的波纹粒子
        global calm_ripples
        # 创建主波纹
        calm_ripples.append(CalmRipple(x, y))
        # 偶尔创建额外的小波纹
        if random.random() < 0.3:
            calm_ripples.append(CalmRipple(x + random.randint(-15, 15), y + random.randint(-15, 15)))

if __name__ == '__main__':
    run()