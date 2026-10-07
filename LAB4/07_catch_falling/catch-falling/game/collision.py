"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    x_overlap = basket_rect.left <= obj.x <= basket_rect.right
    y_overlap = (
        obj.y + obj.radius >= basket_rect.top
        and obj.y - obj.radius <= basket_rect.bottom
    )
    return x_overlap and y_overlap
