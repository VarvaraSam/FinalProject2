import datetime
from app import app
from flask import render_template, request
from utils import get_db_connection
from models.index_model import get_plan
@app.route('/', methods=['get'])
def index():
   now = datetime.datetime.now()
   year = now.year
   conn = get_db_connection()
   if request.values.get('year'):
      year = int(request.values.get('year'))
   df_planByYear = get_plan(conn, year)

   html = render_template(
   'index.html',
   year = year,
   nowyear = now.year,
   plan = df_planByYear,
   len = len
   )
   return html