from typing import Union
import pygame
import random

from .node import Node

from .COLORS import BLUE, BROWN, BLACK

from .shapes import Shape, Rectangle, Circle


class LLNode(Node):
    def __init__(self, data=None, shape: Shape=None):
        super().__init__(data)
        self.next = None
        self.shape = shape

    def draw(self, surface):
        self.shape.draw(surface)
        
    def draw_text(self, surface, text, font, color=BLACK):
        self.shape.draw_text(surface, text, font, color)
        
    def draw_outline(self, surface, color=BLACK):
        self.shape.draw_outline(surface, color)
        
    def update_shape(self):
        self.shape.update_rect()
        
    def handle_event(self, event):
        return self.shape.handle_event(event)
    
    def resize(self, width, height):
        self.shape.set_width(width)
        self.shape.set_height(height)
        self.update_shape()
        
    def move(self, x, y):
        self.shape.set_x(x)
        self.shape.set_y(y)
        self.update_shape()        

class LList:
    def __init__(self, surface, font, nodeType=LLNode):
        self.head = None
        self.tail = None
        self.nodeType = nodeType
        self.node_count = 0    
        self.surface = surface
        self.font = font

    def add(self, val):
        """Adds to the end of the LList

        Args:
            val (any): value to add

        """
        node = self.nodeType(val)
        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        
        self.node_count += 1

    def insert_node(self, value, pos):
        """Insert a node with the given value at the specified position in the linked list"""
        if self.head is None:
            self.add(value)
            return

        
        if pos < 1 or pos > self.node_count + 1:
            print("Invalid position")
            return

        new_node = self.nodeType(value)
        
        if pos == 1:
            new_node.next = self.head
            self.head = new_node
        else:
            current_node = self.head
            for i in range(1, pos-1):
                current_node = current_node.next
            new_node.next = current_node.next
            current_node.next = new_node
            
            if current_node == self.tail:
                self.tail = new_node

        self.node_count += 1
    
    def preadd(self, val, **kwargs):
        """Adds to the front of the LList

        Args:
            val (any): value to add

        """
        node = self.nodeType(val, **kwargs)
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = node
            
        self.node_count += 1
        
    def remove_tail(self) -> Union[bool, any]:
        """Removes the tail of the LList
    
        Returns:
            Union[bool, any]: False if LList is empty, otherwise the value removed
    
        """
        if self.head is None:
            return False
        
        self.node_count -= 1
        
        if self.head == self.tail:
            temp_value = self.head.value
            self.head = None
            self.tail = None
            return temp_value
        
        node = self.head
        while node.next.next:
            node = node.next
        
        temp_value = node.next.value
        node.next = None
        self.tail = node
        
        return temp_value
                
    

    def remove(self, val) -> Union[bool, any]:
        """Removes the first instance of val from the LList

        Args:
            val (any): value to remove

        Returns:
            Union[bool, any]: False if val is not in LList, otherwise the value removed

        """
        if self.head is None:
            return False

        temp_node = self.head

        if self.head.value == val:
            self.head = self.head.next
            return temp_node.value

        node = self.head
        while node.next:
            temp_node = node.next
            
            if node.next.value == val:
                node.next = node.next.next
                self.node_count -= 1
                return temp_node.value
            
            node = node.next

            
        return False
    
    def remove_at(self, pos) -> Union[bool, any]:
        """Removes the node at the specified position in the linked list
        
        Args:
            pos (int): position of the node to remove
            
        Returns:
            Union[bool, any]: False if LList is empty or pos is invalid, otherwise the value removed"""
        if self.head is None:
            return False
        
        if pos < 1 or pos > self.node_count + 1:
            return False

        self.node_count -= 1
        
        if pos == 1:
            temp_value = self.head.value
            self.head = self.head.next
            return temp_value
        
        current_node = self.head
        
        for i in range(1, pos-1):
            current_node = current_node.next
            
        temp_value = current_node.next.value
        current_node.next = current_node.next.next
        
        if current_node.next is None:
            self.tail = current_node
            
            
        return temp_value
        

    def peek(self):
        """Returns the first value in the LList

        Returns:
            Union[bool, any]: False if LList is empty, otherwise the first value

        """
        if self.head is None:
            return False

        return self.head.value

    def is_empty(self):
        """Returns True if LList is empty, False otherwise"""
        return self.head is None
            
    def __str__(self) -> str:
        node = self.head
        output = []
        while node:
            output.append(str(node.value))
            node = node.next

        output.append("None")
        return "->".join(output)
    
    def setup(self):
        self.add_btn = Rectangle((10,10), BLACK, 110, 40)
        self.add_btn.draw_text(self.surface, "Add", self.font, BLACK)
        
        self.insert_btn = Rectangle((125,10), BLACK, 130, 40)
        self.insert_btn.draw_text(self.surface, "Insert", self.font, BLACK)

        self.exit_btn = Rectangle((260,10), BLACK, 70, 40)
        self.exit_btn.draw_text(self.surface, "Exit", self.font, BLACK)
        
        self.btns = {"add": self.add_btn, "insert": self.insert_btn, "exit": self.exit_btn}
        
    def _buttonMenu(self, event):
        for btn in self.btns:
            btn_obj = self.btns[btn]
            btn_obj.draw(self.surface, width=2)
            btn_obj.draw_text(self.surface, btn.capitalize(), self.font, BLACK)
            
            if btn_obj.handle_event(event):
                match btn:
                    case "add":
                        self.add(self.node_count + 1)
                    case "insert":
                        self.insert_node(self.node_count + 1, random.randint(1, self.node_count + 1))
                    case "exit":
                        return "exit"
        
    def visualize(self):
        self.setup()
        while True:
            for event in pygame.event.get():
                if self._visualize(event) == "exit":
                    return
        
    def _visualize(self, event):
        self.surface.fill(BLUE)
        
        if self._buttonMenu(event) == "exit":
            return "exit"
        
        curr = self.head
        
        x = 100
        y = 250
        
        prevNode = None
        pos = 1
        
        while curr is not None:
            curr.shape = Circle((x, y), BROWN, 30)
            curr.move(x, y)
            curr.draw(self.surface)
            curr.draw_text(self.surface, str(curr.value), self.font, BLUE)
            curr.draw_outline(self.surface, BLACK)
            
            if curr.shape.handle_event(event):
                self.remove_at(pos)
                
            if prevNode is not None:
                # draw line
                n1 = prevNode
                n2 = curr
                
                # edge of n1
                x1 = n1.shape.pos[0] + n1.shape.radius
                y1 = n1.shape.pos[1]
                
                # edge of n2
                x2 = n2.shape.pos[0] - n2.shape.radius
                y2 = n2.shape.pos[1]
                
                pygame.draw.line(self.surface, BLACK, (x1, y1), (x2, y2), 2)
                
                
            prevNode = curr
            curr = curr.next
            x += 80
            pos += 1
            
        pygame.display.update()

