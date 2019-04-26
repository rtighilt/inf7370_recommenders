from ProductsWorker import ProductsWorker
from BasketsWorker import BasketsWorker
from Helpers import PRODUCT_SHAPE, BASKET_SHAPE, LEVEL_OF_SIMILARITY, permutations
import itertools


def products_process():
    p = ProductsWorker("../Data/product.csv", PRODUCT_SHAPE)
    t = p.get_tree()
    return p, t


def basket_process():
    return BasketsWorker("../Data/transaction_data.csv", BASKET_SHAPE)


def get_common_path(src, dest):
    source_path = str(src.path[-1]).split("('")[1].split("')")[0]
    dest_path = str(dest.path[-1]).split("('")[1].split("')")[0]
    common_path = ""
    for i in range(0, len(source_path)):
        if dest_path[i] != source_path[i]:
            common_path = source_path[:i]
            break
    return common_path


def calculate_similarity(source_node, dest_node, level):
    common_path = get_common_path(source_node, dest_node)
    length_of_path = common_path.count("/") - 1
    return length_of_path / level


def similarity_from_tuple(t):
    print("Getting similarity for tuple " + str(t))
    return calculate_similarity(products.get_node(t[0]), products.get_node(t[0]), LEVEL_OF_SIMILARITY)


products, tree = products_process()
baskets = basket_process()
# Getting baskets dictionnary
basket_dict = baskets.get_data_dict()
# Choosing a random element from basket dictionnary and remove it from there
rand_basket = basket_dict.popitem()[1]

print("Getting combinations for all baskets :")
print("======================================")


for basket_id, value in basket_dict.items():
    perms = permutations(rand_basket, value)
    compatibility = 0
    print("Calculating for basket " + str(basket_id))
    agg_sim = map(similarity_from_tuple, perms)
    print(list(agg_sim))
    #     print(perm[0] + " - " + perm[1])
    #     compatibility += calculate_similarity(products.get_node(perm[0]), products.get_node(perm[1]), LEVEL_OF_SIMILARITY)
    # print(compatibility)
    # break
# def calculate_product_similarity_with_basket(product, basket):
#     sum = 0
#     for p in basket:
#         similarity = calculate_similarity(product, products.get_node(p), LEVEL_OF_SIMILARITY)
#         sum += similarity
#         print("Product " + product.name + " with product : " + p + " is : " + str(similarity))
#     return sum
#
#

#
#
# print(permutations([1,2,3,4], [5,6,7,8]))
# # source = products.get_node("26636")
# # dest = products.get_node("26601")
#
# # print(calculate_similarity(source, dest, 6))
