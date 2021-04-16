import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from numpy import genfromtxt



file = "sys_error.txt"
data = genfromtxt(file, delimiter='\t')
x = data[1:,0]
y = data[1:,2]
sigma_x = data[1:,1]
sigma_y = data[1:,3]

print(x,y,sigma_x,sigma_y)

# Our 2-dimensional distribution will be over variables X and Y
N = 60
X = np.linspace(-13, 13, N)
Y = np.linspace(-13, 13, N)
X, Y = np.meshgrid(X, Y)

# Mean vector and covariance matrix
mu = np.array([0., 1.])
Sigma = np.array([[ 1. , -0.5], [-0.5,  1.5]])

# Pack X and Y into a single 3-dimensional array
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y

def multivariate_gaussian(pos, mu, Sigma):
    """Return the multivariate Gaussian distribution on array pos.

    pos is an array constructed by packing the meshed arrays of variables
    x_1, x_2, x_3, ..., x_k into its _last_ dimension.

    """
    print("mduabfjds",mu)
    n = mu.shape[0]
    Sigma_det = np.linalg.det(Sigma)
    Sigma_inv = np.linalg.inv(Sigma)
    N = np.sqrt((2*np.pi)**n * Sigma_det)
    # This einsum call calculates (x-mu)T.Sigma-1.(x-mu) in a vectorized
    # way across all the input variables.
    fac = np.einsum('...k,kl,...l->...', pos-mu, Sigma_inv, pos-mu)

    return np.exp(-fac / 2) / N

# The distribution on the variables X, Y packed into pos.
z = []
Z = multivariate_gaussian(pos, mu, Sigma)

for i in range(len(x)): 
    mu = np.array([x[i],y[i]])
    Sigma = np.array([[sigma_x[i],-sigma_x[i]/2], [-sigma_y[i]/2,sigma_y[i]]])
    Z = multivariate_gaussian(pos, mu, Sigma)
    z.append(Z)

# Create a surface plot and projected filled contour plot under it.
fig = plt.figure()
ax = fig.gca(projection='3d')
for i in range(len(z)):
    ax.plot_surface(X, Y, z[i], rstride=3, cstride=3, linewidth=1, antialiased=True,
                    cmap=cm.viridis)

    cset = ax.contourf(X, Y, z[i], zdir='z', offset=-0.15, cmap=cm.viridis)

# Adjust the limits, ticks and view angle
ax.set_zlim(-0.15,0.2)
ax.set_zticks(np.linspace(0,0.2,5))
ax.view_init(27, -21)

#plt.show()
print(sigma_x[:-3])
print(sigma_y[:-3])
print(np.mean(sigma_x[:-3]),np.std(sigma_x[:-3]))
print(np.mean(sigma_y[:-3]),np.std(sigma_y[:-3]))