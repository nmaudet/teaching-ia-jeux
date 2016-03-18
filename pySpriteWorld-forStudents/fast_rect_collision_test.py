
from fast_rect_collision import *
import random

class NaiveGroupCollide:
	'''
	Small class only written for test purposes, to compare with FastGroupCollide.
	It is used to check if FastGroupCollide class (see below) behaves correctly
	'''
	def __init__(self,group,max_interv=None):
		self.group = set(group)
	def add_sprite(self,s):
		self.group.add(s)
	def remove_sprite(self,s):
		self.group.remove(s)
	def update_sprite(self,s):
		pass
	def compute_collision_list(self,s,collision_callback=None):
		candidates = []
		l,t,r,b = s.rect.left,s.rect.top,s.rect.right,s.rect.bottom

		for s2 in self.group:
			l2,t2,r2,b2 = s2.rect.left,s2.rect.top,s2.rect.right,s2.rect.bottom

			if r2 < l or l2 > r or t2 > b or b2 < t:	continue

			if collision_callback is None or collision_callback(s,s2):
				if id(s2) != id(s):
					candidates.append( s2 )
		return candidates


'''

	*******************************************************************************
	TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST
	*******************************************************************************

'''
import time
from collections import namedtuple

'''
	TestSprite and TestRect are only for standalone test purpose
'''
TestSprite = namedtuple('TestSprite',['rect'])
class TestRect:
	def __init__(self,**kargs): self.__dict__ = kargs
	def __repr__(self):
		return 't/l/r/b='+str(self.top)+'/'+str(self.left)+'/'+str(self.right)+'/'+str(self.bottom)



def frc_make_random_group(N):
	''' create group of N random 'sprites' '''
	group = []
	for i in range(N):
		t=random.randint(0,500)
		l=random.randint(0,500)
		r=l+31+random.randint(0,10)
		b=t+31+random.randint(0,10)
		group.append( TestSprite(rect=TestRect(top=t,bottom=b,left=l,right=r)) )
		#print( group[-1] )
	return group

def frc_test_update_sprites():
	'''
	checks update_sprite in FastGroupCollide
	tries updating sprites, and checks if collision detection still works

	algorithm:
	---------
	1. create a group of sprites
	2. repeat
		A. pick a random sprite
		B. change its rectangle
		C. call update_sprite
		D. check if still consistent behavior
	'''
	g = frc_make_random_group(3)
	initial_fgd = FastGroupCollide(g,max_interv=42)
	for i in range(50):
		for j in range(10):
			s = random.choice(g)
			#print('sprite before update:',s)
			r = s.rect
			r.top, r.left = random.randint(0,500),random.randint(0,500)
			r.right=r.left+31+random.randint(0,10)
			r.bottom=r.top+31+random.randint(0,10)
			#print('sprite after update: ',s,'\n')
			initial_fgd.add_or_update_sprite(s)
		new_fgd = FastGroupCollide(g)
		_frc_check_consistency_count_collisions(g,initial_fgd,new_fgd)
	print('  frc_test_update_sprites OK')

def frc_test_collisions(g,fg):
	''' count all collisions in group
		note: fg can be FastGroupCollide or NaiveGroupCollide
	'''
	ncoll = 0
	for s in g:
		l = fg.compute_collision_list(s)
		ncoll += len(l)
	return ncoll


def frc_test_fg(CollideClass,g,niter=1):
	''' measure time require to check all collisions multiple times
	'''
	t = time.time()
	for i in range(niter):
		fga = CollideClass(g,max_interv=42)
		frc_test_collisions(g,fga)
	return time.time() -t


def frc_measure_speed():
	'''
	On Asus eee-pc, we get:
	la = [0.001, 0.095, 0.25, 0.502, 0.806, 1.184, 1.612, 2.104, 2.685, 3.481, 4.066]
	lp = [0.001, 0.185, 0.603, 1.302, 2.219, 3.4, 4.888, 6.498, 8.5, 10.483, 13.071]
	'''
	import matplotlib.pyplot as plt
	print('running many experiments... might take a minute')
	la = [ frc_test_fg(FastGroupCollide, frc_make_random_group(N),20) for N in [1,100,200,300,400,500,600,700,800,900,1000]]
	#lp = [ frc_test_fg(NaiveGroupCollide,frc_make_random_group(N),20) for N in [1,100,200,300,400,500,600,700,800,900,1000]]
	print('plotting results')
	plt.plot(la)
	print(la)
	#plt.plot(lp)
	plt.show()


#la_cy =  [0.002588987350463867, 0.013396978378295898, 0.062116146087646484, 0.03505086898803711, 0.04832601547241211, 0.06245017051696777, 0.0944368839263916, 0.07260394096374512, 0.10058903694152832, 0.0993039608001709, 0.129655122756958]
#la_nocy= [0.012737035751342773, 0.11520600318908691, 0.27207207679748535, 0.2210381031036377, 0.30518198013305664, 0.42356395721435547, 0.47412681579589844, 0.6074831485748291, 0.7632999420166016, 0.8776600360870361, 1.074411153793335]

def _frc_check_consistency_count_collisions(group,fgc1,fgc2):
	ncoll = 0
	for s in group:
		l1 = set( fgc1.compute_collision_list(s) )
		l2 = set( fgc2.compute_collision_list(s) )
		ncoll += len(l1)
		assert l1==l2 , "INCONSISTENCY !!!"
	return ncoll

def frc_consistency_fga_fgn(N):
	'''
	check if FastGroupCollide and NaiveGroupCollide
	return the same collision lists.
	Also, prints statistics
	'''
	group = frc_make_random_group(N)
	ncoll = 0
	fga = FastGroupCollide(group,max_interv=42)
	fgn = NaiveGroupCollide(group,max_interv=42)

	ncoll = _frc_check_consistency_count_collisions(group,fga,fgn)

	print('  --  frc_consistency_fga_fgn stats collision --')
	print('  --> nb of sprites = ',len(group))
	print('  --> avg nb of collisions = ',ncoll/len(group))
	print('  frc_consistency_fga_fgn OK')


if __name__ == '__main__':
	print('### Testing FastGroupCollide classes ###')
	print('# checking if both classes behave the same way:')
	frc_consistency_fga_fgn(300)
	print('# checking if DictBased class can handle updating sprites correctly:')
	frc_test_update_sprites()
	print('\nto run the benchmark, type frc_measure_speed()')
