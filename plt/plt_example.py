import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # 生成数据
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # 创建画布
    # figsize 参数指定图形的宽度和高度（单位为英寸）
    # dpi 每英寸点数，控制分辨率
    plt.figure(figsize=(10, 5), dpi=100)
        
    # 绘制线图
    plt.plot(x, y, label='Sine Wave', color='blue', linestyle='-')
    plt.title('Sine Wave Example')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend() # 显示label
    
    # 打开当前坐标系的网格线
    plt.grid(True)

    # 显示图形
    plt.show()