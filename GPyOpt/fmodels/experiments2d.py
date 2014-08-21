from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

'''
Benchmark of optimzation functions. 

List of avaiable functions so far:
- Branin

The classes are oriented to create a python function which contain.
- *.f : the funtion itself
- *.plot: a plot of the function if the dimension is <=2.
- *.sensitivity: The Sobol coefficient per dimension when these are available.
- *.min : value of the global minimum(s) for the default parameters.

NOTE: the imput of .f must be a nxD numpy array. The dimension is calculated within the fucntion.

Javier Gonzalez August, 2014
'''


class function2d:
        def plot(self):
		bounds = self.bounds
                x1 = np.linspace(bounds[0][0], bounds[0][1], 100)
                x2 = np.linspace(bounds[1][0], bounds[1][1], 100)
                X1, X2 = np.meshgrid(x1, x2)
                X = np.hstack((X1.reshape(100*100,1),X2.reshape(100*100,1)))
                Y = self.f(X)

        	fig = plt.figure()
                ax = fig.gca(projection='3d')
                surf = ax.plot_surface(X1, X2, Y.reshape((100,100)), rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
                ax.zaxis.set_major_locator(LinearLocator(10))
                ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
               	ax.set_title(self.name)	
			
		plt.figure()	
		plt.contourf(X1, X2, Y.reshape((100,100)),100)
		if (len(self.min)>1):	
			plt.plot(np.array(self.min)[:,0], np.array(self.min)[:,1], 'w.', markersize=20, label=u'Observations')
		else:
			plt.plot(self.min[0][0], self.min[0][1], 'w.', markersize=20, label=u'Observations')
		plt.colorbar()
		plt.xlabel('X1')
		plt.ylabel('X2')
		plt.title(self.name)
		plt.show()


class branin(function2d):
	def __init__(self,bounds=None,a=None,b=None,c=None,r=None,s=None,t=None,sd=None):
		self.D = 2
		if bounds == None: self.bounds = [(-5,10),(1,15)]
		else: self.bounds = bounds
		if a==None: self.a = 1
		else: self.a = a   		
		if b==None: self.b = 5.1/(4*np.pi**2)
		else: self.b = b
		if c==None: self.c = 5/np.pi
                else: self.c = c
		if r==None: self.r = 6
		else: self.r = r
		if s==None: self.s = 10 
		else: self.s = s
		if t==None: self.t = 1/(8*np.pi)
		else: self.t = t	
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.min = [(-np.pi,12.275),(np.pi,2.275),(9.42478,2.475)] 
		self.fmin = 0.397887
		self.name = 'Branin'
	
	def f(self,X):
		if len(X)==self.D: X = X.reshape((1,2))
		n = X.shape[0]
		if X.shape[1] != self.D: 
			return 'Wrong input dimension'  
		else:
			x1 = X[:,0]
			x2 = X[:,1]
			fval = self.a * (x2 - self.b*x1**2 + self.c*x1 - self.r)**2 + self.s*(1-self.t)*np.cos(x1) + self.s 
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise



class crossintray(function2d):
	def __init__(self,bounds=None,sd=None):
		self.D = 2
		if bounds == None: self.bounds = [(-10,10),(-10,10)]
		else: self.bounds = bounds
		self.min = [(1.3491,-1.3491),(1.3491,1.3491),(-1.3491,1.3491),(-1.3491,-1.3491)]
		self.fmin = -2.06261
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Cross in tray'

	def f(self,X):
		if len(X)==self.D: X = X.reshape((1,2))
		n = X.shape[0]
		if X.shape[1] != self.D:
			return 'Wrong input dimension'
		else:
			x1 = X[:,0]
			x2 = X[:,1]
			fval = -0.0001 *(abs (np.sin(x1)*np.sin(x2) *np.exp(abs(100-(np.sqrt(x1**2+x2**2) )/np.pi ) ) ) + 1 )**.1
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise


class dropwave(function2d):
	def __init__(self,bounds=None,sd=None):
		self.D = 2
		if bounds == None: self.bounds = [(-5.12,5.12),(-5.12,5.12)]
		else: self.bounds = bounds
		self.min = [(0,0)]
		self.fmin = -1
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Drop wave'

	def f(self,X):
		if len(X)==self.D: X = X.reshape((1,2))
		n = X.shape[0]
		if X.shape[1] != self.D:
			return 'Wrong input dimension'
		else:
			x1 = X[:,0]
			x2 = X[:,1]
			fval = -(1 + np.cos(12* np.sqrt(x1**2+x2**2)))/(0.5*(x1**2+x2**2)+2)
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise



class eggholder(function2d):
	def __init__(self,bounds=None,sd=None):
		self.D = 2
		if bounds == None: self.bounds = [(-512,512),(-512,512)]
		else: self.bounds = bounds
		self.min = [(512,404.2319)]
		self.fmin = -959.6407
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Egg-holder'

	def f(self,X):
		if len(X)==self.D: X = X.reshape((1,2))
		n = X.shape[0]
		if X.shape[1] != self.D:
			return 'Wrong input dimension'
		else:
			x1 = X[:,0]
			x2 = X[:,1]
			fval = -(x2+47) * np.sin(np.sqrt(abs(x2+x1/2+47))) + -x1 * np.sin(np.sqrt(abs(x1-(x2+47))))
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise



class goldstein(function2d):
	def __init__(self,bounds=None,sd=None):
		self.D = 2
		if bounds == None: self.bounds = [(-2,2),(-2,2)]
		else: self.bounds = bounds
		self.min = [(0,-1)]
		self.fmin = 3
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Goldstein'

	def f(self,X):
		if len(X)==self.D: X = X.reshape((1,2))
		n = X.shape[0]
		if X.shape[1] != self.D:
			return 'Wrong input dimension'
		else:
			x1 = X[:,0]
			x2 = X[:,1]
			fact1a = (x1 + x2 + 1)**2
			fact1b = 19 - 14*x1 + 3*x1**2 - 14*x2 + 6*x1*x2 + 3*x2**2
			fact1 = 1 + fact1a*fact1b
			fact2a = (2*x1 - 3*x2)**2
			fact2b = 18 - 32*x1 + 12*x1**2 + 48*x2 - 36*x1*x2 + 27*x2**2
			fact2 = 30 + fact2a*fact2b
			fval = fact1*fact2
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise


class beale(function2d):
	def __init__(self,bounds=None,sd=None):
		self.D = 2
		if bounds == None: self.bounds = [(-4.5,4.5),(-4.5,4.5)]
		else: self.bounds = bounds
		self.min = [(3,0.5)]
		self.fmin = 0
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Beale'

	def f(self,X):
		if len(X)==self.D: X = X.reshape((1,2))
		n = X.shape[0]
		if X.shape[1] != self.D:
			return 'Wrong input dimension'
		else:
			x1 = X[:,0]
			x2 = X[:,1]
			term1 = (1.5 - x1 + x1*x2)**2
			term2 = (2.25 - x1 + x1*x2**2)**2
			term3 = (2.625 - x1 + x1*x2**3)**2
			fval = term1 + term2+ term3
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise


class sixhumpcamel(function2d):
	def __init__(self,bounds=None,sd=None):
		self.d = 2
		if bounds == None: self.bounds = [(-2,2),(-1,1)]
		else: self.bounds = bounds
		self.min = [(0.0898,-0.7126),(-0.0898,0.7126)]
		self.fmin = -1.0316
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Six-hump camel'

	def f(self,x):
		if len(x)==self.d: x = x.reshape((1,2))
		n = x.shape[0]
		if x.shape[1] != self.d:
			return 'wrong input dimension'
		else:
			x1 = x[:,0]
			x2 = x[:,1]
			term1 = (4-2.1*x1**2+(x1**4)/3) * x1**2
			term2 = x1*x2
			term3 = (-4+4*x2**2) * x2**2
			fval = term1 + term2 + term3
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise



class mccormick(function2d):
	def __init__(self,bounds=None,sd=None):
		self.d = 2
		if bounds == None: self.bounds = [(-1.5,4),(-3,4)]
		else: self.bounds = bounds
		self.min = [(-0.54719,-1.54719)]
		self.fmin = -1.9133
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Mccormick'

	def f(self,x):
		if len(x)==self.d: x = x.reshape((1,2))
		n = x.shape[0]
		if x.shape[1] != self.d:
			return 'wrong input dimension'
		else:
			x1 = x[:,0]
			x2 = x[:,1]
			term1 = np.sin(x1 + x2)
			term2 = (x1 - x2)**2
			term3 = -1.5*x1
			term4 = 2.5*x2
			fval = term1 + term2 + term3 + term4 + 1
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise


class levy2(function2d):
	def __init__(self,bounds=None,sd=None):
		self.d = 2
		if bounds == None: self.bounds = [(-10,10),(-10,10)]
		else: self.bounds = bounds
		self.min = [(1,1)]
		self.fmin = 0
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Levy2'

	def f(self,x):
		if len(x)==self.d: x = x.reshape((1,2))
		n = x.shape[0]
		if x.shape[1] != self.d:
			return 'wrong input dimension'
		else:
			x1 = x[:,0]
			x2 = x[:,1]
			w1 = 1 + (x1-1)/4
			w2 = 1 + (x2-1)/4
			term1 = np.sin(np.pi*w1)**2
			term2 = (w1-1)**2*(1+10*np.sin(np.pi*w1+1)**2)
			term3 = (w2-1)**2*(1 +np.sin(2*np.pi*w2)**2)			
			fval = term1 + term2 + term3
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise



class schaffer2(function2d):
	def __init__(self,bounds=None,sd=None):
		self.d = 2
		if bounds == None: self.bounds = [(-2,2),(-2,2)]
		else: self.bounds = bounds
		self.min = [(0,0)]
		self.fmin = 0
		if sd==None: self.sd = 0
		else: self.sd=sd
		self.name = 'Schaffer2'

	def f(self,x):
		if len(x)==self.d: x = x.reshape((1,2))
		n = x.shape[0]
		if x.shape[1] != self.d:
			return 'wrong input dimension'
		else:
			x1 = x[:,0]
			x2 = x[:,1]
			fact1 = (np.sin(x1**2-x2**2))**2 - 0.5
			fact2 = (1 + 0.001*(x1**2+x2**2))**2
			fval = 0.5 + fact1/fact2;
			if self.sd ==0:
				noise = np.zeros(n).reshape(n,1)
			else:
				noise = np.random.normal(0,self.sd,n).reshape(n,1)
			return fval.reshape(n,1) + noise
















