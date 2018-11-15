import inspect
import textwrap
from vyper import compiler, optimizer
from vyper.parser.parser import parse_to_lll
from vyper.compile_lll import compile_to_assembly, assembly_to_evm
from web3 import Web3
import json

class Block:
	def __init__(self):
		self.timestamp = None

block = Block()

class message:
	def __init__(self):
		self.sender = None
		self.value = None

msg = message()

__vython_pub_funcs = []
__vython_priv_funcs = []
__vython_const_funcs = []

# For now, prefer no type inference: only allow uint256 to interact with other valid vyper types
class uint256:
	def __init__(self, val=None):
		self.initd = True if val else False
		if val and val >= 0: 
			self.val = val
		elif not val: 
			pass
		else: 
			raise TypeError
		self.public = False
		self.constant = False

	def __add__(self, other):
		if (type(other) is int128 and other.val >= 0) or type(other) is uint256:
			return self.val + other.val
		if (type(other) is int128):
			print("You're trying to add a negative signed int with an unsigned int. No bueno.")
		else:
			print("cannot add uint256 with {}".format(type(other)))
		raise TypeError

# For now, prefer no type inference: only allow int128 to interact with other valid vyper types
class int128:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False

	def __add__(self, other):
		if (type(other) is uint256 and self.val >= 0) or type(other) is int128:
			return self.val + other.val
		if (type(other) is uint256):
			print("You're trying to add a negative signed int with an unsigned int. No bueno.")
		else:
			print("cannot add int128 with {}".format(type(other)))
		raise TypeError


class under_bool:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False

class decimal:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False

class address:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False

class timestamp:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False

class timedelta:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False

class wei_value:
	def __init__(self, val=None):
		self.initd = True if val else False
		self.val = val
		self.public = False
		self.constant = False	

# class struct:

# class mapping:


def public(thing):
	try:
		thing.public
		thing.public = True
	except AttributeError:
		if type(thing) is bool:
			# May need to fix this for initialized vals
			b = under_bool()
			b.public = True
			return b
		if thing not in __vython_pub_funcs: 
			__vython_pub_funcs.append(thing)
	return thing


def private(thing):
	try:
		thing.public
		thing.public = False
	except AttributeError:
		if type(thing) is bool:
			# May need to fix this for initialized vals
			b = under_bool()
			return b
		if thing not in __vython_priv_funcs: 
			__vython_priv_funcs.append(thing)
	return thing


def constant(thing):
	try:
		thing.constant
		thing.constant = True
	except AttributeError:
		if thing not in __vython_const_funcs: 
			__vython_const_funcs.append(thing)



def payable(func):
	return func


def send(fr: address, to: address):
	pass


def selfdestruct(destructor: address):
	pass


## Transpile shit

class Vyper:
	def __init__(self, st):
		self.str = st

	def __str__(self):
		return self.str

class Bytecode:
	def __init__(self, st):
		self.str = st

	def __str__(self):
		return self.str

class Abi:
	def __init__(self, dic):
		self.abi = dic

	def to_json(self):
		return json.dumps(self.abi)

	def __str__(self):
		return str(self.abi)

class Deploy:
	def __init__(self, abi, bytecode):
		self.abi = abi
		self.bytecode = bytecode

	def __str__(self):
		fin = "abi: {}\n".format(str(self.abi))
		fin = fin + "-"*50 + "\n"
		fin = "{}bytecode: {}\n".format(fin, self.bytecode)
		return fin


class Lll:
	def __init__(self, node):
		self.node = node

	def __str__(self):
		return str(self.node)

def python_to_vyper(clss):
	# Perform 2 passes: first to collect all static vars, then to collect funcs.
	fin = ""
	for x in inspect.getmembers(clss):
		if not callable(x[1]):
			name = type(x[1]).__name__ if type(x[1]).__name__ != "under_bool" else "bool"
			try:
				if x[1].public:
					dec = "{}: public({})".format(x[0], name)
				else:
					dec = "{}: private({})".format(x[0], name)
				if x[1].initd:
					dec = "{} = {}".format(dec, x[1].val)
				fin = "{}\n{}".format(fin, dec)
			except AttributeError:
				pass

	fin = "{}\n\n".format(fin)
	for x in inspect.getmembers(clss):
		if callable(x[1]) and (x[0][0:2]!="__" or x[0]=="__init__") and x[0] != "builtins":
			func = textwrap.dedent(inspect.getsource(x[1]))
			for st in func.splitlines():
				if st[0:3] == "def":
					fin = "{}\n{}".format(fin, st.replace("self,","").replace("self", ""))
				else:
					fin = "{}\n{}".format(fin, st)
	return Vyper(fin)

# deploy = bytecode + abi
def transpile(clss, target="deploy"):
	if target not in ["deploy", "abi", "bytecode", "lll", "vyper", "vy"]: 
		raise ValueError("Unrecognized target for transpilation")
	if type(clss) is Lll:
		#todo: need to rework this
		if target == "bytecode":
			asm = compile_to_assembly(clss.node)
			return '0x' + assembly_to_evm(asm).hex()
		raise ValueError("lll can only be compiled to bytecode for now")

	vyp = python_to_vyper(clss)

	if target == "vyper" or target == "vy":
		return vyp

	if target == "bytecode":
		return Bytecode('0x' + compiler.compile(str(vyp)).hex())

	if target == "abi":
		return Abi(compiler.mk_full_signature(str(vyp)))

	if target == "deploy":
		abi = Abi(compiler.mk_full_signature(str(vyp)))
		bytecode = Bytecode('0x' + compiler.compile(str(vyp)).hex())
		return Deploy(abi, bytecode)

	return Lll(optimizer.optimize(parse_to_lll(str(vyp))))

def deploy(deploy):
	if type(deploy) is not Deploy:
		raise ValueError("Deploy only works with Deploy objects!")
	print("ok")

	#todo: swap this!
	w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545/"))
	w3.eth.defaultAccount = w3.eth.accounts[0]
	ctest = w3.eth.contract(abi=deploy.abi.to_json(), bytecode=str(deploy.bytecode))
	print(type(ctest))
	tx_hash = ctest.constructor().transact()
	tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	return tx_receipt
	# print(w3.isConnected())

