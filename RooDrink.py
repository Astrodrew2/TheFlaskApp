
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from matplotlib.colors import ListedColormap
def DrinkRating(name,beer,wine,whiskey,urname): 

    x = np.array(beer)
    y = np.array(wine)
    z = np.array(whiskey)
    a = np.array(urname)

# Create a dictionary to map unique names to colors
    name_to_color = {}

# Assign a random color to each unique name
    for usr in set(a):
        name_to_color[usr] = "#%06x" % random.randint(0, 0xFFFFFF)

    color_list = [name_to_color[usr] for usr in a]

# Print the names with their respective colors
   # for usr in a:
      #  print(f"{usr}: {name_to_color[usr]}")

    #create table

    



# initialize data of lists.
    data = {'Beer Rating': x,
            'Wine Rating': y,
            'Whiskey Rating': z,
            'User': a}

# Create DataFrame
    df = pd.DataFrame(data, index = name)

    print(df)
    df.to_pickle('bevlist4roo.pkl')
    #df.to_csv('bevlist4roo.csv')

    fig = plt.figure()

    ax = plt.axes(projection='3d')

    for xcod,ycod,zcod,names in zip(x,y,z,name):
        ax.text(xcod,ycod,zcod,names)

    p = ax.scatter(x, y, z, c=color_list)
              
    ax.set_title('Roo Drink Chart, by Andrew')
    ax.set_xlabel("Beer: Guinness")
    ax.set_ylabel("Wine: Riaca")

    ax.set_zlabel("Whiskey: 10yr Talisker")

    # Create a color bar with the unique names and their colors
    unique_names = list(name_to_color.keys())
    unique_colors = list(name_to_color.values())

# Create a custom colorbar-like legend

    cmap = ListedColormap(unique_colors)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=len(unique_names)))
    sm.set_array([])

    # Add the color bar to the side
    cbar = plt.colorbar(sm, ax=ax, ticks=range(len(unique_names)))
    cbar.set_ticks(range(len(unique_names)))
    cbar.set_ticklabels(unique_names)
    cbar.ax.set_title("Names")

    #basic color bar below
    #cbar = plt.colorbar(p)
    #cbar.set_label('Average', rotation=90)
    #fig.colorbar(p)
    
    plt.show()


def FindDrink(find):
    df = pd.read_pickle('bevlist4roo.pkl')
    drink = df.loc[[find]]
    print(drink)

def FindBest(type, val):
    df = pd.read_pickle('bevlist4roo.pkl')
    result = df.index[df[type]==val].tolist()
    print(result)

def FindName(type,user):
    df = pd.read_pickle('bevlist4roo.pkl')
    result = df.loc[df[type]==user]
    print(result)








