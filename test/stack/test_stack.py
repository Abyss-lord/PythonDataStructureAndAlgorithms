#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_stack
   Description :
   date：          2024/6/17
-------------------------------------------------
   Change Activity:
                   2024/6/17:
-------------------------------------------------
"""
import threading
from operator import eq

import pytest
from loguru import logger
from src.stack.stack_study import Stack
import random


class TestStack:
    TEST_ROUND: int = 10
    RANDOM_NUMERIC_LOW: int = -10
    RANDOM_NUMERIC_HIGH: int = 10
    STACK = Stack()

    @classmethod
    def test_push_and_pop(cls) -> None:
        stack = Stack()
        tmp = []
        for _ in range(cls.TEST_ROUND):
            rand_val = random.randint(cls.RANDOM_NUMERIC_LOW, cls.RANDOM_NUMERIC_HIGH)
            tmp.append(rand_val)
            stack.push(rand_val)

        for i in range(len(tmp) - 1, -1, -1):
            assert stack.pop() == tmp[i]

    @classmethod
    def test_is_empty(cls) -> None:
        stack = Stack()
        assert stack.is_empty()
        for _ in range(cls.TEST_ROUND):
            rand_val = random.randint(cls.RANDOM_NUMERIC_LOW, cls.RANDOM_NUMERIC_HIGH)
            stack.push(rand_val)

        assert not stack.is_empty()
        assert eq(stack.size(), cls.TEST_ROUND)

    @classmethod
    def test_peek(cls) -> None:
        stack = Stack()
        assert stack.is_empty()
        for _ in range(cls.TEST_ROUND):
            rand_val = random.randint(cls.RANDOM_NUMERIC_LOW, cls.RANDOM_NUMERIC_HIGH)
            stack.push(rand_val)
            assert eq(stack.peek(), rand_val)
        ori_size = stack.size()
        for _ in range(cls.TEST_ROUND):
            stack.peek()
            assert eq(stack.size(), ori_size)

    @classmethod
    def test_clear(cls) -> None:
        stack = Stack()
        assert stack.is_empty()
        for _ in range(cls.TEST_ROUND):
            rand_val = random.randint(cls.RANDOM_NUMERIC_LOW, cls.RANDOM_NUMERIC_HIGH)
            stack.push(rand_val)
            assert eq(stack.peek(), rand_val)

        stack.clear()
        assert stack.is_empty()

    @classmethod
    def thread_function(cls, i: int) -> None:

        for _ in range(cls.TEST_ROUND):
            rand_val = random.randint(cls.RANDOM_NUMERIC_LOW, cls.RANDOM_NUMERIC_HIGH)
            logger.debug("thread-{} push val {}", i, rand_val)
            cls.STACK.push(rand_val)

    @classmethod
    def test_threading(cls) -> None:
        threads = []

        for i in range(5):
            thread = threading.Thread(target=cls.thread_function, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        logger.debug(f"Final value of shared_resource: {cls.STACK}")

    @classmethod
    def test_pop_in_empty_stack(cls) -> None:
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()

    @classmethod
    def test_peek_in_empty_stack(cls) -> None:
        stack = Stack()
        with pytest.raises(IndexError):
            stack.peek()

    @classmethod
    def test_remove_element_by_index(cls) -> None:
        stack = Stack()
        with pytest.raises(IndexError):
            stack.remove_element_by_index(0)

        tmp = []
        for _ in range(cls.TEST_ROUND):
            rand_val = random.randint(cls.RANDOM_NUMERIC_LOW, cls.RANDOM_NUMERIC_HIGH)
            stack.push(rand_val)
            tmp.append(rand_val)

        assert eq(tmp[2], stack.remove_element_by_index(2))
        assert eq(stack.size(), cls.TEST_ROUND - 1)
        with pytest.raises(IndexError):
            stack.remove_element_by_index(-1)
            stack.remove_element_by_index(stack.size())
