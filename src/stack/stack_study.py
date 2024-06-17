#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     stack-study
   Description :
   date：          2024/6/17
-------------------------------------------------
   Change Activity:
                   2024/6/17:
-------------------------------------------------
"""
import threading
from typing import Any


class Stack:
    DEBUG_ENABLE = False
    LOCK = threading.Lock()

    def __init__(self) -> None:
        self._elements = []

    def __str__(self) -> str:
        return str(self._elements)

    def is_empty(self) -> bool:
        """
        测试栈是否为空
        :return:
        """
        return bool(not self._elements)

    def push(self, element: Any) -> Any:
        """
        将数据项 item 添加到栈顶
        :param element: 压栈元素
        :return: item
        """
        if element is None:
            raise ValueError("Element cannot be None")
        self._add_element(element)
        return element

    def peek(self) -> Any:
        """
        从栈返回顶部数据项
        :return: item
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        with Stack.LOCK:
            return self._elements[-1]

    def pop(self) -> Any:
        """
        从栈中删除顶部数据项
        :return: item
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        elements_length = self.size()
        return self.remove_element_by_index(elements_length - 1)

    def size(self) -> int:
        """
        返回栈中数据项的数量
        :return: int
        """
        with Stack.LOCK:
            length = len(self._elements)
            return length

    def clear(self) -> None:
        """
        清理栈
        :return: None
        """
        self._do_clear()

    def remove_element_by_index(self, index: int) -> None:
        """
        根据索引删除栈元素
        :param index: 索引
        :return: None
        """
        with self.LOCK:
            if self.is_empty():
                raise IndexError("remove from empty stack")
            elif index >= len(self._elements):
                raise IndexError(f"Index >= {len(self._elements)}")
            elif index < 0:
                raise IndexError(f"Index < 0")

            return self._elements.pop(index)

    def _do_clear(self) -> None:
        with Stack.LOCK:
            self._elements.clear()

    def _add_element(self, element: Any) -> None:
        with Stack.LOCK:
            self._elements.append(element)
