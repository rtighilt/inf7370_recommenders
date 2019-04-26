import ntpath
import os

from FileReader import FileReader


class BasketsWorker(FileReader):

    def get_data_dict(self):
        return self.data.groupby('BASKET_ID')['PRODUCT_ID'].apply(list).to_dict()

    @staticmethod
    def intersection(lst1, lst2):
        # Use of hybrid method
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3

    def get_baskets_with_products(self, products):
        print("Getting baskets with specified products")
        baskets = self.get_data_dict()
        return {k: v for k, v in baskets.items() if self.intersection(products, v) is not False}
