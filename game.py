# main.py
import pygame
from vci_game import VCIGame #x
from pri_game import PRIGame #o
from wmi_game import WMIGame #o
from psi_game import PSIGame #o

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cognitive Skills Test Game")

def main():
    # 게임 실행 순서 정의
    games = [PRIGame(screen)]
    total_score = 0

    for game in games:
        game.run()
        total_score += game.score
        avg_time = game.time / 10

    # test
    #print(avg_time)

    # 총점 표시
    font = pygame.font.Font(None, 50)
    text = font.render(f"Total Score: {total_score}", True, (0, 255, 0))
    screen.fill((0, 0, 0))
    screen.blit(text, (200, 300))
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == "__main__":
    main()
    pygame.quit()