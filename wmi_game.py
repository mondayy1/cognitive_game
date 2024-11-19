import pygame
from random import randrange, shuffle

class WMIGame:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.start_button = pygame.Rect(0, 0, 50, 50) # 시작 버튼
        self.start_button.center = (120, 120) # 시작 버튼 중심
        self.number_buttons = [] 
        self.curr_level = 1
        self.display_time = None
        self.start_ticks = None
        self.start = False
        self.hidden = False
        self.running = True
        self.score = 0

    # 난이도 조정 
    def setup(self, level):
        """게임 설정: 숫자와 시간 초기화"""
        self.display_time = max(5 - (level // 3), 1)  # 숫자 표시 시간
        number_count = min((level // 3) + 5, 20) # 숫자 개수 (최대 20개)
        self.shuffle_grid(number_count) # 숫자 버튼 화면 배치

    def shuffle_grid(self, number_count):
        """숫자 버튼을 화면에 랜덤으로 배치"""
        rows, columns = 4, 4  # 행렬 크기를 4x4로 설정
        cell_size, button_size = 120, 100  # 셀 크기와 버튼 크기 조정
        screen_left_margin, screen_top_margin = 50, 50  # 여백 조정


        grid = [[0 for _ in range(columns)] for _ in range(rows)]
        number = 1

        while number <= number_count:
            row_idx, col_idx = randrange(0, rows), randrange(0, columns)
            if grid[row_idx][col_idx] == 0:
                grid[row_idx][col_idx] = number
                center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
                center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)
                button = pygame.Rect(0, 0, button_size, button_size)
                button.center = (center_x, center_y)
                self.number_buttons.append(button)
                number += 1

    def display_start_screen(self):
        """시작 화면 표시"""
        pygame.draw.circle(self.screen, (255, 255, 255), self.start_button.center, 60, 5)


    def display_game_screen(self):
        """게임 화면 표시"""
        if not self.hidden:
            elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
            if elapsed_time > self.display_time:
                self.hidden = True

        for idx, rect in enumerate(self.number_buttons, start=1):
            if self.hidden:
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
            else:
                cell_text = self.font.render(str(idx), True, (255, 255, 255))
                text_rect = cell_text.get_rect(center=rect.center)
                self.screen.blit(cell_text, text_rect)

    def check_buttons(self, pos):
        """클릭한 버튼 확인"""
        if self.start:
            for button in self.number_buttons:
                if button.collidepoint(pos):
                    if button == self.number_buttons[0]:
                        self.number_buttons.pop(0)
                        if not self.hidden:
                            self.hidden = True
                        if len(self.number_buttons) == 0:
                            self.curr_level += 1
                            self.score += 10  # 점수 추가
                            self.start = False
                            self.hidden = False
                            self.setup(self.curr_level)
                    else:
                        self.running = False
                        self.show_game_over()
                    break
        elif self.start_button.collidepoint(pos):
            self.start = True
            self.start_ticks = pygame.time.get_ticks()

    def show_game_over(self):
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        """게임 실행"""
        self.setup(self.curr_level)
        while self.running:
            self.screen.fill((0, 0, 0))
            if self.start:
                self.display_game_screen()
            else:
                self.display_start_screen()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.check_buttons(event.pos)
