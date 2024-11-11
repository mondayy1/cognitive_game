import pygame
import random
import time

class WMIGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.time = 0
        self.font = pygame.font.Font(None, 36)
        self.total_questions = 5  # 총 5번의 문제

    def run(self):
        correct_answers = 0
        total_attempts = 0

        for question_number in range(1, self.total_questions + 1):
            # 임의의 숫자 배열 생성 (숫자 4개)
            sequence = [random.choice(range(1, 10)) for _ in range(4)]
            correct_sequence = ', '.join(map(str, sequence))
            
            # 숫자 배열을 3초간 보여주기
            self.show_sequence(correct_sequence, correct_answers)
            
            # 숫자 배열을 숨기고, 사용자가 입력하도록 유도
            user_answer = self.get_user_input()
            
            # 정답 확인
            if user_answer == correct_sequence:
                correct_answers += 1
                self.score += 10
                result_text = "Correct!"
                result_color = (0, 255, 0)
            else:
                result_text = "Wrong!"
                result_color = (255, 0, 0)
            
            # 결과 표시
            self.show_result(result_text, result_color)
            
            total_attempts += 1
            pygame.time.wait(1000)  # 1초간 결과를 표시 후 넘어감

        # 점수 계산
        self.score = (correct_answers / self.total_questions) * 100  # 정답 비율
        print(f"Final Score: {self.score}")

    def show_sequence(self, sequence, correct_answers):
        """3초간 숫자 배열을 보여주는 함수"""
        self.screen.fill((255, 255, 255))
        
        # 숫자 배열 텍스트
        sequence_text = self.font.render(f"Remember this: {sequence}", True, (0, 0, 0))
        self.screen.blit(sequence_text, (100, 100))

        # 점수 텍스트
        score_text = self.font.render(f"Score: {self.score:.2f}", True, (0, 0, 0))
        self.screen.blit(score_text, (100, 50))

        pygame.display.flip()
        pygame.time.wait(3000)  # 3초간 보여주기

        self.screen.fill((255, 255, 255))  # 숫자 숨기기
        pygame.display.flip()

    def get_user_input(self):
        """사용자가 차례대로 숫자를 입력하도록 받는 함수 (5초 제한)"""
        start_time = time.time()
        user_input = []
        input_active = True

        while input_active:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, 5 - elapsed_time)  # 남은 시간 계산
            self.update_timer(remaining_time)  # 남은 시간 화면에 업데이트

            if elapsed_time >= 5:
                break  # 5초가 지나면 입력 종료

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter를 누르면 입력을 종료
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        if user_input:
                            user_input[-1] = user_input[-1][:-1]  # 마지막 숫자 지우기
                    elif event.key == pygame.K_SPACE:
                        user_input.append('')  # 스페이스바로 구분된 새로운 숫자 입력 시작
                    elif event.unicode.isdigit():
                        if not user_input:  # 첫 번째 숫자 입력시 바로 추가
                            user_input.append(event.unicode)
                        else:
                            user_input[-1] += event.unicode  # 스페이스바로 구분된 숫자에 추가

            # 입력한 텍스트 화면에 실시간으로 표시
            self.screen.fill((255, 255, 255), (100, 200, 600, 50))  # 기존 텍스트 지우기
            user_input_text = ' '.join(user_input)
            user_input_surface = self.font.render(f"Enter the sequence: {user_input_text}", True, (0, 0, 255))
            self.screen.blit(user_input_surface, (100, 200))

            # 추가: 입력 예시 및 설명을 화면에 표시
            example_text = self.font.render("Enter numbers separated by spaces", True, (0, 0, 0))
            self.screen.blit(example_text, (100, 150))

            pygame.display.flip()

        return ', '.join(user_input).strip()  # 공백으로 구분된 숫자 입력 문자열로 반환

    def show_result(self, result_text, result_color):
        """정답/오답에 대한 피드백을 화면에 보여주는 함수"""
        result_surface = self.font.render(result_text, True, result_color)
        self.screen.blit(result_surface, (100, 300))
        pygame.display.flip()

    def update_timer(self, remaining_time):
        """남은 시간 표시하는 함수"""
        self.screen.fill((255, 255, 255), (100, 100, 200, 50))  # 기존 타이머 지우기
        timer_text = self.font.render(f"Time: {remaining_time:.2f}", True, (0, 0, 0))  # 소수점 둘째 자리까지 표시
        self.screen.blit(timer_text, (100, 100))
        pygame.display.flip()
