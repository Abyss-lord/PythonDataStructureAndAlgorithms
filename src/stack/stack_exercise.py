#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     stack_exercise
   Description :
   date：          2024/6/17
-------------------------------------------------
   Change Activity:
                   2024/6/17:
-------------------------------------------------
"""

from collections import deque
from operator import eq, add, sub, mul, truediv
from typing import Callable, Optional
from loguru import logger

DEBUG_ENABLE = False


def divide_by_n(num: int, n: int) -> str:
    """
    将给定的整数转换为指定进制（2到16之间）的字符串表示。

    :param num: 要转换的整数。必须是非负整数。
    :param n: 要转换到的进制。必须在2到16之间（包括2和16）。
    :return: 一个表示该整数在指定进制下的字符串。
    :raises TypeError: 如果 `num` 或 `n` 不是整数。
    :raises ValueError: 如果 `n` 不在2到16之间或者`n`不是2的幂次方
    """

    def is_power_of_2(num: int) -> bool:
        """
        判断一个数是否是2的幂。

        :param num: 要判断的整数。
        :return: 如果是2的幂返回True，否则返回False。
        """

        if num <= 0:
            return False
        return (num & (num - 1)) == 0

    if not isinstance(num, int):
        raise TypeError('num must be an integer')

    if not isinstance(n, int):
        raise TypeError('n must be an integer')

    if n < 2 or n > 16:
        raise ValueError('n must be between 2 and 16')

    if not is_power_of_2(n):
        raise ValueError('The number n must be a power of two')

    # 将整数值映射到在进制大于10时的字符串表示
    mapper = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
              10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

    # 使用 deque 作为栈来存储余数
    stack = deque()

    # 临时变量存储转换过程中的值
    tmp = num

    # 将数字转换为指定的进制
    while tmp > 0:
        rem = tmp % n  # 计算余数
        stack.append(rem)  # 将余数压入栈
        tmp = tmp // n  # 更新待处理的数字

    # 从栈构建最终的字符串
    s = ""
    while len(stack):
        top_element = stack.pop()  # 弹出栈顶元素
        s += mapper[top_element]  # 根据映射表将数字转换为字符串

    return s


def _is_left_bracket(s: str) -> bool:
    """
    判断字符是否为左括号。

    :param s: 要判断的字符
    :return: 如果字符是左括号，返回 True，否则返回 False
    """
    return eq(s, '[') or eq(s, '{') or eq(s, '(')


def _is_right_bracket(s: str) -> bool:
    """
    判断字符是否为右括号。

    :param s: 要判断的字符
    :return: 如果字符是右括号，返回 True，否则返回 False
    """
    return eq(s, ']') or eq(s, ')') or eq(s, '}')


def _get_matched_brackets(s: str) -> str:
    """
    获取与右括号匹配的左括号。

    :param s: 右括号字符
    :return: 匹配的左括号字符
    """
    if eq(s, ']'):
        return '['
    elif eq(s, ')'):
        return '('
    else:
        return '{'


def bracket_matching(s: str) -> bool:
    """
    检查括号字符串是否匹配。

    :param s: 要检查的括号字符串
    :return: 如果括号匹配，返回 True，否则返回 False
    """

    # 使用双端队列作为栈
    stack = deque()
    # 去掉字符串两端的空格
    s = s.strip()

    # 遍历字符串中的每一个字符
    for c in s:
        if _is_left_bracket(c):
            # 如果是左括号，压入栈中
            stack.append(c)
        elif _is_right_bracket(c):
            # 如果是右括号，获取相应的左括号
            required_left_bracket = _get_matched_brackets(c)
            if len(stack) == 0:
                # 如果栈为空，说明没有匹配的左括号，返回 False
                return False
            if eq(stack[-1], required_left_bracket):
                # 如果栈顶元素与匹配的左括号相同，弹出栈顶元素
                stack.pop()
            else:
                # 否则，括号不匹配，返回 False
                return False

    # 最后检查栈是否为空，如果为空则所有括号都匹配
    return len(stack) == 0


def precedence(op):
    """
    定义运算符的优先级。
    :param op: 运算符
    :return: 运算符的优先级，数值越高优先级越高
    """
    if eq(op, '+') or eq(op, '-'):
        return 1
    if eq(op, '*') or eq(op, '/'):
        return 2
    return 0


def infix_to_postfix(expression: str) -> str:
    """
    将中缀表达式转换为后缀表达式。
    :param expression: 中缀表达式字符串
    :return: 后缀表达式字符串
    """
    if not bracket_matching(expression):
        raise ValueError('expression must be a valid expression')
    if DEBUG_ENABLE:
        logger.debug(f"{expression=}")

    # 初始化操作符栈和后缀表达式队列
    op_stack = deque()  # 操作符栈
    postfix = deque()  # 后缀表达式队列
    split = '|'  # 分隔符
    idx = 0  # 表达式索引

    # 遍历表达式中的每个字符
    while idx < len(expression):
        char = expression[idx]

        if char.isalnum():  # 如果是字母或数字，表示操作数
            s = ""
            while idx < len(expression) and expression[idx].isalnum():
                s += expression[idx]
                idx += 1
            postfix.append(s)  # 将操作数添加到后缀表达式队列
            postfix.append(split)  # 添加分隔符，用于后续分隔操作数
        else:
            if char == '(':  # 左括号直接入栈
                op_stack.append(char)

            elif _is_operator(char):  # 如果是运算符
                while len(op_stack) > 0 and precedence(op_stack[-1]) > precedence(char):
                    postfix.append(op_stack.pop())  # 弹出优先级较高的运算符，添加到后缀表达式队列
                op_stack.append(char)  # 当前运算符入栈

            elif eq(char, ')'):  # 如果是右括号
                last_op = op_stack.pop()
                while not eq(last_op, '('):
                    postfix.append(last_op)  # 弹出直到遇到左括号，并添加到后缀表达式队列
                    last_op = op_stack.pop()
            idx += 1

    # 将栈中剩余的操作符全部弹出，添加到后缀表达式队列
    while len(op_stack) > 0:
        postfix.append(op_stack.pop())

    # 将后缀表达式队列转换为字符串并返回
    return "".join(postfix)


def _get_op_func(op: str) -> Callable[[float, float], float]:
    """
    根据运算符返回相应的运算函数。
    :param op: 运算符字符串
    :return: 对应的运算函数
    """
    if eq(op.strip(), '+'):
        return add
    elif eq(op.strip(), '-'):
        return sub
    elif eq(op.strip(), '*'):
        return mul
    elif eq(op.strip(), '/'):
        return truediv


def _is_operator(c: str) -> bool:
    """
    检查字符是否为运算符。
    :param c: 字符
    :return: 如果是运算符返回 True，否则返回 False
    """
    return c in ['+', '-', '*', '/']


def get_result_from_postfix(expression: str) -> Optional[float]:
    """
    从后缀表达式计算结果。
    :param expression: 后缀表达式字符串
    :return: 计算结果
    """
    if DEBUG_ENABLE:
        logger.debug(f"{expression=}")

    # 初始化数字栈
    num_stack = deque()

    idx = 0

    # 遍历表达式中的每个字符
    while idx < len(expression):
        current_char = expression[idx]

        if current_char.isalnum():  # 如果是操作数
            s = ""
            # 处理多位数，用 '|' 分隔
            while current_char != '|':
                s += current_char
                idx += 1
                current_char = expression[idx]
            num_stack.append(float(s))
        elif _is_operator(current_char):  # 如果是运算符
            val1 = num_stack.pop()
            val2 = num_stack.pop()
            op_func = _get_op_func(current_char)
            if op_func == truediv or op_func == sub:
                val1, val2 = val2, val1  # 确保正确的操作数顺序
            num_stack.append(op_func(val1, val2))

            if DEBUG_ENABLE:
                logger.debug(f"{val1=}, {val2=}, {op_func=}, {op_func(val1, val2)=}, {num_stack=}")
            idx += 1
        else:  # 跳过其他字符
            idx += 1

    # 返回计算结果
    return num_stack.pop() if num_stack else None
