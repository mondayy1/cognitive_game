import pygame
import random
import time

class PRIGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.time = 0
        self.font = pygame.font.Font(None, 36)
        self.total_questions = 5  # 총 5문제 (예시로 5개의 문제를 사용)
        
        # 문제 리스트 (행렬 형식과 정답)
        self.questions = [
            ([
                ['1', '2', '3'],
                ['4', '5', '?'],
                ['7', '8', '9']
            ], '6'),  # 정답은 6
            ([
                ['A', 'B', 'C'],
                ['D', 'E', '?'],
                ['G', 'H', 'I']
            ], 'F'),  # 정답은 F
            ([
                ['X', 'Y', 'Z'],
                ['P', 'Q', '?'],
                ['R', 'S', 'T']
            ], 'W'),  # 정답은 W
            ([
                ['10', '20', '30'],
                ['40', '50', '?'],
                ['70', '80', '90']
            ], '60'),  # 정답은 60
            ([
                ['Red', 'Blue', 'Green'],
                ['Yellow', 'Purple', '?'],
                ['Orange', 'Pink', 'Black']
            ], 'Brown')  # 정답은 Brown
        ]
        
    def run(self):
        correct_answers = 0
        start_time = time.time()

        for _ in range(self.total_questions):
            # 랜덤으로 문제를 선택
            matrix, answer = random.choice(self.questions)
            self.screen.fill((255, 255, 255))  # 화면을 흰색으로 초기화

            # 행렬 그리기
            self.show_matrix(matrix)
            
            # 사용자 입력 받기
            user_answer = self.get_user_input()

            # 정답 여부 확인 및 결과 출력
            if user_answer == answer:
                correct_answers += 1
                result_text = "Correct!"
                result_color = (0, 255, 0)  # 녹색
            else:
                result_text = "Wrong!"
                result_color = (255, 0, 0)  # 빨간색

            # 결과 텍스트 화면에 표시
            result_surface = self.font.render(result_text, True, result_color)
            self.screen.blit(result_surface, (100, 350))  # 결과는 좀 더 아래에 배치
            pygame.display.flip()
            pygame.time.wait(1000)  # 1초 동안 결과 표시

        end_time = time.time()
        reaction_time = (end_time - start_time) / self.total_questions

        self.score = 70 if correct_answers >= self.total_questions * 0.7 else 0
        if reaction_time <= 15:
            self.score += 15  # 반응 시간이 15초 이하일 경우 점수 보너스

        print(f"Final Score: {self.score}")

    def show_matrix(self, matrix):
        """3x3 행렬을 화면에 표시하는 함수"""
        cell_size = 100  # 각 셀 크기
        x_offset = 100  # 행렬 시작 x 좌표
        y_offset = 100  # 행렬 시작 y 좌표
        spacing = 10  # 셀 간격

        for row_idx, row in enumerate(matrix):
            for col_idx, item in enumerate(row):
                # 각 행렬 요소를 화면에 표시
                item_text = self.font.render(str(item), True, (0, 0, 0))
                x_pos = x_offset + col_idx * (cell_size + spacing)  # x 위치
                y_pos = y_offset + row_idx * (cell_size + spacing)  # y 위치
                self.screen.blit(item_text, (x_pos, y_pos))
        
        pygame.display.flip()

    def get_user_input(self):
        """사용자가 차례대로 숫자를 입력하도록 받는 함수"""
        user_text = ""
        input_active = True

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]  # 글자 하나 지우기
                    else:
                        user_text += event.unicode  # 입력한 글자를 추가
            
            # 입력한 텍스트 화면에 실시간으로 표시 (위치를 좀 더 아래로 이동)
            self.screen.fill((255, 255, 255), (100, 450, 600, 50))  # 기존 텍스트 지우기, 위치를 아래로 이동
            user_text_surface = self.font.render(user_text, True, (0, 0, 255))
            self.screen.blit(user_text_surface, (100, 450))  # 텍스트 입력창을 아래쪽에 배치
            pygame.display.flip()

        return user_text.strip()
