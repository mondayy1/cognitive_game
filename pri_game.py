from prigame_env import PRIGameEnv
from stable_baselines3 import DQN
import pygame
import time
import random


class PRIGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.total_questions = 2
        self.env = PRIGameEnv()
        self.model = DQN.load("prigame_dqn_model")  # 학습된 모델 로드
        self.state = self.env.reset()
        self.current_difficulty = 1

    def generate_matrix(self, difficulty):
        """난이도에 따라 행렬 생성"""
        base_matrix = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

        if difficulty >= 2:
            base_matrix.append(['10', '11', '12'])  # 난이도 2: 행 추가
        if difficulty >= 3:
            base_matrix[0].extend(['A', 'B'])  # 난이도 3: 열 추가
        if difficulty >= 4:
            base_matrix.append(['C', 'D', 'E'])  # 난이도 4: 추가 행
        if difficulty >= 5:
            base_matrix = [[str(random.randint(1, 50)) for _ in range(len(base_matrix[0]))] 
                           for _ in range(len(base_matrix) + 1)]  # 난이도 5: 무작위 값

        return base_matrix

    def randomize_question(self, matrix):
        """문제에서 '?'의 위치를 랜덤하게 설정하고 정답을 반환"""
        question_matrix = [row[:] for row in matrix]
        random_pos = random.choice([(i, j) for i in range(len(matrix)) for j in range(len(matrix[0]))])
        row, col = random_pos
        answer = question_matrix[row][col]  # 정답
        question_matrix[row][col] = '?'  # 해당 위치를 '?'로 바꿈
        return question_matrix, answer

    def show_matrix(self, matrix):
        """화면에 행렬 표시"""
        cell_size = 100
        x_offset = 100
        y_offset = 100
        spacing = 10

        for row_idx, row in enumerate(matrix):
            for col_idx, item in enumerate(row):
                cell_x = x_offset + col_idx * (cell_size + spacing)
                cell_y = y_offset + row_idx * (cell_size + spacing)
                pygame.draw.rect(self.screen, (200, 200, 200), (cell_x, cell_y, cell_size, cell_size))
                text_surface = self.font.render(str(item), True, (0, 0, 0))
                self.screen.blit(text_surface, (cell_x + cell_size // 2 - 10, cell_y + cell_size // 2 - 10))
        pygame.display.flip()

    def get_user_input(self):
        """사용자 입력 받기"""
        user_text = ""
        input_active = True
        input_box_x = 600  # 입력 상자의 x 위치 설정
        input_box_y = 550  # 입력 상자의 y 위치 설정
        input_box_width = 200  # 입력 상자의 너비
        input_box_height = 50  # 입력 상자의 높이

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # 엔터키로 입력 종료
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:  # 백스페이스로 글자 삭제
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode  # 입력 추가
                        
            label_surface = self.font.render("Answer:", True, (0, 0, 0))
            self.screen.blit(label_surface, (input_box_x - 100, input_box_y + 15))  # 레이블 위치
            # 입력된 텍스트 표시
            input_surface = self.font.render(user_text, True, (0, 0, 0))
            pygame.draw.rect(self.screen, (200, 200, 200), (input_box_x, input_box_y, input_box_width, input_box_height))  # 입력 상자 그리기
            self.screen.blit(input_surface, (input_box_x + 5, input_box_y + 15))
            pygame.display.flip()  # 화면 업데이트

        return user_text.strip()

    def show_feedback(self, text, color):
        """피드백 메시지를 화면에 표시"""
        feedback_surface = self.font.render(text, True, color)
        self.screen.blit(feedback_surface, (250, 450))
        pygame.display.flip()
        pygame.time.wait(1000)

    def run(self):
        correct_answers = 0
        start_time = time.time()

        for _ in range(self.total_questions):
            matrix = self.generate_matrix(self.current_difficulty)
            question_matrix, answer = self.randomize_question(matrix)

            question_start_time = time.time()
            user_answer = None
            time_limit = 5  # 기본 남은시간 5초

            while user_answer is None:
                elapsed_time = time.time() - question_start_time
                remaining_time = max(0, time_limit - elapsed_time)  # 남은시간 계산
                self.screen.fill((255, 255, 255))

                # 남은 시간을 화면에 표시
                timer_surface = self.font.render(f"Time Left: {remaining_time:.1f}s", True, (255, 0, 0))
                self.screen.blit(timer_surface, (400, 50))  # 상단에 남은 시간 표시
                self.show_matrix(question_matrix)

                if remaining_time <= 0:
                    self.show_feedback("Time's up!", (255, 165, 0))
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        user_answer = self.get_user_input()
                        if user_answer == answer:
                            correct_answers += 1
                            self.show_feedback("Correct!", (0, 255, 0))
                        else:
                            self.show_feedback("Wrong!", (255, 0, 0))

                pygame.display.flip()  # 화면 업데이트

            # 상태 업데이트 및 난이도 조정
            self.state, _, _, _ = self.env.step(self.current_difficulty)
            self.current_difficulty = self.model.predict(self.state, deterministic=True)[0]

        end_time = time.time()
        reaction_time = (end_time - start_time) / self.total_questions

        self.score = 70 if correct_answers >= self.total_questions * 0.7 else 0
        if reaction_time <= 15:
            self.score += 15

        print(f"Final Score: {self.score}")
