class InventoryAllocator:
    """
    Given and order and inventory across a set of warehouses,
    produce the cheapest shipment of the order.

    Attributes
    ----------
    order: dict { string: int }
        A map of item names to how many of them are ordered
    warehouses: list [ Warehouse ]
        A list of Warehouse objects with name and inventory

    Methods
    -------
    allocate_inventory() -> list
        Produces the cheapest shipment

    """
    def __init__(self, order, warehouses):
        """
        order: dict { string: int }
            A map of item names to how many of them are ordered
        warehouses: list [ dict { "name": string, "inventory": dict { string: int } } ]
            A list of objects with warehouse name and inventory amounts for items
        """
        self._order = order.copy()
        self._warehouses = []
        for warehouse_dict in warehouses:
            self._warehouses.append(Warehouse(warehouse_dict))

    def allocate_inventory(self):
        """
        Core function, allocate inventory according to warehouses information
        to fufill the order in the cheapest way

        Parameters
        ----------
        order: dict { string: int }
            A map of item names to how many of them are ordered
        warehouses: list [ Warehouse ]
            A list of Warehouse objects with name and inventory

        Returns
        -------
        shipment: list [ dict { string: dict { string: int } } ]
            A list of which and how many item each warehouses provide to fufill
            the order in the cheapest way
        """

        # Store the required number of each item, number must > 0
        checklist = {}
        for required_item in self._order:
            if self._order[required_item] > 0:
                checklist[required_item] = self._order[required_item]

        shipment = [] # The output list, the cheapest possible shipment

        # Start from the cheapest and traverse warehouses to fufil the checklist
        for warehouse in self._warehouses:

            # Items provided from the inventory of a certain warehouse
            items_from_a_warehouse = {}

            # Check which and how many items in the checklist the warehouse can provide
            for required_item in list(checklist.keys()):
                if required_item in warehouse.inventory:
                    required_item_num = checklist[required_item]
                    stock_item_num = warehouse.inventory[required_item]
                    if stock_item_num == 0:
                        continue
                    if required_item_num > stock_item_num:
                        items_from_a_warehouse[required_item] = stock_item_num
                        checklist[required_item] -= stock_item_num
                    else:
                        items_from_a_warehouse[required_item] = required_item_num
                        del checklist[required_item]

            # If the warehouse do provide some items, add it into shipment
            if len(items_from_a_warehouse) != 0:
                shipment.append({warehouse.name: items_from_a_warehouse})

            # If there's no more item in checklist, the order is already fufilled
            if len(checklist) == 0:
                break

        # If there's still item in checklist, there's not enough inventory
        # No allocations should be returned
        if len(checklist) > 0:
            shipment = []
        return shipment

class Warehouse:
    """
    A warehouse with name and inventory

    Attributes
    ----------
    name: string
        warehouse name
    inventory: dict { string: int } }
        A map of item names to how many of them are in the inventory
    """
    def __init__(self, warehouse_dict):
        self.name = warehouse_dict["name"]
        self.inventory = warehouse_dict["inventory"].copy()
