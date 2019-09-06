# coding=utf-8
#
# Created by junn, on 2019-09-02
#

import logging
from unittest import TestCase

import pytest

from kata.gildedrose import (
    Item, AgedBrieItem, SulfurasItem, BackstagePassesItem,
    ConjuredItem, Store,
    ITEM_NAMES,
    ItemFactory)

logs = logging.getLogger(__name__)


class ItemTest(TestCase):

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


def test_item_names_dict():
    items_data = ItemFactory.init_item_data_dict()
    assert items_data.get("aged_brie") is not None
    assert items_data["aged_brie"].get("name") == ITEM_NAMES["aged_brie"]


def test_factory_new_item():
    item = ItemFactory.new_item("unkown_item", **{"sellin": 10, "quality": 50})
    assert item is None

    item = ItemFactory.new_item("normal", **{"sellin": 10, "quality": 50})
    assert item.sellin == 10
    assert isinstance(item, Item)
    item = ItemFactory.new_item("conjured", **{"sellin": 10, "quality": 50})
    assert type(item) == ConjuredItem


ITEMS_DATA = {
    "normal": {"sellin": 10, "quality": 50},
    "sulfuras": {"sellin": 30, "quality": 80},
    "conjured": {"sellin": 20, "quality": 50},
    "aged_brie": {"sellin": 30, "quality": 30},
    "backstage_passes": {"sellin": 30, "quality": 50},
}


def test_factory_init_items():
    items_data = ITEMS_DATA
    item_dict = ItemFactory.init_items(items_data)
    conjured_item = item_dict.get("conjured")
    assert conjured_item is not None
    assert conjured_item.sellin == items_data["conjured"]["sellin"]


def test_shop_create():
    items_data = ITEMS_DATA
    store = Store(items_data)

    store.pass_one_day()

    normal_item = store.item_dict.get("normal")
    assert normal_item is not None
    assert items_data["normal"]["sellin"] == normal_item.sellin + 1

    store.pass_many_days(39)

    aged_brie_item = store.item_dict.get("aged_brie")
    assert items_data["aged_brie"]["sellin"] == aged_brie_item.sellin + 40
    assert aged_brie_item.quality == 50

    backstage_item = store.item_dict.get("backstage_passes")
    assert items_data["backstage_passes"]["sellin"] == backstage_item.sellin + 40

    sulfuras_item = store.item_dict.get("sulfuras")
    assert items_data["sulfuras"]["quality"] == sulfuras_item.quality




