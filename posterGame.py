# importing required library
import pygame
import requests
import time
import io
from urllib.request import urlopen

# activate the pygame library .
pygame.init()


# create the display surface object
# of specific dimension..e(X, Y).



class mainLoop:
    window_width = int(1080/3)
    window_height = int(1960/3)
    movie_id = None
    loading = False
    def check_for_image(self):
        try:
            rsp = requests.get(f"http://192.168.86.35:8000/get-current-movie/{self.movie_id}")
            data = rsp.json()
            if data.get('msg',None) and self.loading == False:
                #self.i += 1
                #print("Check_for_image: " + str(self.i))
                msg = data['msg']
                if msg != 'Movie has not changed':
                    print("Check_for_image said to update image")
                    self.update_image(msg)
            return
        except Exception as e:
            print(str(e))
            return

    def update_image(self, data):
        print("SCHEDULER STOPPED")
        self.loading = True
        self.movie_id = data['movie_id']
        self.poster_path = data['poster_path']
        # create a surface object, image is drawn on it.

        image_str = urlopen(self.poster_path).read()
        # create a file object (stream)
        image_file = io.BytesIO(image_str)
        image = pygame.image.load(image_file)
        # Using blit to copy content from one surface to other
        poster = pygame.transform.scale(image, (self.window_width - 10, (self.window_height - 10)*(27/32)))
        # Using blit to copy content from one surface to other
        self.scrn.blit(poster,(5, self.window_height*(5/32)))

        # paint screen one time
        pygame.display.flip()
        self.loading = False
        return

    def main_loop(self):
        self.scrn = pygame.display.set_mode((self.window_width, self.window_height))

        # set the pygame window name
        pygame.display.set_caption('image')

        # create a surface object, image is drawn on it.
        twilight = pygame.image.load('static/theatername.jpg').convert()
        poster = pygame.image.load('static/default.jpeg').convert()
        twilight = pygame.transform.scale(twilight, (self.window_width, (self.window_height)*(5/32)))
        poster = pygame.transform.scale(poster, (self.window_width - 10, (self.window_height - 10)*(27/32)))
        # Using blit to copy content from one surface to other
        #pygame.draw.rect(self.scrn, (255,255,255), (5,5,self.window_width - 10, self.window_height - 10), border_radius=12)
        self.scrn.blit(twilight,(0,0))
        self.scrn.blit(poster,(5, (self.window_height*(5/32))))

        x = 5
        y = (self.window_height*(5/32))
        border_colors = [(.1*255,.1*255,.1*255),(.3*255,.3*255,.3*255),(.6*255,.6*255,.6*255),(1*255,1*255,1*255)]
        for j in range(4):
            i = 3 - j
            pygame.draw.rect(self.scrn, border_colors[j], (x - (1*i), y - (1*i), (self.window_width - 10) + (2*i), (self.window_height - 10)*(27/32) + (2*i)), 1, border_radius=4)

        # paint screen one time
        pygame.display.flip()
        status = True
        oldEpoch = time.time()
        while (status):
            if time.time() - oldEpoch >= .5:
                print("Checking for image")
                oldEpoch = time.time()
                self.check_for_image()
            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for i in pygame.event.get():

                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if i.type == pygame.QUIT:
                    status = False

if __name__=="__main__":
    mainLoop().main_loop()

    pygame.quit()