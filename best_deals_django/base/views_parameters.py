from drf_yasg import openapi


PLATFORM_PARAM = openapi.Parameter('platform', openapi.IN_QUERY, description="filter by platform (jumia or souq)", type=openapi.TYPE_STRING)
BRAND_PARAM = openapi.Parameter('brand', openapi.IN_QUERY, description="filter by brand", type=openapi.TYPE_STRING)
SEARCH_PARAM = openapi.Parameter('search', openapi.IN_QUERY, description="search the description of the products", type=openapi.TYPE_STRING)
MAX_PRICE_PARAM = openapi.Parameter('max_price', openapi.IN_QUERY, description="excludes products that has prices above this number", type=openapi.TYPE_NUMBER)
MIN_PRICE_PARAM = openapi.Parameter('min_price', openapi.IN_QUERY, description="excludes products that has prices below this number", type=openapi.TYPE_NUMBER)
SORT_PARAM = openapi.Parameter('sort', openapi.IN_QUERY, description="sorts products either ascending or descending based on prices, accepts 'a' or 'd'", type=openapi.TYPE_STRING)

PARAM_LIST = [
    PLATFORM_PARAM,
    BRAND_PARAM,
    SEARCH_PARAM,
    MAX_PRICE_PARAM,
    MIN_PRICE_PARAM,
    SORT_PARAM,
]
