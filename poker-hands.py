#!/usr/bin/python

#Amir Haziem Razali
#Python solution for poker hands for ICM Consulting
#18/10/2020

import io
import sys
import argparse
from collections import defaultdict
from itertools import combinations

parser = argparse.ArgumentParser(description= "Poker Hands Programming Exercise")
parser.add_argument('--filename', default="poker-hands.txt")
args = parser.parse_args()

values_dict = {"2":2, 
"3":3, 
"4":4, 
"5":5, 
"6":6, 
"7":7, 
"8":8, 
"9":9, 
"T":10, 
"J":11, 
"Q":12, 
"K":13, 
"A":14}

rank_dict = {10:"royal-flush", 
9:"straight-flush", 
8:"four-of-a-kind", 
7:"full-house", 
6:"flush", 
5:"straight", 
4:"three-of-a-kind", 
3:"two-pairs", 
2:"pair", 
1:"highest-card"}


def main():
	p1_counter  = 0
	p2_counter = 0
	tie = 0
	tied_games = []
	j = 0 #round number
	with open(args.filename) as f:
		for line in f:
			j+=1
			[p1, p2] = read_line(line)
			if decision(p1,p2) == "p1":
				p1_counter+=1
				# print("p1 wins round {} with hand {}".format(j,p1))
				# print("p2 loses round {} with hand {}".format(j,p2))
			elif decision(p1,p2) == "p2":
				p2_counter+=1
				# print("p2 wins round {} with hand {}".format(j,p2))
				# print("p1 loses round {} with hand {}".format(j,p1))
			else:
				#goal is to not have any ties
				tie+=1
				tied_games.append(j)
				print("Tied game")
				print("p1 hand: {}".format(p1))
				print("p2 hand: {}".format(p2))
			
			print("Player 1: {} hands".format(p1_counter))
			print("Player 2: {} hands".format(p2_counter))
			print("Tied games: {} at rounds: {}".format(tie,tied_games))
			print("Total rounds: {} rounds".format(j))
			# if j == 10:
			# 	break
	f.close()

def decision(p1,p2):
	winner = " "
	if check_hand(p1) > check_hand(p2):
		winner = "p1"
	elif check_hand(p1) < check_hand(p2):
		winner = "p2"
	elif check_hand(p1) == check_hand(p2):
		#gotta break the tie somehow, last resort is return_highest_value
		# print("check_hand results: \np1:{}  p2:{}".format(check_hand(p1),check_hand(p2)))
		if check_hand(p1) == 9: #straight-flush
			if return_highest_value(p1) > return_highest_value(p2):
				winner = "p1"
			elif return_highest_value(p1) < return_highest_value(p2):
				winner = "p2"
		elif check_hand(p1) == 8: #four-of-a-kind
			if values_dict[check_four_kind(p1)[1]] > values_dict[check_four_kind(p2)[1]]:
				winner = "p1"
			elif values_dict[check_four_kind(p1)[1]] < values_dict[check_four_kind(p2)[1]]:
				winner = "p2"
		elif check_hand(p1) == 7: #full-house
			if values_dict[check_full_house(p1)[1]] > values_dict[check_full_house(p2)[1]]:
				winner = "p1"
			elif values_dict[check_full_house(p1)[1]] < values_dict[check_full_house(p2)[1]]:
				winner = "p2"
		elif check_hand(p1) == 6: #flush
			if return_highest_value(p1) > return_highest_value(p2):
				winner = "p1"
			elif return_highest_value(p1) < return_highest_value(p2):
				winner = "p2"
		elif check_hand(p1) == 5: #straights
			if return_highest_value(p1) > return_highest_value(p2):
				winner = "p1"
			elif return_highest_value(p1) < return_highest_value(p2):
				winner = "p2"
		elif check_hand(p1) == 4: #three-of-a-kinds
			if values_dict[check_three_kind(p1)[1]] > values_dict[check_three_kind(p2)[1]]:
				winner = "p1"
			elif values_dict[check_three_kind(p1)[1]] < values_dict[check_three_kind(p2)[1]]:
				winner = "p2"
		elif check_hand(p1) == 3: #two-pairs
			if values_dict[check_two_pairs(p1)[1]] > values_dict[check_two_pairs(p2)[1]]:
				winner = "p1"
			elif values_dict[check_two_pairs(p1)[1]] < values_dict[check_two_pairs(p2)[1]]:
				winner = "p2"
		elif check_hand(p1) == 2:
			if values_dict[check_pair(p1)[1]] > values_dict[check_pair(p2)[1]]:
				winner = "p1"
			elif values_dict[check_pair(p1)[1]] < values_dict[check_pair(p2)[1]]:
				winner = "p2"
			elif values_dict[check_pair(p1)[1]] == values_dict[check_pair(p2)[1]]:
				#in case of two of the same pairs against each other, need to eliminate the two pairs and return highest card
				if return_highest_value(p1) > return_highest_value(p2):
					winner = "p1"
				elif return_highest_value(p1) < return_highest_value(p2):
					winner = "p2"
		else:
			if return_highest_value(p1) > return_highest_value(p2):
				winner = "p1"
			elif return_highest_value(p1) < return_highest_value(p2):
				winner = "p2"
			elif return_highest_value(p1) == return_highest_value(p2):
				p1_values = [i[0] for i in p1]
				p2_values = [j[0] for j in p2]
				p1_ranks = [values_dict[i] for i in p1_values]
				p2_ranks = [values_dict[i] for i in p2_values]
				for i in p1:
					[p1_rank, p1_newhand] = remove_highest_card(p1_ranks)
					[p2_rank, p2_newhand] = remove_highest_card(p2_ranks)
					if p1_rank > p2_rank:
						winner = "p1"
						break
					elif p1_rank < p2_rank:
						winner = "p2"
						break
					else:
						p1_values = p1_newhand
						p2_values = p2_newhand
	# else:
	# 	winner = " "

	return winner

