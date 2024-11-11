import pygame
import random
import time

class PSIGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.time = 0
        self.font = pygame.font.Font(None, 36)

        # 도형의 위치를 클래스 속성으로 정의
        self.circle_pos = None
        self.triangle_points = None
        self.rectangle_pos = None

    def run(self):
        shapes = ["circle", "triangle", "rectangle"]
        correct_answers = 0
        total_questions = 10

        for question_number in range(1, total_questions + 1):
            target_shape = random.choice(shapes)
            self.screen.fill((255, 255, 255))

            # 목표 도형과 현재 점수, 문제 번호 표시
            question_text = self.font.render(f"Click {target_shape}", True, (0, 0, 0))
            self.screen.blit(question_text, (100, 50))

            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (400, 50))

            question_number_text = self.font.render(f"Question: {question_number}/{total_questions}", True, (0, 0, 0))
            self.screen.blit(question_number_text, (100, 10))

            # 도형 순서 랜덤화
            random.shuffle(shapes)  # 도형 순서를 매번 랜덤으로 섞음

            # 도형들 그리기
            self.draw_shapes(shapes)  # 랜덤 순서대로 도형 그리기
            pygame.display.flip()

            # 사용자 클릭 또는 타임아웃 처리
            user_click, clicked_within_time, waste_time = self.get_user_click(target_shape, timeout=3)

            # 정답 여부에 따른 피드백 표시
            if clicked_within_time and user_click == target_shape:
                correct_answers += 1
                result_text = "Correct!"
                result_color = (0, 255, 0)  # 초록색
                self.score += 10  # 정답 시 10점 추가
            else:
                result_text = "Wrong!"
                result_color = (255, 0, 0)  # 빨간색

            self.time += waste_time

            # 결과 텍스트 화면에 표시
            result_surface = self.font.render(result_text, True, result_color)
            self.screen.blit(result_surface, (100, 300))
            pygame.display.flip()
            pygame.time.wait(1000)  # 1초 동안 결과 표시 후 다음 문제로 이동

    def draw_shapes(self, shapes_order):
        # 화면 상에 도형들이 겹치지 않도록 위치 설정
        used_positions = []  # 이미 사용된 위치들 기록

        # 원 위치와 크기 랜덤 설정 (원 크기 키움)
        circle_radius = random.randint(50, 80)  # 원 크기를 50~80 사이로 키움
        self.circle_pos = self.get_random_position(used_positions, circle_radius)
        used_positions.append(("circle", self.circle_pos, circle_radius))

        # 삼각형 꼭짓점들 랜덤 설정
        self.triangle_points = [
            self.get_random_position(used_positions, 0),
            self.get_random_position(used_positions, 0),
            self.get_random_position(used_positions, 0)
        ]
        used_positions.append(("triangle", self.triangle_points, 0))

        # 사각형 위치와 크기 랜덤 설정 (사각형 크기 키움)
        rectangle_width = random.randint(80, 120)  # 사각형 크기를 80~120 사이로 키움
        rectangle_height = random.randint(80, 120)  # 사각형 크기를 80~120 사이로 키움
        self.rectangle_pos = self.get_random_position(used_positions, max(circle_radius, rectangle_width, rectangle_height))
        used_positions.append(("rectangle", self.rectangle_pos, (rectangle_width, rectangle_height)))

        # 순서대로 도형 그리기
        for shape in shapes_order:
            if shape == "circle":
                pygame.draw.circle(self.screen, (255, 0, 0), self.circle_pos, circle_radius)
            elif shape == "triangle":
                pygame.draw.polygon(self.screen, (0, 255, 0), self.triangle_points)
            elif shape == "rectangle":
                pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(self.rectangle_pos[0], self.rectangle_pos[1], rectangle_width, rectangle_height))

    def get_random_position(self, used_positions, padding):
        # 무작위 위치를 생성하고, 이미 사용된 위치들과 겹치지 않도록 처리
        screen_width, screen_height = self.screen.get_size()
        while True:
            x = random.randint(100 + padding, screen_width - padding)
            y = random.randint(100 + padding, screen_height - padding)
            is_valid = True

            # 사용된 위치들과 겹치는지 확인
            for pos in used_positions:
                shape, position, size = pos
                if shape == "circle":
                    circle_x, circle_y = position
                    radius = size
                    if (x - circle_x) ** 2 + (y - circle_y) ** 2 <= (radius + padding) ** 2:
                        is_valid = False
                        break
                elif shape == "rectangle":
                    rect_x, rect_y = position
                    rect_width, rect_height = size
                    if rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height:
                        is_valid = False
                        break
                elif shape == "triangle":
                    if self.point_in_triangle((x, y), *position):
                        is_valid = False
                        break

            if is_valid:
                return x, y

    def get_user_click(self, target_shape, timeout=3):
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, timeout - elapsed_time)  # 남은 시간 계산
            self.update_timer(remaining_time)  # 남은 시간 화면에 업데이트

            if elapsed_time >= timeout:
                return None, False, elapsed_time  # 시간 초과로 인한 타임아웃 처리

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    # 원 클릭 확인
                    if self.circle_pos and (x - self.circle_pos[0]) ** 2 + (y - self.circle_pos[1]) ** 2 <= 80 ** 2:
                        return "circle", True, elapsed_time

                    # 삼각형 클릭 확인
                    if self.triangle_points and self.point_in_triangle((x, y), *self.triangle_points):
                        return "triangle", True, elapsed_time

                    # 사각형 클릭 확인
                    if self.rectangle_pos and pygame.Rect(self.rectangle_pos[0], self.rectangle_pos[1], 120, 120).collidepoint(x, y):
                        return "rectangle", True, elapsed_time

    def update_timer(self, remaining_time):
        self.screen.fill((255, 255, 255), (100, 100, 200, 50))  # 이전 타이머 지우기
        timer_text = self.font.render(f"Time: {remaining_time:.2f}", True, (0, 0, 0))  # 소수점 둘째 자리까지 표시
        self.screen.blit(timer_text, (100, 100))
        pygame.display.flip()

    def point_in_triangle(self, pt, v1, v2, v3):
        """삼각형 내부에 점이 있는지 확인하는 함수"""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(pt, v1, v2)
        d2 = sign(pt, v2, v3)
        d3 = sign(pt, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)
