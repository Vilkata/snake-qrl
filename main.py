import pygame
import time
from q_learning_agent import QLearningAgent
from snake_game import SnakeGame

def main():
    pygame.init()
    game = SnakeGame(grid_size=5, cell_size=60)
    screen = pygame.display.set_mode((game.width, game.height))
    pygame.display.set_caption("Snake RL")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    progress_interval = 1000
    speed = 20

    agent = QLearningAgent(actions=[0, 1, 2, 3])
    episode = 0  
    total_score = 0
    total_steps = 0  
    steps_in_interval = 0 


    while True:  
        episode += 1
        state = game.reset()
        score = 0
        done = False

        show_episode = episode % progress_interval == 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            #Избор на действие и обучение
            action = agent.choose_action(state)
            next_state, reward, done = game.step(action)
            agent.learn(state, action, reward, next_state)

            state = next_state
            if reward == 10:
                score += 1

            total_steps += 1
            steps_in_interval += 1

            #Визуализация
            if show_episode:
                screen.fill((0, 0, 0))
                for segment in game.snake:
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
                        segment[1] * game.cell_size, segment[0] * game.cell_size, game.cell_size, game.cell_size
                    ))
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                    game.food[1] * game.cell_size, game.food[0] * game.cell_size, game.cell_size, game.cell_size
                ))

                text_surface = font.render(
                    f"Episode: {episode}", True, (255, 255, 255)
                )
                screen.blit(text_surface, (10, 10))

                pygame.display.flip()
                clock.tick(speed)

        #Изчисляване на средния резултат
        total_score += score

        if episode % progress_interval == 0:
            average_score = total_score / progress_interval
            average_steps_per_episode = steps_in_interval / progress_interval
            print(f"Episode {episode}: Average Score = {average_score}, Average Steps = {average_steps_per_episode:.0f}")
            total_score = 0
            total_steps = 0

if __name__ == "__main__":
    main()
