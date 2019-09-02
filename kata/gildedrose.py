# coding=utf-8
#
# Created by junn, on 2019-09-01
#

# 


ITEM_NAMES = {
    "normal": "Normal",
    "aged_brie": "Aged Brie",
    "backstage_passes": "Backstage passes",
    "sulfuras": "Sulfuras",
    "conjured": "Conjured"
}


class Item:
    """
    一旦销售期限过期，品质`Quality`会以双倍速度加速下降
    物品品质  0<=quality<=50，
    每天结束时，系统会降低每种物品的这两个数值
    """

    MAX_QUALITY = 50

    def __init__(self, sellin, quality=MAX_QUALITY):
        self.name = ITEM_NAMES['normal']
        self.sellin = sellin
        self.quality = quality

    def is_expired(self):
        return self.sellin < 0

    def is_zero_quality(self):
        return self.quality == 0

    def is_max_quality(self):
        return self.quality == self.MAX_QUALITY

    def make_expired(self):
        for i in range(self.sellin + 1):
            self.update_both()

    def make_zero_sellin(self):
        for i in range(self.sellin):
            self.update_both()

    def after_many_days(self, days):
        for i in range(days):
            self.update_both()

    def update_both(self):
        """
        每天结束时调用该方法，降低sellin和quality值.
        注：以下两方法调用顺序不能调换
        """
        self.decr_sellin()
        self.update_quality()

    def update_quality(self):
        if self.quality == 0:
            return

        if self.is_expired():    # expired
            self.quality -= 2
        else:
            self.quality -= 1

        self._correct_min_quality()

    def decr_sellin(self):
        self.sellin -= 1

    def _correct_min_quality(self):
        self.quality = 0 if self.quality < 0 else self.quality


class AgedBrieItem(Item):
    """
    "Aged Brie"的品质`Quality`会随着时间推移而提高
    """

    def __init__(self, sellin, quality=Item.MAX_QUALITY):
        super(AgedBrieItem, self).__init__(sellin, quality)
        self.name = ITEM_NAMES['aged_brie']

    def update_quality(self):
        if self.quality == self.MAX_QUALITY:
            return
        self.quality += 1
        self._correct_max_quality()

    def _correct_max_quality(self):
        self.quality = self.MAX_QUALITY if self.quality > self.MAX_QUALITY else self.quality


class BackstagePassesItem(AgedBrieItem):
    """
    "Backstage passes"与aged brie类似，其品质`Quality`会随着时间推移而提高；
    - 当还剩10天或更少的时候，品质`Quality`每天提高2；
    - 当还剩5天或更少的时候，品质`Quality`每天提高3；
    - 但一旦过期，品质就会降为0
    """

    def __init__(self, sellin, quality=Item.MAX_QUALITY):
        super(BackstagePassesItem, self).__init__(sellin, quality)
        self.name = ITEM_NAMES['backstage_passes']

    def update_quality(self):
        if self.is_expired():
            self.quality = 0
            return

        if self.sellin <= 5:
            self.quality += 3
            self._correct_max_quality()
            return
        if self.sellin <= 10:
            self.quality += 2
            self._correct_max_quality()
            return

        super(BackstagePassesItem, self).update_quality()


class SulfurasItem(Item):
    """
    传奇物品"Sulfuras"永不到期，也不会降低品质`Quality`
    """

    MAX_QUALITY = 80

    def __init__(self, sellin, quality=MAX_QUALITY):
        super(SulfurasItem, self).__init__(999999, quality)
        self.name = ITEM_NAMES['sulfuras']

    def update_quality(self):
        pass

    def decr_sellin(self):
        pass


class ConjuredItem(Item):
    """
    "Conjured"物品的品质`Quality`下降速度比正常物品快一倍
    """

    def __init__(self, sellin, quality=Item.MAX_QUALITY):
        super(ConjuredItem, self).__init__(sellin, quality)
        self.name = ITEM_NAMES['conjured']

    def update_quality(self):
        if self.quality == 0:
            return

        if self.is_expired():    # expired
            self.quality -= 2 * 2
        else:
            self.quality -= 1 * 2

        self._correct_min_quality()


class ItemFactory(object):

    @staticmethod
    def init_items(items_data):
        items = []
        items.append(Item(30, 50))
        items.append(AgedBrieItem(30, 50))
        items.append(BackstagePassesItem(30, 50))
        items.append(SulfurasItem(30, 50))
        items.append(ConjuredItem(30, 50))
        return items


class Store:

    def __init__(self, *args, **kwargs):
        self.items = ItemFactory.init_items()

    def next_day(self):
        """
        结束一天， 降低物品的sellin和quality值
        :return:
        """
        for item in self.items:
            item.update_both()

    def after_many_days(self, days):
        """ 结束多天 """
        for i in range(days):
            self.next_day()


