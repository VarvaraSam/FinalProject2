import pandas
import datetime
def get_t(conn,year):
    plan = pandas.read_sql(
        f'''
        SELECT * FROM task_for_farm
        WHERE year = {year}
        ''', conn)
    print (plan)

def task_for_farm(conn,cultivated_areas_amount,year,farm_has_product):
    cur = conn.cursor()
    cur.executescript(f'''
           INSERT INTO task_for_farm (cultivated_areas_amount,year,farm_has_product_id)
            VALUES({cultivated_areas_amount},{year},{farm_has_product})
       ''')
    return conn.commit()
def calc_tasks(conn,year):
    farm_areas=dict()
    farm_has_product =[]
    cultivated_areas_amount =[]
    plan = pandas.read_sql(
        f'''
        SELECT product_id, product_amount FROM plan
        JOIN product_has_plan USING(plan_id)
        JOIN product USING(product_id)
        WHERE year = {year}
        ''', conn)
    for n in range(len(plan)):
        farm_for_product = pandas.read_sql(
        f'''
        SELECT farm_id,farm_has_product_id FROM farm_has_product
        WHERE product_id = {plan.values[n][0]}
        ''', conn)
        areas =  plan.values[n][1]
        for k in range(len(farm_for_product)):
            farm_areas_for_product = pandas.read_sql(
            f'''
            SELECT free_cultivated_areas,farm_id FROM farm
            WHERE farm_id = {farm_for_product.values[k][0]}
            ''', conn)

            task = 0
            if farm_areas_for_product.values[0][1] in farm_areas:
                if farm_areas[farm_areas_for_product.values[0][1]] - areas >= 0:
                    farm_areas[farm_areas_for_product.values[0][1]] = farm_areas[farm_areas_for_product.values[0][1]] - areas
                    task = areas
                    areas = 0
                else:
                    areas = areas - farm_areas[farm_areas_for_product.values[0][1]]
                    task = farm_areas[farm_areas_for_product.values[0][1]]
                    farm_areas[farm_areas_for_product.values[0][1]] = 0
            else:
                farm_areas[farm_areas_for_product.values[0][1]] = farm_areas_for_product.values[0][0]
                if farm_areas[farm_areas_for_product.values[0][1]] - areas >= 0:
                    farm_areas[farm_areas_for_product.values[0][1]] = farm_areas[farm_areas_for_product.values[0][1]] - areas
                    task = areas
                    areas = 0
                else:
                    areas = areas - farm_areas[farm_areas_for_product.values[0][1]]
                    task = farm_areas[farm_areas_for_product.values[0][1]]
                    farm_areas[farm_areas_for_product.values[0][1]] = 0
            farm_has_product.append(farm_for_product.values[k][1])
            cultivated_areas_amount.append(task)
        #print(farm_areas)
        if areas != 0:
            return "Невозможно выполнить план, недостаточно ферм"
    for i in range(len(farm_has_product)):
        if cultivated_areas_amount[i] != 0:
            task_for_farm(conn,cultivated_areas_amount[i],year,farm_has_product[i])
    return get_tasks(conn,year)

def del_tasks(conn,year):
    cur = conn.cursor()
    cur.executescript(
        f'''
       DELETE FROM task_for_farm 
       WHERE year = {year} 
       ''')
    return conn.commit()
def get_tasks(conn,year):
    # now = datetime.datetime.now()
    # nowyear = now.year
    plan_id = pandas.read_sql(
        '''
        SELECT plan_id
        FROM plan
        WHERE year = :year
        ''', conn, params={"year": year})
    if (plan_id.empty):
        return plan_id
    else:

        pr = pandas.read_sql(
            '''
            SELECT product_has_plan_id
            FROM product_has_plan
            JOIN plan USING(plan_id)
            WHERE year = :year
            ''', conn, params={"year": year})
        if (pr.empty):
            return pr
        else:

            C = pandas.read_sql(
            '''
            SELECT cultivated_areas_amount, product_name, farm_name FROM task_for_farm 
            JOIN farm_has_product USING(farm_has_product_id)
            JOIN farm USING(farm_id)
            JOIN product USING(product_id)
            WHERE year = :year
            ''', conn, params={"year": year})
            if C.empty:
                C = calc_tasks(conn,year)
            return C
def get_farms(conn,year):
    C = pandas.read_sql(
    f'''
    SELECT farm_name FROM farm
    JOIN farm_has_product USING(farm_id)
    JOIN task_for_farm USING(farm_has_product_id)
    WHERE year = {year}
    GROUP BY farm_name
    ''', conn)
    return C