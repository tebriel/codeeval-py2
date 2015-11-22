"""
Calculates the sum of the SS Discount Offer Score
"""
import sys
import re

VOWELS = '[aeiouy]'
CONSONANTS = '[bcdfghjklmnpqrstvwxz]'


def determine_factors(num):
    """
    Determines the factors of a number
    >>> determine_factors(20)
    set([2, 10, 4, 5])
    >>> determine_factors(7)
    set([])
    >>> determine_factors(14)
    set([2, 7])
    """
    possibles = range(2, num)
    results = set()
    for possible in possibles:
        if num % possible == 0:
            results.add(possible)
    return results


def count_letters(word):
    """
    Counts the number of letters in a word
    >>> count_letters("Jack Abraham")
    11
    >>> count_letters("Jeffery Lebowski")
    15
    >>> count_letters("iPad 2 - 4-pack")
    8
    """
    word = word.lower()
    consonants = len(re.findall(CONSONANTS, word))
    vowels = len(re.findall(VOWELS, word))
    return consonants + vowels


def has_factor_modifier(customer, product_factors):
    """
    Determines if there's an intersection in factors between customer
    and product
    >>> has_factor_modifier("Jeffery Lebowski", set([5]))
    True
    >>> has_factor_modifier("Jack Abraham", set([2,3]))
    False
    """
    customer_length = count_letters(customer)
    customer_factors = determine_factors(customer_length)
    return len(customer_factors.intersection(product_factors)) > 0


def even_product_score(scores, customer, product):
    """
    Calculates the score when the product has an even number of letters
    """
    customer = customer.lower()
    score = len(re.findall(VOWELS, customer)) * 1.5
    scores[customer][product] = score

    return score


def odd_product_score(scores, customer, product):
    """
    Calculates the score when the product has an even number of letters
    """
    customer = customer.lower()
    score = len(re.findall(CONSONANTS, customer))
    scores[customer][product] = score * 1.00

    return score


def determine_total_score(scores):
    """
    Determine the best product per customer
    """
    total = 0
    score_sets = []
    cost_matrix = []

    for customer, products in scores.iteritems():
        score_sets.append(products.values())

    for row in score_sets:
        cost_row = []
        for column in row:
            # Negate all to fit into the typical minimum-cost style of the
            # assignment problem
            cost_row.append(-column)
        cost_matrix.append(cost_row)

    m = Munkres()
    indexes = m.compute(cost_matrix)
    total = 0
    for row, column in indexes:
        value = score_sets[row][column]
        total += value

    return total


def discount_offer(line):
    (customers, products) = line.split(';')
    if len(customers) == 0 or len(products) == 0:
        return 0.0
    customers = [customer.lower() for customer in customers.split(',')]
    products = [product.lower() for product in products.split(',')]
    scores = dict()
    # calculate rule 1
    for product in products:
        letter_count = count_letters(product)
        product_factors = determine_factors(letter_count)
        if letter_count % 2 == 0:
            # vowels in customer's name * 1.5
            for customer in customers:
                if scores.get(customer) is None:
                    scores[customer] = dict()
                even_product_score(scores, customer, product)
                if has_factor_modifier(customer, product_factors):
                    print scores[customer][product] * 1.5
                    scores[customer][product] *= 1.5
        else:
            # consonants in customer's name
            for customer in customers:
                if scores.get(customer) is None:
                    scores[customer] = dict()
                odd_product_score(scores, customer, product)
                if has_factor_modifier(customer, product_factors):
                    print scores[customer][product] * 1.5
                    scores[customer][product] *= 1.5

    return determine_total_score(scores)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        lines = None
        with open(sys.argv[1], 'r') as f:
            for line in f.readlines():
                print "%.2f" % discount_offer(line.rstrip('\n'))
    else:
        import doctest
        doctest.testmod()
