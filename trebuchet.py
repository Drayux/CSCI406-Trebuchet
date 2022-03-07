# TREBUCHET PROBLEM ALGORITHM
# Liam Dempsey

import time
import sys

rcalls = 0

def trebuchet(p, t):
	global rcalls
	rcalls += 1

	# Base cases
	if p == 1 or t <= 1: return t

	# Check best case for each target
	minthrows = t + 1
	for x in range(1, t + 1):
		broken = trebuchet(p - 1, x - 1)
		intact = trebuchet(p, t - x)

		minthrows = min(max(broken, intact), minthrows)

	return 1 + minthrows

def trebuchetdp(p, t, output=False):
	# Build an empty table
	table = [[0 for i in range(t + 1)] for j in range(p)]  # Primary table
	tb = [[0 for i in range(t + 1)] for j in range(p)]  # Traceback table

	# Set up the base case values
	# Primary table
	for i in range(1, t + 1): table[0][i] = i
	for i in range(1, p): table[i][1] = 1

	# Traceback table
	for i in range(2, t + 1): tb[0][i] = 1
	for i in range(0, p): tb[i][1] = -1

	# Compute recursive entries
	for row in range(1, p):
		for col in range(2, t + 1):
			entrymin = t
			besttarget = 0

			for x in range(1, col + 1):
				broken = table[row - 1][x - 1]
				intact = table[row][col - x]
				
				tmp = max(broken, intact)
				if tmp < entrymin:
					entrymin = tmp
					besttarget = x * ((-1) if broken >= intact else 1)

			table[row][col] = entrymin + 1
			tb[row][col] = besttarget

	# Traceback step
	targets = []
	offset = 0
	row = p - 1
	col = t

	while True:
		# Check if we're done
		if col <= 0: break

		# Determine the next entry
		entry = tb[row][col]
		x = abs(entry)
		if entry < 0 and row > 1:
			row -= 1
			col -= col - x + 1

		else:
			col -= x

		# Append to the list and update the offset
		targets.append((x + offset) * ((-1) if entry < 0 else 1))
		if entry > 0: offset += x


	# Table output for debugging
	# if output:
	# 	print("Throws:")
	# 	for row in table:
	# 		print(row)
	# 	print()

	# 	print("Traceback:")
	# 	for row in tb:
	# 		print(row)
	# 	print()

	return table[p - 1][t], targets

# Mode = 0 track recursive calls
# Mode = 1 track runtimes
def toCSV(p, t, num):
	global rcalls

	calls = open(f"rcalls-{num}.csv", 'w')
	times = open(f"rtimes-{num}.csv", 'w')

	# Num pumpkins is rows
	for i in range(1, p + 1):
		rowcalls = ""
		rowtimes = ""

		# Num targets is columns
		for j in range(1, t + 1):
			# Debug output
			print(f"Now testing T({i}, {j})...")

			# Reset the calls counter
			rcalls = 0
			starttime = time.perf_counter()

			# The actual recursive function
			trebuchetdp(i, j)

			if j != 1: 
				rowcalls += f",{rcalls}"
				rowtimes += f",{time.perf_counter() - starttime}"

			else:
				rowcalls = f"{rcalls}"
				rowtimes = f"{time.perf_counter() - starttime}"

		# Append the results
		calls.write(rowcalls + "\n")
		times.write(rowtimes + "\n")

	calls.close()
	times.close()

	print("Done!")

if __name__ == "__main__":
	p = int(sys.argv[1])
	t = int(sys.argv[2])

	if len(sys.argv) == 4:
		toCSV(p, t, int(sys.argv[3]))
		exit(0)

	throws, targets = trebuchetdp(p, t, True)

	print(f"INPUT: pumpkins = {p}, targets = {t}")
	print(f"Min throws: {throws} (worst-case)")
	# print(f"Recursive calls: {rcalls}")
	# print("Targets:", end = " ")
	# print(targets)

	print()
	print(throws)
	for x in targets: print(x, end = " ")
	print()

	print()


