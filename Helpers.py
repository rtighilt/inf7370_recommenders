import itertools

PRODUCT_SHAPE = ['DEPARTMENT','COMMODITY_DESC','SUB_COMMODITY_DESC','CURR_SIZE_OF_PRODUCT', 'BRAND', 'PRODUCT_ID']
BASKET_SHAPE = ['BASKET_ID', 'PRODUCT_ID']
LEVEL_OF_SIMILARITY = 3


def permutations(lst1, lst2):
    list3 = [zip(x, lst2) for x in itertools.permutations(lst1, len(lst2))]
    chain = itertools.chain(*list3)
    list4 = list(chain)
    return list4
