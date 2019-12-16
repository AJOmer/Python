for x in range(151):
	print(x)

for x in range(5,1005,5):
	print(x)

for x in range(1,101):
	if(x % 5 == 0):
		print("coding")
	if(x % 10 == 0):
		print("Coding Dojo")


totalOdd = 0
for x in range(500001):
	if (x % 2 == 1):
		totalOdd += x
print(totalOdd) 


for x in range(2018, 0, -4):
	print(x) 




lowNum = 2
highNum = 10
mult = 3
for x in range(lowNum, highNum):
	if(x % mult ==0):
		print(x)