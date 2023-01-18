import numpy as np
from app import app
import datetime
from flask import render_template, request
from utils import get_db_connection
from models.plan_model import get_products,insert_plan,get_plan,del_line_plan
@app.route('/plan', methods=['get'])
def plan():
   now = datetime.datetime.now()
   conn = get_db_connection()
   year = now.year
   if request.values.get('addplan'):
      year = int(request.values.get('addplan'))
   elif request.values.get('changeplan'):
      year = int(request.values.get('changeplan'))
   elif request.values.get('localyear'):
      year = int(request.values.get('localyear'))
      if request.values.get('tempamount'):
         if int(request.values.get('tempamount'))>0:
            insert_plan(conn,request.values.get('tempproduct'),request.values.get('tempamount'),year)
   elif request.values.get('delete'):
      year = int(request.values.get('delyear'))
      product = request.values.get('delete')
      del_line_plan(conn,year,product)

   df_products = get_products(conn,year)
   df_plan = get_plan(conn,year)
   df_plan[""]=np.nan

   html = render_template(
   'plan.html',
   year = year,
   plan=df_plan,
   products = df_products,
   len = len
   )
   return html