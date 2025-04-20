import pygame

class Animator:
    def __init__(self, animations_data: dict, scale_factor=1, animation_speed=700):
        """
        animations_data: dict dạng { "state": ("path_to_sprite", frame_count) }
        scale_factor: hệ số phóng to
        animation_speed: tổng thời gian để chạy hết 1 animation (ms)
        """
        self.scale_factor = scale_factor
        self.animation_speed = animation_speed
        self.animations = {}
        self.state = "idle"
        self.load_animations(animations_data)
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.avatar = self.animations[self.state][0]

        self.frame_w = 0
        self.frame_h = 0

        

    def load_animations(self, data):
        for state, (path, number_frame) in data.items():
            self.animations[state] = self.load_frames(path, number_frame)

    def load_frames(self, path, frame_count):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frame_w = sprite_sheet.get_width() // frame_count
        frame_h = sprite_sheet.get_height()
        self.frame_w, self.frame_h = frame_w, frame_h

        frames = [
            sprite_sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
            for i in range(frame_count)
        ]
        if self.scale_factor != 1:
            frames = [
                pygame.transform.scale(f, (frame_w * self.scale_factor, frame_h * self.scale_factor))
                for f in frames
            ]
        return frames

    def in_animate(self, velocity_x):
        now = pygame.time.get_ticks()
        total_frames = len(self.animations[self.state])
        delay = self.animation_speed // total_frames

        if now - self.last_update >= delay:
            self.frame_index = (self.frame_index + 1) % total_frames
            self.last_update = now

            frame = self.animations[self.state][self.frame_index]
            if velocity_x < 0:
                self.avatar = pygame.transform.flip(frame, True, False)
            else:
                self.avatar = frame

    def get_frame(self):
        return self.avatar
