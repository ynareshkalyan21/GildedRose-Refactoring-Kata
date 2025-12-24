# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_normal_item_before_sell_date(self):
        #1.Once the sell by date has passed, Quality degrades twice as fast
        item = Item("Normal Item", 10, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(9, item.sell_in)
        self.assertEqual(19, item.quality)

    def test_normal_item_on_sell_date(self):
        item = Item("Normal Item", 0, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(18, item.quality)

    def test_normal_item_after_sell_date(self):
        item = Item("Normal Item", -1, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(-2, item.sell_in)
        self.assertEqual(18, item.quality)

    def test_quality_never_negative(self):
        #2. The Quality of an item is never negative
        item = Item("Normal Item", 5, 0)
        GildedRose([item]).update_quality()
        self.assertEqual(0, item.quality)

    def test_aged_brie_increases_in_quality(self):
        #3."Aged Brie" actually increases in Quality the older it gets
        item = Item("Aged Brie", 5, 10)
        GildedRose([item]).update_quality()
        self.assertEqual(11, item.quality)

    def test_quality_never_exceeds_50(self):
        #4. The Quality of an item is never more than 50
        item = Item("Aged Brie", 5, 50)
        GildedRose([item]).update_quality()
        self.assertEqual(50, item.quality)

    def test_sulfuras_never_changes(self):
        #5. "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
        item = Item("Sulfuras, Hand of Ragnaros", 0, 80)
        GildedRose([item]).update_quality()
        self.assertEqual(0, item.sell_in)
        self.assertEqual(80, item.quality)

    def test_backstage_passes_before_sell_date(self):
        #6.0 "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches
        item = Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(21, item.quality)

    def test_backstage_passes_within_10_days(self):
        #6.1.1 "Backstage passes":: Quality increases by 2 when there are 10 days
        item = Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(22, item.quality)

    def test_backstage_passes_within_5_days(self):
        #6.1.2 "Backstage passes":: Quality increases by 3 when there are 5 days
        item = Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(23, item.quality)

    def test_backstage_passes_after_concert(self):
        #6.2 "Backstage passes":: Quality drops to 0 after the concert
        item = Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)
        GildedRose([item]).update_quality()
        self.assertEqual(0, item.quality)

        
if __name__ == '__main__':
    unittest.main()
