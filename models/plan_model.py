import pandas

def get_products(conn,year):

    products_in_plan = pandas.read_sql(
    f'''
    SELECT product_id FROM product_has_plan
    JOIN plan USING(plan_id)
    WHERE year = {year}
    ''', conn)
    products=[]
    for n in range(len(products_in_plan)):
        products.append(products_in_plan.values[n][0])
    if len(products) == 1:
        C = pandas.read_sql(
            f'''
        SELECT product_name AS Продукт FROM product
        WHERE product_id != {products[0]}
        ''', conn)
    else:
        C = pandas.read_sql(
        f'''
        SELECT product_name AS Продукт FROM product
        WHERE product_id NOT IN {tuple(products)}
        ''', conn)

    return C

def get_plan(conn,year):

    C = pandas.read_sql(
    '''
    SELECT product_name AS Продукт, product_amount AS Количество FROM product_has_plan
    JOIN plan USING(plan_id)
    JOIN product USING(product_id)
    WHERE year = :year
    ''', conn, params={"year": year})
    return C

def insert_plan(conn,tempprod,tempamount,year):
    cur = conn.cursor()
    tempprod = pandas.read_sql(
        f'''
        SELECT product_name
        FROM product
        WHERE product_name LIKE '{tempprod}%'
        ''', conn).values[0][0]
    product_id = pandas.read_sql(
        '''
        SELECT product_id
        FROM product
        WHERE product_name = :name
        ''', conn, params={"name": tempprod})

    product_id = product_id.values[0][0]
    plan_id = pandas.read_sql(
        '''
        SELECT plan_id
        FROM plan
        WHERE year = :year
        ''', conn, params={"year": year})

    if (plan_id.empty):
        cur.executescript(f'''
            INSERT INTO plan(year)
            VALUES({year})
        ''')
        conn.commit()
        plan_id = pandas.read_sql(
            '''
            SELECT plan_id
            FROM plan
            WHERE year = :year
            ''', conn, params={"year": year})
    plan_id = plan_id.values[0][0]
    cur.executescript(f'''
        INSERT INTO product_has_plan (product_id,plan_id,product_amount)
        VALUES({product_id},{plan_id},{tempamount})
    ''')
    return conn.commit()

def del_line_plan(conn,year,product):
    cur = conn.cursor()
    product = pandas.read_sql(
        f'''
        SELECT product_name
        FROM product
        WHERE product_name LIKE '{product}%'
        ''', conn).values[0][0]
    product_id = pandas.read_sql(
        '''
        SELECT product_id
        FROM product
        WHERE product_name = :name
        ''', conn, params={"name": product}).values[0][0]
    plan_id = pandas.read_sql(
        '''
        SELECT plan_id
        FROM plan
        WHERE year = :year
        ''', conn, params={"year": year})
    if (plan_id.empty):
        cur.executescript(f'''
            INSERT INTO plan(year)
            VALUES({year})
        ''')
        conn.commit()
        plan_id = pandas.read_sql(
            '''
            SELECT plan_id
            FROM plan
            WHERE year = :year
            ''', conn, params={"year": year})
    plan_id = plan_id.values[0][0]
    cur.executescript(
    f'''
    DELETE FROM product_has_plan 
    WHERE plan_id = {plan_id} AND product_id = {product_id}
    ''')
    return conn.commit()
