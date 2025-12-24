# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class ItemUpdater(ABC):
    """Abstract base class for all item update strategies."""

    @abstractmethod
    def update(self, item):
        """Update the given item's sell_in and quality based on its type rules."""
        pass

class QualityHelper:
    """Shared helper for quality adjustments."""

    @staticmethod
    def increase_quality(item):
        if item.quality < 50:
            item.quality += 1

    @staticmethod
    def decrease_quality(item):
        if item.quality > 0:
            item.quality -= 1

class NormalItemUpdater(ItemUpdater):
    """Updates normal items:
    - Quality decreases by 1 each day before sell_in date.
    - Quality decreases by 2 each day after sell_in date has passed.
    - Quality never goes below 0.
    """
    def update(self, item):
        item.sell_in -= 1
        QualityHelper.decrease_quality(item)
        if item.sell_in < 0:
            QualityHelper.decrease_quality(item)


class AgedBrieUpdater(ItemUpdater):
    """Updates 'Aged Brie':
    - Quality increases by 1 each day before sell_in date.
    - Quality increases by 2 each day after sell_in date has passed.
    - Quality never exceeds 50.
    """
    def update(self, item):
        item.sell_in -= 1
        QualityHelper.increase_quality(item)
        if item.sell_in < 0:
            QualityHelper.increase_quality(item)


class BackstagePassUpdater(ItemUpdater):
    """Updates 'Backstage passes':
    - Quality increases by 1 each day normally.
    - Additional +1 if 10 days or fewer remain.
    - Additional +1 if 5 days or fewer remain.
    - Quality drops to 0 after the concert date.
    - Quality never exceeds 50.
    """
    def update(self, item):
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = 0
            return
        QualityHelper.increase_quality(item)
        if item.sell_in < 10:
            QualityHelper.increase_quality(item)
        if item.sell_in < 5:
            QualityHelper.increase_quality(item)


class SulfurasUpdater(ItemUpdater):
    """Updates 'Sulfuras, Hand of Ragnaros':
    - Legendary item; quality and sell_in never change.
    """
    def update(self, item):
        # Legendary item does not change quality or sell_in
        pass


class ConjuredItemUpdater(ItemUpdater):
    """Updates 'Conjured' items:
    - Quality decreases twice as fast as normal items:
      * -2 each day before sell_in date.
      * -4 each day after sell_in date has passed.
    - Quality never goes below 0.
    """
    def update(self, item):
        item.sell_in -= 1
        QualityHelper.decrease_quality(item)
        QualityHelper.decrease_quality(item)
        if item.sell_in < 0:
            QualityHelper.decrease_quality(item)
            QualityHelper.decrease_quality(item)


class ItemUpdaterFactory:
    """Factory that returns the correct ItemUpdater based on the item name."""

    @staticmethod
    def get_updater(item):
        if item.name == "Aged Brie":
            return AgedBrieUpdater()
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassUpdater()
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdater()
        elif item.name.lower().startswith("conjured"):
            return ConjuredItemUpdater()
        else:
            return NormalItemUpdater()


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """
        Delegates item updates to the appropriate ItemUpdater returned by ItemUpdaterFactory.
        """
        for item in self.items:
            updater = ItemUpdaterFactory.get_updater(item)
            updater.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
