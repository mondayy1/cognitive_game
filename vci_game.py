# vci_game.py
import pygame
import random
import time

class VCIGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.time = 0

    def run(self):
        font = pygame.font.Font(None, 36)
        questions = [("cat", "dog", "bird", "animal"),
                     ("apple", "banana", "grape", "fruit")]
        correct_answers = 0
        start_time = time.time()

        for question in questions:
            words, answer = question[:-1], question[-1]
            self.screen.fill((255, 255, 255))
            for idx, word in enumerate(words):
                text = font.render(word, True, (0, 0, 0))
                self.screen.blit(text, (100, 100 + 50 * idx))

            pygame.display.flip()
            user_answer = self.get_user_input()

            if user_answer == answer:
                correct_answers += 1

            pygame.time.wait(1000)

        end_time = time.time()
        reaction_time = (end_time - start_time) / len(questions)

        self.score = 80 if correct_answers >= len(questions) * 0.8 else 0
        if reaction_time <= 10:
            self.score += 20

    def get_user_input(self):
        # 임의의 사용자 입력 시뮬레이션
        return random.choice(["animal", "fruit"])
