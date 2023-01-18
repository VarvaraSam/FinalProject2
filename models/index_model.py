import pandas

def get_plan(conn,year):

    C = pandas.read_sql(
    '''
    SELECT product_name AS Продукт, product_amount AS Количество FROM product_has_plan
    JOIN plan USING(plan_id)
    JOIN product USING(product_id)
    WHERE year = :year
    ''', conn, params={"year": year})
    return C