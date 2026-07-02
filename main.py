from agent import FeedbackAgent
from file_reader import read_file
import time

SAMPLE_COURSE_CONTENT = """本次课程为 Python 编程入门第3课，主要内容包括：
1. 变量与数据类型：介绍了整数、浮点数、字符串、布尔值等基本数据类型，以及变量的命名规则和赋值操作
2. 运算符：讲解了算术运算符（+、-、*、/、//、%、**）、比较运算符和逻辑运算符
3. 条件语句：详细讲解了 if-elif-else 条件判断结构，包括缩进的重要性和条件表达式的书写
4. 实战练习：通过3个练习题巩固所学知识，分别是计算圆的面积、判断成绩等级、简单的猜数字游戏逻辑

教学目标：让学生掌握基本的数据类型和运算符，能够使用条件语句解决简单的逻辑判断问题"""

SAMPLE_STUDENT_PERFORMANCE = """学员张三在本节课表现如下：
1. 课堂参与：积极举手回答问题，参与度高，共回答了5次问题
2. 知识掌握：对变量和数据类型掌握较好，能够正确进行类型转换；运算符部分理解基本正确，但在整除和取模运算上有些混淆
3. 条件语句：能够独立写出简单的 if-else 语句，但在多条件判断时需要提示
4. 练习情况：完成了前两道练习题，第三道猜数字游戏逻辑思路正确，但代码实现上有一些语法错误
5. 学习态度：学习热情高，遇到问题主动提问，笔记记录认真
6. 存在问题：对缩进的理解还不够深刻，有时会忘记缩进或缩进不正确"""

def main():
    print("=" * 60)
    print("          课后反馈智能体")
    print("=" * 60)
    print()

    print("【使用示例】")
    print("课程内容：", SAMPLE_COURSE_CONTENT[:50] + "...")
    print("学员表现：", SAMPLE_STUDENT_PERFORMANCE[:50] + "...")
    print()

    print("请选择输入方式：")
    print("  1. 使用示例数据")
    print("  2. 手动输入")
    print("  3. 从文件读取")
    print()

    choice = input("请输入选择 (1/2/3): ").strip()

    course_content = ""
    student_performance = ""

    if choice == '1':
        course_content = SAMPLE_COURSE_CONTENT
        student_performance = SAMPLE_STUDENT_PERFORMANCE
    elif choice == '2':
        print("\n请输入课程内容：")
        course_content = input().strip()
        print("\n请输入学员表现：")
        student_performance = input().strip()
    elif choice == '3':
        print("\n请输入课程内容文件路径：")
        course_file = input().strip()
        print("\n请输入学员表现文件路径：")
        student_file = input().strip()

        try:
            course_content = read_file(course_file)
            print(f"✓ 课程内容文件读取成功，长度: {len(course_content)} 字符")
        except Exception as e:
            print(f"✗ 读取课程内容文件失败: {e}")
            return

        try:
            student_performance = read_file(student_file)
            print(f"✓ 学员表现文件读取成功，长度: {len(student_performance)} 字符")
        except Exception as e:
            print(f"✗ 读取学员表现文件失败: {e}")
            return
    else:
        print("无效选择，请输入 1、2 或 3")
        return

    print("\n正在生成课后反馈报告...")
    print("=" * 60)

    agent = FeedbackAgent()

    try:
        for chunk in agent.generate_report_streaming(course_content, student_performance):
            print(chunk, end="", flush=True)
            time.sleep(0.02)
        print("\n" + "=" * 60)
        print("\n报告生成完成！")
    except ValueError as e:
        print(f"\n输入错误：{e}")
    except Exception as e:
        print(f"\n生成报告时出现错误：{e}")
        print("\n请检查您的 API 密钥配置是否正确。")

if __name__ == "__main__":
    main()