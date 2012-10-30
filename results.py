def skill_colors(ndx=-1):
	colors = ["orange", "green", "blue", "purple", "red"]
	if ((ndx<0) | (ndx>len(colors))):
		color = "black"
	else:
		color = colors[ndx]
	return(color)

def self_id_colors(ndx=-1):
	colors = ["#fdc592", "#b8f997", "#fba2c3", "#b3effe"]
	if ((ndx<0) | (ndx>len(colors))):
		color = "grey"
	else:
		color = colors[ndx]
	return(color)


def compute_results(session, DEBUG):
	#Data Businessperson, Data Creative, Data Researcher, Data Engineer
	# Rows: Scientist	Engineer	Business person	Artist	Researcher	Statistician	Jack of All Trades	Leader	Entrepeneur	Developer	Hacker
	self_id_labels = ['Data Businessperson', 'Data Creative', 'Data Researcher', 'Data Engineer']
	nmf_self_id_coefs = [[0.009963015, 0.3716809758, 0.85740821, 0.167622008, 0.04800009, 0.1281892, 0.3267641, 0.6594510, 0.61200620, 0.24482807, 0.0000108286],
						[0.129221047, 0.0026543565, 0.29647806, 0.850075527, 0.11137019, 0.2399181, 0.4589113, 0.1505755, 0.41604830, 0.34281471, 0.8454369306],
						[0.792606674, 0.0001581727, 0.01934239, 0.182484734, 0.95225779, 0.7290859, 0.4426208, 0.2950846, 0.07824637, 0.06751748, 0.0095306879],
						[0.506760298, 0.9637696274, 0.04407253, 0.003502658, 0.35405891, 0.2508140, 0.2702048, 0.2928380, 0.08595124, 0.76271333, 0.5897772478]]

	self_id_normalization  = [6.474, 4.733, 5.592, 5.608]

	#Programming, Stats, Math/OR, Bus, ML/Big Data
	#Rows: Algorithms	Back.End.Programming	Bayesian.Monte.Carlo.Statistics	Big.and.Distributed.Data	Business	Classical.Statistics	Data.Manipulation	Front.End.Programming	Graphical.Models	Machine.Learning	Math	Optimization	Product.Development	Science	Simulation	Spatial.Statistics	Stuctured.Data	Surveys.and.Marketing	Systems.Administration	Temporal.Statistics	Unstructured.Data	Visualization
	skill_labels = ['Programming', 'Stats', 'Math/OR', 'Business', 'ML/Big Data']
	nmf_rank_coefs = [[2.209891e-01, 7.037957e-01, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.667951e-01, 5.647743e-01, 2.220446e-16, 2.220446e-16, 2.179039e-01, 2.220446e-16, 2.220446e-16, 1.435995e-01, 2.220446e-16, 2.220446e-16, 4.951900e-01, 2.220446e-16, 5.684981e-01, 2.220446e-16, 2.220446e-16, 7.013570e-13],
						[2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 6.243905e-01, 3.798971e-01, 2.220446e-16, 2.220446e-16, 2.482207e-01, 1.455518e-01, 2.220446e-16, 2.220446e-16, 4.187207e-01, 1.375681e-01, 3.022789e-01, 2.220446e-16, 3.576539e-01, 2.220446e-16, 4.298513e-01, 2.220446e-16, 5.635239e-01],
						[4.253356e-01, 2.220446e-16, 5.191935e-01, 2.220446e-16, 2.220446e-16, 4.322221e-01, 2.173335e-01, 2.220446e-16, 3.264821e-01, 3.112354e-01, 4.030644e-01, 4.938181e-01, 2.220446e-16, 3.439012e-01, 3.048536e-01, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.107039e-01, 2.220446e-16, 2.852953e-06],
						[2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 1.268313e+00, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.248777e-01, 2.220446e-16, 2.691779e-01, 2.220446e-16, 1.069837e+00, 1.046090e-13, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 5.141404e-07],
						[2.220446e-16, 2.220446e-16, 2.220446e-16, 5.283354e-01, 2.220446e-16, 2.220446e-16, 2.980927e-01, 2.220446e-16, 2.220446e-16, 3.119030e-01, 3.214431e-10, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 2.220446e-16, 5.427035e-01, 2.220446e-16, 2.220446e-16, 2.220446e-16, 6.560886e-01, 4.377165e-01]]
	
	#No longer used
	#skill_normalization = [32.971, 35.006, 44.13, 18.496, 28.937]
	#skill_normalization = [58.5755, 63.1307, 65.8634, 57.1935, 52.6067]

	"""
	skills =['Algorithms', 'Back-End Programming', 'Bayesian/Monte-Carlo Statistics',  'Big and Distributed Data',  'Business', 
			'Classical Statistics', 'Data Manipulation', 'Front-End Programming', 'Graphical Models',
			'Machine Learning', 'Math', 'Optimization', 'Product', 'Science', 'Simulation', 'Spatial Statistics', 
			'Stuctured Data', 'Surveys and Marketing', 'Systems Administration', 'Temporal Statistics', 'Unstructured Data', 'Visualization']
	"""
	skills = [x for x in range(0,22)]

	q1 = session['q1']
	#q1 = q1.split(',')
	#del(q1[-1])

	skill_rank_vec = []
	for s in skills:
		if s in q1:
			rank = 21-q1.index(s)
		else:
			rank = 0
		print str(s) + '--->' + str(rank)
		skill_rank_vec.append(rank) 
	
	if DEBUG:
		print "skill_rank_vec"
		print skill_rank_vec

	skill_score = matmult(nmf_rank_coefs, skill_rank_vec)

	sum = 0
	for num in skill_score:
		sum += num

	skill_norm = max([max(skill_score), 2*(sum/len(skill_score)) ])


	loop_ndx=0;
	
	for i in skill_score:
		#skill_score[loop_ndx] = i/skill_normalization[loop_ndx]
		skill_score[loop_ndx] = i/skill_norm
		loop_ndx += 1

	skill_score_ndx_max = skill_score.index(max(skill_score))


	session['skill_score'] = skill_score
	session['skill_score_ndx_max'] = skill_score_ndx_max

	if DEBUG:
		print "skill_score"
		print skill_score
		print "Max Skill_Score_ndx"
		print skill_score_ndx_max

	session['skill_label'] = skill_labels[skill_score_ndx_max]

	q2 = session['q2']

	if DEBUG:
		print "q2"
		print q2
	self_id_score = matmult(nmf_self_id_coefs, q2)

	loop_ndx = 0
	for i in self_id_score:
		self_id_score[loop_ndx] = i/self_id_normalization[loop_ndx]
		loop_ndx += 1

	self_id_score_ndx_max = self_id_score.index(max(self_id_score))

	session['self_id_score'] = self_id_score
	session['self_id_score_ndx_max'] = self_id_score_ndx_max

	if DEBUG:
		print "Self ID Score"
		print self_id_score
		print "Max Self_ID_Score_ndx"
		print self_id_score_ndx_max

	session['self_label'] = self_id_labels[self_id_score_ndx_max]

	return(session)


def matmult(m, v):
	nrows = len(m)
	w = [None] * nrows
	for row in range(nrows):
		w[row] = reduce(lambda x,y: x+y, map(lambda x,y: x*y, m[row], v))
	return w