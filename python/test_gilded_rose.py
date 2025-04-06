# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_normal_item_before_sell_date(self):
        items = [Item("Normal Item", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)

    def test_normal_item_after_sell_date(self):
        items = [Item("Normal Item", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(8, items[0].quality)

    def test_normal_item_quality_never_negative(self):
        items = [Item("Normal Item", 5, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    # Aged Brie
    def test_aged_brie_before_sell_date(self):
        items = [Item("Aged Brie", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(11, items[0].quality)

    def test_aged_brie_after_sell_date(self):
        items = [Item("Aged Brie", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(12, items[0].quality)

    def test_aged_brie_quality_never_exceeds_50(self):
        items = [Item("Aged Brie", 5, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(50, items[0].quality)

    # Sulfuras
    def test_sulfuras_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(5, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_after_sell_date(self):
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    # Backstage Passes
    def test_backstage_pass_more_than_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(14, items[0].sell_in)
        self.assertEqual(11, items[0].quality)

    def test_backstage_pass_10_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(12, items[0].quality)

    def test_backstage_pass_5_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(13, items[0].quality)

    def test_backstage_pass_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)


    # Edge Cases
    def test_unknown_item_type(self):
        items = [Item("Random Junk", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)

    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    # Conjured Items
    def test_conjured_item_quality_decreases_twice_as_fast(self):
        items = [Item("Conjured Mana Cake", 10, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(18, items[0].quality)

    def test_conjured_item_quality_decreases_twice_as_fast_after_sell_by(self):
        items = [Item("Conjured Mana Cake", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(16, items[0].quality)

    def test_conjured_item_quality_never_negative(self):
        items = [Item("Conjured Mana Cake", 5, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    # Add these test cases to enforce quality bounds

    def test_legendary_item_quality_enforced_on_creation(self):
        """Test that Sulfuras quality is automatically set to 80 if initialized with wrong value"""
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 50)]  # Incorrect quality
        gilded_rose = GildedRose(items)
        self.assertEqual(80, items[0].quality)  # Should be corrected to 80

    def test_normal_item_quality_clamped_on_creation(self):
        """Test that normal items' quality is clamped to 0-50 range during initialization"""
        items = [Item("Normal Item", 5, 60)]  # Above max
        gilded_rose = GildedRose(items)
        self.assertEqual(50, items[0].quality)

        items = [Item("Normal Item", 5, -5)]  # Below min
        gilded_rose = GildedRose(items)
        self.assertEqual(0, items[0].quality)

    def test_legendary_item_quality_unchanged_by_updates(self):
        """Test that Sulfuras quality remains 80 even after multiple updates"""
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gilded_rose = GildedRose(items)
        for _ in range(5):  # Multiple updates
            gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(5, items[0].sell_in)  # Sell_in should not change

    def test_backstage_pass_quality_clamped_on_creation(self):
        """Test that backstage pass quality is clamped to 0-50 during initialization"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 60)]
        gilded_rose = GildedRose(items)
        self.assertEqual(50, items[0].quality)

    def test_conjured_item_quality_clamped_on_creation(self):
        """Test that conjured items' quality is clamped to 0-50 during initialization"""
        items = [Item("Conjured Mana Cake", 5, 60)]
        gilded_rose = GildedRose(items)
        self.assertEqual(50, items[0].quality)

        items = [Item("Conjured Mana Cake", 5, -10)]
        gilded_rose = GildedRose(items)
        self.assertEqual(0, items[0].quality)

    def test_aged_brie_quality_clamped_on_creation(self):
        """Test that Aged Brie quality is clamped to 0-50 during initialization"""
        items = [Item("Aged Brie", 5, 60)]
        gilded_rose = GildedRose(items)
        self.assertEqual(50, items[0].quality)






if __name__ == '__main__':
    unittest.main()