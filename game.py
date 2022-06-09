# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from utils import *
# noinspection PyUnresolvedReferences
from constants import *
from rechargeables import *
from battery import Battery
from foil import Foil
from random import choice as choose


class Game:
    def __init__(self, b_font, s_font):
        self.big_font = b_font
        self.s_font = s_font
        self.items = [Battery(0, (500, 400), "drag me to the foil"), Foil((200, 400))]
        self.item_to_fill = "camera"
        self.money = 2
        self.money_goal = 50
        self.appliances_fixed = 0
        self.money_bar_rect = pygame.Rect(10, 10, WIDTH - 20, 40)
        self.current_rechargeable = Flashlight()
        self.next_rechargeable_rect = pygame.Rect(WIDTH - 370, HEIGHT - 100, 240, 60)
        self.buy_foil_rect = self.money_bar_rect.copy().move(0, 50)
        self.buy_foil_rect.w = 180
        self.buy_battery_rect = self.buy_foil_rect.copy().move(190, 0)
        self.restart_rect = self.money_bar_rect.copy().move(0, 50)
        self.restart_rect.w = 180
        self.restart_rect.right = self.money_bar_rect.right
        self.restart_money = self.money
        self.start_time = 0
        self.restart_items = self.items

    def draw_button(self, screen, rect, text):
        pygame.draw.rect(screen, DARKER_BLACK, rect.inflate((2, 2)))
        pygame.draw.rect(
            screen,
            BG_COLOR.lerp(
                (255, 255, 255), 0.06
            ).lerp(
                (0, 0, 0), 0.2 * rect.collidepoint(pygame.mouse.get_pos())
            ),
            rect
        )
        next_text = fetch_text(self.big_font, text, DARK_WHITE)
        screen.blit(next_text, next_text.get_rect(center=rect.center))

    def draw(self, screen: pygame.Surface):
        if self.start_time == 0:
            self.start_time = time()
        if self.money >= self.money_goal:
            set_current_screen("highscores")
            add_highscore(int((time()-self.start_time)*100)/100)
            self.start_time = 0
            return
        # money bar
        pygame.draw.rect(screen, DARKER_BLACK, self.money_bar_rect.inflate(2, 2))
        pygame.draw.rect(screen, BG_COLOR.lerp((255, 255, 255), 0.06), self.money_bar_rect)
        money_text = fetch_text(self.big_font, f"cash: {self.money}/{self.money_goal}", DARK_WHITE)
        screen.blit(money_text, money_text.get_rect(midleft=self.money_bar_rect.midleft).move(10, 0))

        # buy bars
        if self.appliances_fixed != 0:
            if self.money > 0:
                self.draw_button(screen, self.buy_foil_rect, "buy foil")
                self.draw_button(screen, self.buy_battery_rect, "buy case")
            else:
                self.draw_button(screen, self.restart_rect, "restart")

        # rechargeable
        self.current_rechargeable.draw(screen)
        if self.current_rechargeable.running():
            self.draw_button(screen, self.next_rechargeable_rect, "next appliance")

        # items
        for item in self.items:
            item.draw(screen, self.s_font)

    def next_appliance(self):
        self.restart_money = self.money
        self.restart_items = self.items.copy()
        self.appliances_fixed += 1
        if self.appliances_fixed > 3:
            self.current_rechargeable = choose(Rechargeable.__subclasses__())()
        elif self.appliances_fixed > 2:
            self.current_rechargeable = Blender()
        elif self.appliances_fixed > 1:
            self.current_rechargeable = Camera()
        else:
            self.current_rechargeable = Flashlight()

    @property
    def item_to_fill_image(self):
        if self.item_to_fill == "camera":
            return 0

    def handle_events(self, event: pygame.event.Event):
        def grab_effect(bat):
            add_shake((5, 5))
            bat.rot = 0
            for _ in range(25):
                add_particle(
                    (
                        rand(bat.rect.left, bat.rect.right),
                        rand(bat.rect.top, bat.rect.bottom)
                    ),
                    7,
                    ACCENT_COLOR
                )
            play_sound("electricity2.mp3", 0.3)
            if bat.message == "drag me to the foil":
                bat.message = "put me inside the flashlight"

        # next appliance
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_rechargeable.running():
                if self.next_rechargeable_rect.collidepoint(pygame.mouse.get_pos()):
                    self.money += self.current_rechargeable.reward
                    self.next_appliance()
            if self.appliances_fixed > 0:
                if self.money > 0:
                    if self.buy_foil_rect.collidepoint(pygame.mouse.get_pos()):
                        self.money -= 1
                        self.items.append(Foil((rand(0, 300), rand(200, HEIGHT - 100))))
                    if self.buy_battery_rect.collidepoint(pygame.mouse.get_pos()):
                        self.money -= 1
                        self.items.append(Battery(0, (rand(330, 600), rand(200, HEIGHT - 100))))
            if self.money == 0:
                if self.restart_rect.collidepoint(pygame.mouse.get_pos()):
                    self.money = self.restart_money
                    self.items = self.restart_items
                    for spot in self.current_rechargeable.glue_spots:
                        self.current_rechargeable.glue_spots[spot] = None

        # other stuff
        batteries = [item for item in self.items if isinstance(item, Battery)]
        foils = [item for item in self.items if isinstance(item, Foil)]
        for item in self.items.__reversed__():
            if item.handle_events(event):
                self.items.remove(item)
                self.items.append(item)
                return True

            # handle battery collision
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if isinstance(item, Battery):
                        if item.tier != 4:
                            for foil in foils:
                                if foil.rect.colliderect(item.rect):
                                    item.tier += 1
                                    self.items.remove(foil)
                                    item.selected = False
                                    grab_effect(item)
                                    return True
                    if isinstance(item, Foil):
                        for battery in batteries:
                            if battery.tier != 4:
                                if battery.rect.colliderect(item.rect):
                                    battery.tier += 1
                                    self.items.remove(item)
                                    battery.selected = False
                                    grab_effect(battery)
                                    return True

                    # rechargeables
                    if isinstance(item, Battery):
                        if self.current_rechargeable.glue_check(item):
                            item.selected = False
                            self.items.remove(item)
                            grab_effect(item)
                            return True

        # rechargeable takeout
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                take_battery = self.current_rechargeable.handle_events(event)
                if take_battery:
                    take_battery.selected = True
                    take_battery.grab_position = take_battery.x - pygame.mouse.get_pos()[0], \
                        take_battery.y - pygame.mouse.get_pos()[1]
                    self.items.append(take_battery)
                    grab_effect(take_battery)
                    return True
