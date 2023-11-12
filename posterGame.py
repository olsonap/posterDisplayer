import pygame
import requests
import time
import io
from urllib.request import urlopen
import logging

class MainLoop:
    def __init__(self):
        self.window_width = int(1080 / 3)
        self.window_height = int(1960 / 3)
        self.movie_id = None
        self.scrn = pygame.display.set_mode((self.window_width, self.window_height))

    def check_for_image(self):
        try:
            response = requests.get(f"http://localhost:8000/get-current-movie/{self.movie_id}")
            data = response.json()
            msg = data.get('msg')

            if msg:
                movie_id = msg.get('movie_id')

                if movie_id and movie_id != self.movie_id:
                    logging.info("Image has changed, updating image")
                    self.update_image(msg)
                elif not movie_id:
                    logging.debug("No movie selected, displaying default")

            else:
                logging.error("Error trying to reach server")
            return

        except Exception as e:
            logging.error(f"Error in check_for_image: {str(e)}")
            return

    def update_image(self, data):
        try:
            self.movie_id = data['movie_id']
            self.poster_path = data['poster_path']

            image_str = urlopen(self.poster_path).read()
            image_file = io.BytesIO(image_str)
            image = pygame.image.load(image_file)

            poster = pygame.transform.scale(image, (self.window_width - 10, int((self.window_height - 10) * (27 / 32))))
            self.scrn.blit(poster, (5, int(self.window_height * (5 / 32))))

            pygame.display.flip()
            return

        except Exception as e:
            logging.error(f"There was an error while trying to update the image: {str(e)}")
            return

    def begin(self):
        pygame.init()
        pygame.display.set_caption('image')

        twilight = pygame.image.load('static/theatername.jpg').convert()
        poster = pygame.image.load('static/default.jpeg').convert()

        twilight = pygame.transform.scale(twilight, (self.window_width, int(self.window_height * (5 / 32))))
        poster = pygame.transform.scale(poster, (self.window_width - 10, int((self.window_height - 10) * (27 / 32))))

        self.scrn.blit(twilight, (0, 0))
        self.scrn.blit(poster, (5, int(self.window_height * (5 / 32))))

        x = 5
        y = int(self.window_height * (5 / 32))
        border_colors = [(.1 * 255, .1 * 255, .1 * 255), (.3 * 255, .3 * 255, .3 * 255),
                         (.6 * 255, .6 * 255, .6 * 255), (1 * 255, 1 * 255, 1 * 255)]

        for j in range(4):
            i = 3 - j
            pygame.draw.rect(self.scrn, border_colors[j], (x - (1 * i), y - (1 * i),
                                                           (self.window_width - 10) + (2 * i),
                                                           int((self.window_height - 10) * (27 / 32)) + (2 * i)),
                             1, border_radius=4)

        pygame.display.flip()

        self.main_loop()
        return

    def main_loop(self):
        status = True
        old_epoch = time.time()

        while status:
            if time.time() - old_epoch >= 0.5:
                old_epoch = time.time()
                self.check_for_image()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    status = False
        return

if __name__ == "__main__":
    MainLoop().begin()
    pygame.quit()
