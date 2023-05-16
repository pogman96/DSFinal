from typing import Union

import pygame

from .COLORS import BLUE, BROWN, BLACK
from .llist import LList, LLNode
from .shapes import Rectangle


class Queue(LList):
    def __init__(self, surface, font, nodeType=LLNode):
        super().__init__(surface, font, nodeType)
        self.rect_width = 120
        self.rect_height = 40
        self.rect_spacing = 5
        surface_x, surface_y = surface.get_size()
        self.queue_pos = (surface_x // 2 - self.rect_width // 2, surface_y - self.rect_height * 2)
        self.button_pos = (10, 10)
        self.button_height = 40
        self.button_width = 150
        self.button_spacing = 5

    def enqueue(self, val):
        """Adds an element to the end of the queue.

        Args:
            val (any): Value to add to the queue.

        """
        self.add(val)

    def dequeue(self) -> Union[bool, any]:
        """Removes and returns the element at the front of the queue.

        Returns:
            Union[bool, any]: False if the queue is empty, otherwise the value at the front of the queue.

        """
        return self.remove_at(1)

    def setup(self):
        btn_names = ["enqueue", "dequeue", "exit"]
        self.add_buttons(btn_names)

    def _buttonMenu(self, event):
        for btn in self.btns:
            btn_obj = self.btns[btn]
            btn_obj.draw(self.surface, width=2)
            btn_obj.draw_text(self.surface, btn.capitalize(), self.font, BLACK)

            if btn_obj.handle_event(event):
                if btn == "enqueue":
                    self.enqueue(self.node_count + 1)
                elif btn == "dequeue":
                    self.dequeue()
                elif btn == "exit":
                    return "exit"

    def _visualize(self, event):
        self.surface.fill(BLUE)

        if self._buttonMenu(event) == "exit":
            return "exit"

        curr = self.head

        x, y = self.queue_pos

        while curr is not None:
            rect = Rectangle((x, y), BROWN, self.rect_width, self.rect_height)
            curr.shape = rect
            curr.update_shape()
            curr.draw(self.surface)
            curr.draw_text(self.surface, str(curr.value), self.font, BLACK)

            if curr.shape.handle_event(event):
                self.remove_at(1)

            curr = curr.next
            y -= self.rect_height + self.rect_spacing

        pygame.display.update()
