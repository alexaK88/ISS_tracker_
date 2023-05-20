import json  # that's for reading info on ISS
import time  # that's for reducing polling
import matplotlib.pyplot as plt  # for visualisation
from urllib.request import urlopen  # for fetching ISS info
import cartopy.crs as ccrs  # for mapping

def draw_iss(doblit=True):
    # setting the environment where there's going to be mapping
    # setting the extents of the coordinate mapping
    # this code shows the map of the Earth on the grid
    fig, _ = plt.subplots(1, 1)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    if doblit:
        background = fig.canvas.copy_from_bbox(ax.bbox)  # cache the background
    plt.ion()
    plt.show()
    # live tracking
    # copying the current background from the figure
    while True:
        time.sleep(5)  # updating info every 5 seconds
        # placing the ISS as a mark on the map
        # fetching the location of the ISS by using Open-Notify
        request = urlopen("http://api.open-notify.org/iss-now.json")
        # object contains JSON object with a success or failure message, timestap,
        # latitude and longitude of the ISS
        # json library reads the information into the dictionary format and then
        # python accesses information
        obj = json.loads(request.read())
        # print(obj['timestamp'])
        point = plt.plot([float(obj['iss_position']['longitude'])],
             [float(obj['iss_position']['latitude'])],
             color='red', marker='x', markersize=6, transform=ccrs.PlateCarree(),)
        plt.draw()
        if doblit:
            fig.canvas.restore_region(background)  # restore background
            fig.canvas.blit(ax.bbox)  # fill in the axes rectangle
        else:
            fig.canvas.draw()  # redraw everything
        plt.pause(0.005)
        for p in point:
            p.remove()


if __name__ == '__main__':
    draw_iss(doblit=True)