#read and split into player 1 and player 2 lists
def read_line(line):
	p1 = line[:15]
	p1 = p1.split(" ")
	p1.pop() #get rid of spaces
	p2 = line[15:]
	p2 = p2.strip("\n") #get rid of line terminator
	p2 = p2.split(" ")
	return [p1, p2]

def check_hand(hand):
	if check_royal_flush(hand):
		# print("royal-flush detected")
		return 10
	elif check_straight_flush(hand)[0]:
		# print("straight-flush detected")
		return 9
	elif check_four_kind(hand)[0]:
		# print("four-of-a-kind detected")
		return 8
	elif check_full_house(hand)[0]:
		# print("full-house detected")
		return 7
	elif check_flush(hand)[0]:
		# print("flush detected")
		return 6
	elif check_straight(hand):
		# print("straight detected")
		return 5
	elif check_three_kind(hand)[0]:
		# print("three-of-a-kind detected:",check_three_kind(hand)[1])
		return 4
	elif check_two_pairs(hand)[0]:
		# print("two-pairs detected")
		return 3
	elif check_pair(hand)[0]:
		# print("pair detected: pair of",check_pair(hand)[1])
		return 2
	else:
		return 1

def check_royal_flush(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	if check_flush(hand) and check_straight(hand):
		#check for royal flush
		for v in values:
			value_counts[v]+=1
			rank = [values_dict[i] for i in values]
			if sum(rank) == 60:
				return True
	return False

def check_straight_flush(hand):
	values = [i[0] for i in hand]
	if check_flush(hand) and check_straight(hand):
		return (True, return_highest_value(hand))
	return (False, return_highest_value(hand))

def check_four_kind(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	for v in values:
		value_counts[v]+=1
	if sorted(value_counts.values()) == [1,4]:
		fours = get_key(value_counts,4)
		return (True, fours)
	return (False, 0)

def check_full_house(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	for v in values:
		value_counts[v]+=1
	if sorted(value_counts.values()) == [2,3]:
		threes = get_key(value_counts,3)
		return (True, threes)
	return (False,0)

def check_flush(hand):
	suits = [j[1] for j in hand] #checking for similar suits
	if len(set(suits)) == 1:
		return (True, return_highest_value(hand))
	else:
		return (False, return_highest_value(hand))

def check_straight(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	for v in values:
		value_counts[v]+=1
	rank = [values_dict[i] for i in values]
	value_range = max(rank) - min(rank)
	if len(set(value_counts.values())) == 1 and (value_range==4):
		return True
	return False

def check_three_kind(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	for v in values:
		value_counts[v]+=1
	if set(value_counts.values()) == set([3,1]):
		threes = get_key(value_counts,3)
		return (True, threes)
	else:
		return (False, 0)

def check_two_pairs(hand):
	values = [i[0] for i in hand]
	value_counts = []
	value_counts = defaultdict(lambda:0)
	for v in values:
		value_counts[v]+=1
	if sorted(value_counts.values()) == [1,2,2]:
		pairs = get_key(value_counts,2)
		return (True, pairs)
	else:
		return (False, 0)

def check_pair(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	for v in values:
		value_counts[v]+=1
	# print("Value counts: ",value_counts)
	if set(value_counts.values()) == set([2,1]):
		pair = get_key(value_counts,2)
		return (True, pair)
	else:
		return (False, 0)

def return_highest_value(hand):
	values = [i[0] for i in hand]
	value_counts = defaultdict(lambda:0)
	for v in values:
			value_counts[v]+=1
			rank = [values_dict[i] for i in values]
	return max(rank)

def get_key(my_dict, val):
	for key, value in my_dict.items():
		if val == value:
			return key

def remove_highest_card(rank):
	#remove highest card and return new highest and new hand
	rank.remove(max(rank))
	return (max(rank),rank)

if __name__=="__main__":
	main()
