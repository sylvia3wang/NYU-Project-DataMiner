import json
import datetime
from flask import Flask
from flask import request
from flask import render_template
from coinbase.wallet.client import Client
import mysql.connector as mc
from mysql.connector.conversion import MySQLConverter
from mysql.connector.cursor import MySQLCursor

# app = Flask(__name__,static_url_path="",root_path='./')
app = Flask(__name__)

islogin = False

@app.route('/')
@app.route('/index')
def index():
	context = {
		"isLogin": islogin
	}
	print (islogin)
	return render_template('index.html', **context)

@app.route('/signin')
def signinpage():
	context = {
		"isLogin": islogin
	}
	return render_template('login.html', **context)

@app.route('/api/login', methods=['POST'])
def login():
	user_info = {
		'account': 'admin123@nyu.edu',
		'password': 'ilovecode'
	}
	return_info = {}
	global islogin

	account = request.form['account']
	password = request.form['password']

	if account.lower() == user_info['account'] and password.lower() == user_info['password']:
		return_info['status'] = 0
		return_info['message'] = 'log in success'
		islogin = True
		return json.dumps(return_info)
	else:
		if account.lower() != user_info['account']:
			return_info['status'] = -1
			return_info['message'] = 'log in failed, wrong account'
			return json.dumps(return_info)

		if password.lower() != user_info['password']:
			return_info['status'] = -2
			return_info['message'] = 'log in failed, wrong password'
			return json.dumps(return_info)

@app.route('/signup')
def signuppage():
	context = {
		"isLogin": islogin
	}
	return render_template('signup.html', **context)

@app.route('/pricing')
def pricepage():
	btc_price_int, btc_price_decimal = get_realtime_price('BTC')
	eth_price_int, eth_price_decimal = get_realtime_price('ETH')
	ltc_price_int, ltc_price_decimal = get_realtime_price('LTC')
	cointypes = get_cointypes()
	context = {
		"btc_price_int": btc_price_int,
		"btc_price_decimal": btc_price_decimal,
		"eth_price_int": eth_price_int,
		"eth_price_decimal": eth_price_decimal,
		"ltc_price_int": ltc_price_int,
		"ltc_price_decimal": ltc_price_decimal,
		"cointypes": cointypes,
		"isLogin": islogin
	}
	return render_template('pricing.html', **context)

@app.route('/portfolio')
def transaction():
	transactions = get_transcations()
	id2side = {
		-1:'B',
		1:'S'
	}
	id2coinname = {
		1:'BTC',
		2:'ETH',
		3:'LTC'
	}
	transactions = [list(transaction_row) for transaction_row in transactions]
	for transaction_row in transactions:
		transaction_row[6] = id2side[transaction_row[6]]
		transaction_row[7] = id2coinname[transaction_row[7]]
		transaction_row[3] = transaction_row[3].strftime('%Y-%m-%d %H:%M:%S')

	context = {
		'title':'Transactions',
		'transactions': transactions,
		"isLogin": islogin
	}
	print (transactions)
	return render_template('portfolio.html', **context)

@app.route('/api/currency')
def get_btc_buyprice():
	cointype = request.args.get("cointype", 'BTC')
	client = Client('apibuy', 'secretbuy')
	buy_btc = client.get_buy_price(currency_pair = '{}-USD'.format(cointype))
	print (buy_btc)
	return_json = {
		'amount': float(buy_btc['amount']),
		'base': buy_btc['base'],
		'currency': buy_btc['currency']
	}
	return json.dumps(return_json)

@app.route('/api/buy',methods=['POST'])
def buy():
	connection = get_connection()
	result_json = {}
	cointype_json = {
		"BTC":1,
		"ETH":2,
		"LTC":3
	}
	qty = int(request.form['qty'])
	cointype = request.form['cointype']
	side = request.form['buy_or_sell']

	if qty <= 0 or cointype is None or side is None:
		result_json['status'] = -1
		result_json['message'] = 'Error with input qty or cointype or side'
		return json.dumps(result_json)
	else:
		try:
			realtime_price = get_realtime_price(cointype, float_num=True)
			cur_total_price = realtime_price * 1.0 * qty
			transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			side_num = -1 if side == 'buy' else 1
			flag = 1.0 if side == 'buy' else -1.0

			cointype_num = cointype_json[cointype]

			max_pl_id = get_max_pl_id()
			pl_balance = get_pl_balance(max_pl_id)
			pl_balance = pl_balance - flag * cur_total_price
			if pl_balance < 0:
				result_json['status'] = -4
				result_json['message'] = 'Error: you don\'t have enough money'
				return json.dumps(result_json)

			trade_id_before = get_max_trade_id()
			trade_total_qty = get_trade_total_qty(trade_id_before)
			vwap = get_vwap(max_pl_id)

			vwap = (qty * realtime_price + trade_total_qty * vwap) / (qty + trade_total_qty)
			if 'buy' == side:
				upl = (realtime_price - vwap) * (trade_total_qty + qty)
			else:
				upl = (realtime_price - vwap) * (trade_total_qty - qty)

			if 'buy' == side:
				rpl = 0.0
			else:
				rpl = (realtime_price - vwap) * qty

			trade_total_qty += (flag * qty)

			if trade_total_qty < 0 :
				result_json['status'] = -3
				result_json['message'] = 'Error: you don\'t have enough BTC'
				return json.dumps(result_json)

			total_assets = pl_balance + realtime_price * trade_total_qty
			if trade_id_before is None:
				trade_id = 1
			else:
				trade_id = trade_id_before + 1

			sql = 'insert into trade values({},{}, {}, \'{}\',{},{},{},{})'.format(
				trade_id, qty,realtime_price,transaction_time,trade_total_qty, cur_total_price,side_num, cointype_num )
			sql_pl = 'insert into pl values({}, {}, {}, {}, {},{},{},{})'.format(
				max_pl_id + 1, pl_balance, vwap, upl, rpl, cointype_num , trade_id, total_assets
			)
			connection = get_connection()
			cursor = connection.cursor()
			cursor.execute(sql)
			cursor.execute(sql_pl)

			connection.commit()
			cursor.close()
			connection.close()
			result_json['status'] = 0
			result_json['message'] = 'Sucess!'
		except Exception as e:
			result_json['status'] = -2
			result_json['message'] = 'Error in write data to database'

	return json.dumps(result_json)


