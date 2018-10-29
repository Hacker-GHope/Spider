from proxypool.scheduler import Scheduler
import sys
import io

# 设置标准输出（指定编码方式：防止中文乱码）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
