import settings

def height_size(percentage):
    return (settings.HEIGHT / 100) * percentage

#print(height_size(80)) #patikrinti ar metodas veikia ir kiek procentu sudaro pikseliai

def width_size(percentage):
    return (settings.WIDTH / 100) * percentage
