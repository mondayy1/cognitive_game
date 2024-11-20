import pygame
import time
import os

class VCIGame:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.time = 0
        self.total_questions = 10
        # assets 폴더 경로 설정
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")

    def run(self):
        font = pygame.font.Font(None, 36)

        # 문제별 이미지 파일 매핑
        question_images = {
            1: ["apple.png", "banana.png", "grape.png", "watermelon.png"],  # 1번 문제: fruit
            2: ["cat.png", "dog.png", "rabbit.png", "bird.png"],            # 2번 문제: animal
            3: ["doctor.png", "police.png", "chef.png", "teacher.png"],     # 3번 문제: job
            4: ["chair.png", "bed.png", "table.png", "sofa.png"],           # 4번 문제: furniture
            5: ["guitar.png", "piano.png", "drum.png", "violin.png"],       # 5번 문제: instrument
            6: ["mountain.png", "flower.png", "river.png", "tree.png"],     # 6번 문제: nature
            7: ["sight.png", "hearing.png", "smell.png", "tasting.png"],    # 7번 문제: sense (어려움)
            8: ["plant.png", "sakura.png", "sun.png", "butterfly.png"],     # 8번 문제: spring (어려움)
            9: ["wave.png", "lightning.png", "fire.png", "Wind.png"],       # 9번 문제: energy (어려움)
            10: ["free.png", "love.png", "justice.png", "book.png"],        # 10번 문제 : concept or philosophy (매우 어려움)
        }

        for question_number in range(1, self.total_questions + 1):
            # 화면 초기화
            self.screen.fill((255, 255, 255))

            # 이미지 파일 가져오기
            images = question_images.get(question_number, [])  # 문제 번호에 해당하는 이미지 리스트 가져오기
            if not images:
                print(f"No images found for question {question_number}.")
                continue

            # 문제 번호 표시
            question_text = f"Question {question_number} / {self.total_questions}"
            question_surface = font.render(question_text, True, (0, 0, 0))
            self.screen.blit(question_surface, (200, 20))  # 화면 상단에 문제 번호 표시

            # 네 개의 이미지를 화면에 표시
            positions = [(190, 100), (390, 100), (190, 300), (390, 300)]
            for idx, image_file in enumerate(images):
                image_path = os.path.join(self.assets_path, image_file)
                if not os.path.exists(image_path):
                    print(f"Image not found: {image_path}")
                    continue
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (150, 150))
                self.screen.blit(image, positions[idx])

            pygame.display.flip()  # 모든 이미지를 화면에 표시

            # 사용자 입력 받기
            user_answer = self.get_user_input()

            # 정답 확인
            if question_number == 1 and user_answer == "fruit":
                self.score += 10
            elif question_number == 2 and user_answer == "animal":
                self.score += 10
            elif question_number == 3 and user_answer == "job":
                self.score += 10
            elif question_number == 4 and user_answer == "furniture":
                self.score += 10
            elif question_number == 5 and user_answer == "instrument":
                self.score += 10
            elif question_number == 6 and user_answer == "nature":
                self.score += 10
            elif question_number == 7 and user_answer == "sense":
                self.score += 10
            elif question_number == 8 and user_answer == "spring":
                self.score += 10
            elif question_number == 9 and user_answer == "energy":
                self.score += 10
            elif question_number == 10 and user_answer == "concept" or user_answer == "philosophy":
                self.score += 10 
            else:
                self.score += 0

            # 잠깐 대기 후 다음 문제로 이동
            pygame.time.wait(1000)

        # 모든 문제 끝난 후 결과 표시
        self.show_final_score()

    def get_user_input(self):
        user_input = ""
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(250, 500, 300, 50)
        input_active = True

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

            pygame.draw.rect(self.screen, (255, 255, 255), input_box)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)

            text_surface = font.render(user_input, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

            pygame.display.flip()

        return user_input.strip().lower()

    def show_final_score(self):
        """모든 문제 완료 후 최종 점수 표시."""
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 50)
        final_score_text = f"Your VCI Score: {self.score}"
        final_score_surface = font.render(final_score_text, True, (0, 0, 0))
        self.screen.blit(final_score_surface, (200, 250))
        pygame.display.flip()
        pygame.time.wait(3000)
