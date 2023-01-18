from app import app
import datetime
from flask import render_template, request
from utils import get_db_connection
from models.farm_model import get_tasks,get_farms,get_t,del_tasks
@app.route('/farm', methods=['get'])
def farm():
   now = datetime.datetime.now()
   year = now.year
   conn = get_db_connection()
   if request.values.get('year'):
      year = int(request.values.get('year'))
      if year> now.year:
         del_tasks(conn,year)
   get_t(conn,year)
   tasks = get_tasks(conn,year)
   farm=get_farms(conn,year)
   html = render_template(
   'farm.html',
   year = year,
   farm=farm,
   tasks = tasks,
   len = len
   )
   return html