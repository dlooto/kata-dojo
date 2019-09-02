# coding=utf-8
#
# Created by junn, on 2019-09-02
#

import logging
from unittest import TestCase

from kata.gildedrose import (
    Item, AgedBrieItem, SulfurasItem, BackstagePassesItem,
    ConjuredItem, Store,
    ITEM_NAMES
)

logs = logging.getLogger(__name__)


class TestItem(TestCase):

    # def setUp(self):
    #     pass

    def test_item_create(self):
        agedbrie = AgedBrieItem(10)
        assert agedbrie.name == ITEM_NAMES['aged_brie']

        backstage_passes = BackstagePassesItem(10)
        assert backstage_passes.name == ITEM_NAMES["backstage_passes"]

        sulfuras = SulfurasItem(10)
        assert sulfuras.name == ITEM_NAMES["sulfuras"]

        conjured = ConjuredItem(10)
        assert conjured.name == ITEM_NAMES['conjured']

    def test_normal_item_qulity_update(self):
        item = Item(sellin=10, quality=50)
        item.update_both()
        assert item.sellin == 9
        assert item.quality == 49


class TestItemExpired(TestCase):

    def test_expired_item_quality_reduction(self):
        """ 测试：过期item品质下降速度 """
        item = Item(10, 50)
        item.make_expired()
        assert not item.is_zero_quality()
        assert item.quality == 38

        item.update_both()
        item.update_both()
        assert item.sellin == -3
        assert item.quality == 34

    def test_item_expired(self):
        """ 测试item是过期的 """
        item = Item(sellin=10, quality=50)
        for i in range(10):
            item.update_both()

        assert not item.is_expired()
        assert item.sellin == 0

        item.update_both()
        assert item.is_expired()
        assert item.sellin == -1

    def test_make_item_expired(self):
        """ 测试：使item过期 """
        item = Item(20, 10)
        item.make_expired()
        assert item.is_expired()

        item.update_both()
        assert item.quality == 0


class TestAgedBrieItem(TestCase):

    def test_aged_brie_quality(self):
        item = AgedBrieItem(30, 40)

        # test quality increased
        item.update_both()
        assert item.sellin == 29
        assert item.quality == 41

        item.make_expired()
        assert item.is_expired()
        assert item.is_max_quality()

        item.update_both()
        assert item.is_expired()
        assert item.is_max_quality()


class TestBackstagePassesItem(TestCase):

    default_sellin = 20

    def setUp(self) -> None:
        self.item = BackstagePassesItem(self.default_sellin, 10)

    def test_expired_quality(self):
        """ 过期，品质立即立马降为0 """
        self.item.make_expired()
        assert self.item.is_expired()
        assert self.item.quality == 0

    def test_5days_left_quality(self):
        for i in range(self.default_sellin-5):
            self.item.update_both()
        assert self.item.sellin == 5

        prev_quality = self.item.quality
        self.item.update_both()
        assert self.item.quality == prev_quality + 3

        prev_quality = self.item.quality
        self.item.update_both()
        assert self.item.quality == prev_quality + 3

    def test_10days_left_quality(self):
        for i in range(self.default_sellin-10):
            self.item.update_both()
        assert self.item.sellin == 10

        prev_quality = self.item.quality
        self.item.update_both()
        assert self.item.quality == prev_quality + 2

    def test_normal_quality(self):
        self.item.update_both()
        prev_quality = self.item.quality
        self.item.update_both()
        assert self.item.quality == prev_quality + 1


class TestSulfurasItem(TestCase):

    def test_sulfuras_sellin_and_quality(self):
        item = SulfurasItem(10)

        item.make_expired()
        assert not item.is_expired()
        assert item.is_max_quality()
        assert item.quality == SulfurasItem.MAX_QUALITY


class TestConjuredItem(TestCase):

    def test_conjured_quality_reduction_velocity(self):
        normal_item = Item(10, 50)
        conjured_item = ConjuredItem(10, 50)
        prev_quality = normal_item.quality

        normal_item.after_many_days(5)
        conjured_item.after_many_days(5)
        assert prev_quality - conjured_item.quality == 2 * (prev_quality - normal_item.quality)

        nq = normal_item.quality
        cq = conjured_item.quality
        normal_item.make_expired()
        conjured_item.make_expired()
        assert cq - conjured_item.quality == 2 * (nq - normal_item.quality)


NORMAL_DATA = {
    "name": ITEM_NAMES['normal'], "sellin": 30, "quality": 50, "num": 10
}

AGED_BRIE_DATA = {
    "name": ITEM_NAMES["aged_brie"], "sellin": 30, "quality": 50, "num": 10
}

SULFURAS_DATA = {
    "name": ITEM_NAMES["sulfuras"], "sellin": 30, "quality": 50, "num": 10
 }


# "conjured":     {"name": "", "sellin": 30, "quality": 50, "num": 10}
# "backstage_passes": {"name": "", "sellin": 30, "quality": 50, "num": 10}


# class TestShop(TestCase):
#
#     def test_shop_create(self):
#         store = Store()

