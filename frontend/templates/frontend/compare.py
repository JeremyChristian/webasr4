import os

def main(stop_list):

	"""Get stop_list terms."""

	stop_list = set(item.strip() for item in open(stop_list))
	print stop_list