@app.route('/api/btc_price')
def get_btc_price():
	result_json = {}
	prices = get_prices()
	prices = [list(price) for price in prices]
	for price in prices:
		price[1] = price[1].strftime('%Y-%m-%d %H:%M:%S')
	prices = list(reversed(prices))
	prices = prices[1:]
	times = [price[1] for price in prices]
	prices = [price[0] for price in prices]

	result_json = {
		"status":0,
		"prices": prices,
		'times': times
	}
	return json.dumps(result_json)

@app.route('/api/upls')
def get_upls():
	result_json = {}
	upls = get_upls()
	upls = [list(price) for price in upls]
	for upl in upls:
		upl[1] = upl[1].strftime('%Y-%m-%d %H:%M:%S')
	upls = list(reversed(upls))
	upls = upls[1:]
	times = [upl[1] for upl in upls]
	upls = [upl[0] for upl in upls]

	result_json = {
		"status":0,
		"upls": upls,
		"times": times
	}
	return json.dumps(result_json)

@app.route('/api/cash_btc')
def get_cash_btc():
	result_json = {}
	cash, total_qty = get_latest_data(get_max_trade_id())
	realtime_price = get_realtime_price('BTC', float_num=True)

	result_json = {
		"status":0,
		"cash": cash,
		"btc": realtime_price * total_qty
	}
	return json.dumps(result_json)

def get_realtime_price(cointype, float_num=False):
	client = Client('apibuy', 'secretbuy')
	buy_btc = client.get_buy_price(currency_pair='{}-USD'.format(cointype))
	if not float_num:
		items = buy_btc['amount'].split('.')
		if len(items) == 2:
			price_int, price_decimal = items
		elif len(items) == 1:
			price_int, price_decimal = items[0], '00'
		else:
			price_int, price_decimal = '0', '00'
		return price_int, price_decimal
	else:
		return float(buy_btc['amount'])

def get_connection():
	return mc.connect(user='root',
	password='MOONmoon.77',
	host='127.0.0.1',
	database='bitcoin',
	auth_plugin='mysql_native_password')

def get_cointypes():
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select symbol_ID, symbol_name from symbol"
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result

def get_pl_balance(max_pl_id):
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select PL_balance from pl WHERE PL_ID={}".format(max_pl_id)
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result[0][0]

def get_vwap(max_pl_id):
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select VWAP from pl WHERE PL_ID={}".format(max_pl_id)
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result[0][0]

def get_max_pl_id():
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select max(PL_ID) from pl"
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result[0][0]

def get_max_trade_id():
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select max(trade_ID) from trade"
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result[0][0]

def get_trade_total_qty(max_trade_id):
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select total_qty from trade WHERE trade_ID={}".format(max_trade_id)
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result[0][0]

def get_transcations():
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select trade.trade_ID, trade_qty, price, time, total_qty, cash, side_side_index, trade.symbol_symbol_ID, PL_balance, VWAP, UPL, RPL, total_assets  " \
				"from trade , pl where trade.trade_ID = pl.trade_id"
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result

def get_prices():
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select price, time from trade ORDER by time DESC limit 20"
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result

def get_upls():
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select pl.UPL, trade.time from trade , pl where trade.trade_ID = pl.trade_id ORDER  by time DESC limit 20"
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result

def get_latest_data(max_trade_id):
	conn = get_connection()
	curr = conn.cursor()
	sql_query = "select pl.PL_balance, total_qty from trade , pl where trade.trade_ID = " + str(max_trade_id) + " and trade.trade_ID = pl.trade_id "
	curr.execute(sql_query)
	result = curr.fetchall()

	conn.close()
	curr.close()
	return result[0][0], result[0][1]

if __name__ == '__main__':
	print(get_latest_data(get_max_trade_id()))
	app.run(debug=True, port=8000)
