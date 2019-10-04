import unittest
from inventory_allocator import InventoryAllocator

class TestInventoryAllocator(unittest.TestCase):

    def setUp(self):
        self.warehouse_pool = [
            {
            "name": "w1",
            "inventory": {}
            },
            {
            "name": "w2",
            "inventory": {
                "apple": 1,
                "banana": 1,
                "orange": 1,
                }
            },
            {
            "name": "w3",
            "inventory": {
                "apple": 5,
                "orange": 5,
                }
            },
            {
            "name": "w4",
            "inventory": {
                "apple": 0,
                "banana": 5,
                }
            },
        ]


    def select_warehouses(self, warehouses_list):
        """
        Parameters
        ----------
        warehouses_list: list [ int ]
            a list of index ordering from lower shipping cost to higher to
            select warehouse from self.warehouse_pool

        Returns
        -------
        warehouses: list [ dict { "name": string, "inventory": dict { string: int } } ]
            A list of objects with warehouse name and inventory amounts for items
        """
        warehouses = []
        for index in warehouses_list:
            warehouses.append(self.warehouse_pool[index])
        return warehouses

    ### Tests for empty order###

    def test_no_order_no_warehouse(self):
        order = {}
        warehouses = self.select_warehouses([])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected, "No order, no warehouse")

    def test_no_order_empty_inventory(self):
        order = {}
        warehouses = self.select_warehouses([0])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected, "No order, empty inventory")

    def test_no_order_exist_inventory(self):
        order = {}
        warehouses = self.select_warehouses([1])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected, "No order, but exist inventory")

    def test_order_with_zero_number(self):
        order = {"apple": 0, "banana": 0}
        warehouses = self.select_warehouses([0, 1, 2, 3])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected, "Order with zero item number")

    ### Tests for one item in the order, enough inventory ###

    def test_one_item_one_warehouse(self):
        order = {"apple": 4}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = [
            {"w3": {"apple": 4}},
        ]
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "One item in the order, fufilled by one warehouse")

    def test_one_item_exact_one_warehouse(self):
        order = {"apple": 5}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = [
            {"w3": {"apple": 5}},
        ]
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "One item in the order, exactly fufilled by one warehouse")

    def test_one_item_multiple_warehouses(self):
        order = {"apple": 6}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = [
            {"w3": {"apple": 5}},
            {"w2": {"apple": 1}},
        ]
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertCountEqual(shipment, expected,
            "One item in the order, fufilled by multiple warehouse")

    ### Tests for one item, not in inventory or not enough ###

    def test_one_item_no_warehouse(self):
        order = {"apple": 5}
        warehouses = self.select_warehouses([])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "One item in the order, but there's no warehouse")

    def test_one_item_empty_inventory(self):
        order = {"apple": 5}
        warehouses = self.select_warehouses([0])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "One item in the order, but inventory is empty")

    def test_one_item_not_in_inventory(self):
        order = {"kiwi": 5}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "One item in the order, not in inventory")

    def test_one_item_not_enough_inventory(self):
        order = {"apple": 15}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "One item in the order, not enough stock in inventory")

    ### Tests for multiple items, enough inventory ###

    def test_multiple_items_one_warehouse(self):
        order = {"apple": 5, "orange": 3}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = [
            {"w3": {"apple": 5, "orange": 3}},
        ]
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, fufilled by one warehouse")

    def test_multiple_items_multiple_warehouses_permutation1(self):
        order = {"apple": 5, "banana": 5, "orange":3}
        warehouses = self.select_warehouses([3, 2, 1, 0])
        expected = [
            {"w3": {"apple": 5, "orange": 3}},
            {"w4": {"banana": 5}},
        ]
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertCountEqual(shipment, expected,
            "Multiple items in the order, fufilled by multiple warehouses")

    def test_multiple_items_multiple_warehouses_permutation2(self):
        order = {"apple": 5, "banana": 5, "orange":3}
        warehouses = self.select_warehouses([0, 1, 2, 3])
        expected = [
            {'w2': {'apple': 1, 'banana': 1, 'orange': 1}},
            {'w3': {'apple': 4, 'orange': 2}},
            {'w4': {'banana': 4}},
        ]
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertCountEqual(shipment, expected,
            "Multiple items in the order, fufilled by multiple warehouses")

    ### Tests for multiple items, some of not in inventory or not enough ###

    def test_multiple_items_no_warehouse(self):
        order = {"apple": 5, "banana": 5, "orange":3}
        warehouses = self.select_warehouses([])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, but there's no warehouse")

    def test_multiple_items_empty_inventory(self):
        order = {"apple": 5, "banana": 5, "orange":3}
        warehouses = self.select_warehouses([0])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, but inventory is empty")

    def test_multiple_items_one_not_in_inventory(self):
        order = {"apple": 5, "banana": 5, "orange":3, "kiwi": 1}
        warehouses = self.select_warehouses([0, 1, 2, 3])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, but one item is not in inventory")

    def test_multiple_items_some_not_in_inventory(self):
        order = {"apple": 5, "banana": 5, "peach":3, "kiwi": 1}
        warehouses = self.select_warehouses([0, 1, 2, 3])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, but some items is not in inventory")

    def test_multiple_items_one_not_enough_inventory(self):
        order = {"apple": 15, "banana": 5, "orange":3,}
        warehouses = self.select_warehouses([0, 1, 2, 3])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, but one item is not enough in inventory")

    def test_multiple_items_some_not_enough_inventory(self):
        order = {"apple": 15, "banana": 15, "orange":3,}
        warehouses = self.select_warehouses([0, 1, 2, 3])
        expected = []
        inventory_allocator = InventoryAllocator(order, warehouses)
        shipment = inventory_allocator.allocate_inventory()
        self.assertEqual(shipment, expected,
            "Multiple items in the order, but somes items are not enough in inventory")

if __name__ == '__main__':
    unittest.main()
