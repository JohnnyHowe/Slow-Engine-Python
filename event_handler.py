"""Module for handling pygame events and adding listeners.
Allows listeners to be called when a pygame event occurs.
"""
import pygame
from slowEngine.display import Display
from slowEngine.vector2 import Vector2


class _EventHandler:
    """The handler for the pygame events."""

    events = None
    listeners = None

    def __init__(self):
        self.events = []
        self.listeners = {}

        self.add_listener(pygame.VIDEORESIZE, lambda e: Display.set_window(Vector2(e.w, e.h)))
        self.add_listener(pygame.QUIT, lambda e: quit())

    def add_listener(self, event_type, function):
        """ Add a listener for the events.
        The listener is to be a function that takes the pygame event associated with it. """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(function)

    def run(self):
        """ Run the event handler.
        Should the listeners be run? """
        self.events = pygame.event.get()
        for event in self.events:
            if event.type in self.listeners:
                for function in self.listeners[event.type]:
                    function(event)


EventHandler = _EventHandler()
