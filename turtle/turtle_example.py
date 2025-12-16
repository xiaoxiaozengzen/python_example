import turtle
import math

# 创建画布
screen = turtle.Screen()
# 设置画布大小，标题和背景颜色
screen.setup(width=1000, height=700)
screen.title("Rocket Launch Site - Turtle Art")
screen.bgcolor('#87CEEB')

# 创建画笔
t = turtle.Turtle()
# 隐藏画笔
t.hideturtle()
# 提高绘图速度，其中0：最快且无动画效果，1-10：捉逐渐变快速并且带有动画效果
t.speed(0)


def draw_rect(x, y, w, h, color):
    """Draw a filled rectangle with bottom-left corner at (x, y)."""
    # 抬起画笔
    t.penup()
    # 移动到指定位置。画布中心位置是(0, 0)，x轴正方向是向右，y轴正方向是向上
    t.goto(x, y)
    # 落下画笔
    t.pendown()
    
    # 设置填充颜色
    t.fillcolor(color)
    # 开始填充
    t.begin_fill()
    for _ in range(2):
        t.forward(w); t.right(90)
        t.forward(h); t.right(90)
    # 结束填充，会把闭合图形填充颜色，若路径未显示闭合，则把起点和终点连接起来进行填充
    t.end_fill()
    t.penup()

def draw_circle(x, y, r, color):
    """Draw a filled circle centered at (x, y) with radius r."""
    t.penup()
    t.goto(x, y-r)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(r)
    t.end_fill()
    t.penup()

def draw_cloud(x, y, scale=1.0):
    """Draw a cloud at (x, y) with given scale."""
    # 设置画笔颜色为白色
    t.color('white')
    offsets = [(-40,0),(-20,10),(0,0),(25,5),(50,0)]
    for ox, oy in offsets:
        draw_circle(x+ox*scale, y+oy*scale, 20*scale, 'white')

def draw_launchpad():
    """Draw the launchpad structure."""
    # base
    draw_rect(-260, -220, 520, 40, '#555555')
    # support columns
    for i in range(-220, 221, 110):
        draw_rect(i-10, -180, 20, 120, '#333333')
    # platform top
    draw_rect(-160, -60, 320, 20, '#777777')
    # railing
    t.pensize(3)
    t.color('#222222')
    t.penup(); t.goto(-160, -40); t.pendown(); t.goto(160, -40)
    t.penup(); t.pensize(1)

def draw_rocket(x, y, scale=1.0):
    """Draw a rocket at (x, y) with given scale."""
    # rocket body
    body_w = 60*scale; body_h = 220*scale
    t.penup(); t.goto(x, y)
    t.setheading(0)
    t.pendown(); t.fillcolor('#EAEAEA'); t.begin_fill()
    t.forward(body_w/2)
    t.left(90); t.forward(body_h - 40*scale)
    # nose cone curve
    t.circle(body_w/2, 180)
    t.forward(body_h - 40*scale)
    t.left(90); t.end_fill(); t.penup()

    # nose cone (top)
    t.goto(x + body_w/2, y + body_h - 40*scale)
    t.fillcolor('#DD3333'); t.begin_fill()
    t.setheading(90); t.circle(body_w/2, 180); t.end_fill(); t.penup()

    # windows
    win_r = 12*scale
    draw_circle(x + body_w/2, y + body_h*0.6, win_r, '#88CCFF')
    draw_circle(x + body_w/2, y + body_h*0.45, win_r, '#88CCFF')

    # fins
    t.fillcolor('#AA2222')
    for sign in (-1,1):
        t.penup(); t.goto(x + body_w/2, y + 20*scale)
        t.pendown(); t.begin_fill()
        t.setheading(270 if sign==-1 else 90)
        t.left(sign*20)
        t.forward(40*scale)
        t.right(sign*60)
        t.forward(30*scale)
        t.goto(x + body_w/2, y + 20*scale)
        t.end_fill(); t.penup()

    # exhaust (flame) - simple layered circles
    fx = x + body_w/2; fy = y
    for i, col in enumerate(['#FFDD33','#FF6622','#FF2200']):
        draw_circle(fx, fy - i*8*scale, 18*scale - i*4*scale, col)

def draw_control_center(x, y):
    # building
    draw_rect(x, y, 140, 100, '#C0C0C0')
    draw_rect(x+10, y+30, 40, 40, '#333333')
    draw_rect(x+70, y+30, 40, 40, '#333333')
    # roof (triangle)
    t.fillcolor('#884422')
    t.penup(); t.goto(x, y+100); t.pendown(); t.begin_fill()
    t.goto(x+70, y+150); t.goto(x+140, y+100); t.goto(x, y+100); t.end_fill(); t.penup()
    # antenna
    t.pensize(2); t.color('#222222'); t.penup(); t.goto(x+70, y+100); t.pendown()
    t.goto(x+70, y+140); t.dot(8, 'red'); t.penup(); t.pensize(1)

def draw_scene():
    # sky gradient simulated with rectangles
    for i, color in enumerate(['#87CEEB','#9FD5FF','#BFE8FF']):
        draw_rect(-500, 200 - i*120, 1000, 120, color)

    # clouds
    draw_cloud(-300, 220, 1.2)
    draw_cloud(-120, 250, 0.9)
    draw_cloud(140, 230, 1.1)
    draw_cloud(300, 260, 0.8)

    # ground
    draw_rect(-500, -260, 1000, 200, '#2E8B57')

    # launchpad and rocket
    draw_launchpad()
    draw_rocket(-30, -40, 1.0)

    # control center
    draw_control_center(220, -140)

    # signage and details
    t.penup(); t.goto(-420, -190); t.color('white'); t.write('LAUNCH PAD 7', font=('Arial', 14, 'bold'))

    # clouds lower
    draw_cloud(-200, 120, 0.7)
    draw_cloud(60, 140, 0.8)

if __name__ == '__main__':
    draw_scene()
    # t.hideturtle()
    screen.mainloop()