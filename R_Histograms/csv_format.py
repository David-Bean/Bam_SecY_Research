
read_file = 'enterobacteralesOA_original_conserved.csv'
write_file = 'formatted_'+read_file

with open(read_file,'r') as read_csv:
	lines = read_csv.readlines()
	
titles = lines[0]
values = [line[2:-3].replace(' ','') for line in lines[1::]]
values = '\n'.join(values)
new_csv = titles+values

with open(write_file,'w') as write_csv:
	write_csv.write(new_csv)

