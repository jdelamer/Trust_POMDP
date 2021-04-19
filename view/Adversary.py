import random
from tkinter import *
from PIL import Image, ImageTk

from view.EstimatedPosition import EstimatedPosition


class Adversary:
    """
    Class representing an agent for the GUI.
    """

    def __init__(self, canvas, position, color):
        """
        Initializing the class.
        :param canvas: The canvas where the agent will be shown.
        :param position: Position int he environment.
        """
        self.canvas = canvas
        self.position = position
        self.estimated_positions = []
        self.color = color

        im_temp = Image.open("./img/UAV_red.png")
        self.aspect_ratio = im_temp.width / im_temp.height
        im_temp = self.resize_img(im_temp)

        self.im = ImageTk.PhotoImage(im_temp)
        self.position_canvas = self.calculate_position_canvas(self.position)

        self.id = self.canvas.create_image(int(self.position_canvas[0]),
                                           int(self.position_canvas[1]),
                                           image=self.im, anchor=CENTER)

    def move(self, new_position):
        """ Move the agent on the GUI"""
        pos_canvas = self.calculate_position_canvas(new_position)
        self.canvas.move(self.id, int(pos_canvas[0] - self.position_canvas[0]), int(pos_canvas[1] - self.position_canvas[1]))
        self.position = new_position
        self.position_canvas = pos_canvas

    def calculate_position_canvas(self, position):
        """
        Calculate the position in the canvas considering the padding.
        :return: position
        """
        pos_canvas = [int(self.canvas.padding + position[0] * self.canvas.scx + self.im.width()/2),
                      int(self.canvas.padding + position[1] * self.canvas.scy + self.im.height()/2*self.aspect_ratio)]
        return pos_canvas

    def resize_img(self, img):
        """
        Resize the image to take into account the size of the canvas.
        Consider the ratio of the image
        :param img: Image to resize
        :return: new image
        """
        new_height = int(self.canvas.scy)
        new_width = int(self.canvas.scx * self.aspect_ratio)

        if new_width > self.canvas.scx:
            ratio = self.canvas.scx / new_width
            new_width *= ratio
            new_height *= ratio

        img = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        return img

    def update_estimated_position(self, positions):
        """
        Update the estimated position of the agents
        :param positions: list of estimated positions
        """
        for ep in self.estimated_positions:
            self.canvas.delete(ep.rectangle)
        self.estimated_positions = []
        for position in positions:
            if position == self.position:
                pos_canvas = [int(self.canvas.padding + position[0] * self.canvas.scx),
                              int(self.canvas.padding + position[1] * self.canvas.scy)]
                size = [self.canvas.scx, self.canvas.scy]
                expected_position = EstimatedPosition(self.canvas, pos_canvas, size, self.color, False)
                self.estimated_positions.append(expected_position)
            else:
                pos_canvas = [int(self.canvas.padding + position[0] * self.canvas.scx),
                              int(self.canvas.padding + position[1] * self.canvas.scy)]
                size = [self.canvas.scx, self.canvas.scy]
                expected_position = EstimatedPosition(self.canvas, pos_canvas, size, self.color)
                self.estimated_positions.append(expected_position)