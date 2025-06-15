from pygame import Rect
import pgzero

WIDTH, HEIGHT = 740, 480

camera_x = 0
music_on = True
sounds_on = True
game_state = "menu"
btn_play = Rect(WIDTH//2 - 150, 230, 300, 50)
btn_music = Rect(WIDTH//2 - 150, 290, 300, 50)
btn_exit = Rect(WIDTH//2 - 150, 350, 300, 50)
score = 0
start_x = 100
checkpoints = [800, 1200, 1600, 2000, 2500]

lives = 3

def play_music():
   if music_on:
      music.play('music')

def stop_music():
   music.stop()

class Hero:
   def __init__(self):
      self.x = 100
      self.y = 500
      self.speed_y = 0
      self.on_ground = True
      self.direction = "right"
      self.idle_images = ["hero_idle1", "hero_idle2"]
      self.run_images = ["hero_run1", "hero_run2"]
      self.frame = 0
      self.frame_count = 0
      self.image = self.idle_images[0]
      self.rect = Rect(self.x, self.y, 50, 50)

   def update(self):
      # gravity
      self.speed_y += 0.5
      self.y += self.speed_y
      # collide the ground
      if self.y >= 300:
         self.y = 300
         self.speed_y = 0
         self.on_ground = True

      keys = keyboard

      # Moviment left / right
      if keys.left:
         self.x -= 3
         self.direction = "left"
      if keys.right:
         self.x += 3
         self.direction = "right"

      if self.x < 0:
         self.x = 0

      # jump
      if keys.space and self.on_ground:
         self.speed_y = -13
         self.on_ground = False
         if sounds_on:
               sounds.jump.play()

      # Animation
      self.frame_count += 1
      if self.frame_count >= 10:
         self.frame = (self.frame + 1) % 2
         self.frame_count = 0

      if keys.left or keys.right:
         self.image = self.run_images[self.frame]
      else:
         self.image = self.idle_images[self.frame]

      self.rect.topleft = (self.x, self.y)

   def draw(self):
      screen.blit(self.image, (self.x - camera_x, self.y))

class Enemy:
   def __init__(self, x, y, patrol_distance):
      self.x = x
      self.y = y
      self.min_x = x - patrol_distance
      self.max_x = x + patrol_distance
      self.direction = 1
      self.walk_images = ["flyfly1", "flyfly2"]
      self.frame = 0
      self.frame_count = 0
      self.image = self.walk_images[0]
      self.rect = Rect(self.x, self.y, 50, 50)

   def update(self):
      self.x += self.direction * 2
      if self.x <= self.min_x or self.x >= self.max_x:
         self.direction *= -1

      # Animação
      self.frame_count += 1
      if self.frame_count >= 15:
         self.frame = (self.frame + 1) % 2
         self.frame_count = 0

      if self.direction == 1:
         self.image = self.walk_images[self.frame] + '-right'
      else:
         self.image = self.walk_images[self.frame]

      self.rect.topleft = (self.x, self.y)

   def draw(self):
      screen.blit(self.image, (self.x - camera_x, self.y))

hero = Hero()
enemies = [Enemy(400, 320, 100), Enemy(600, 320, 150)]

def draw_menu():
   screen.fill((15, 25, 45))
   screen.draw.text("SPACE RUNNER", center=(WIDTH//2, 100), fontsize=50, color="white")

   screen.draw.filled_rect(btn_play, "darkgreen")
   screen.draw.text("Start Game", center=btn_play.center, fontsize=40, color="white")

   screen.draw.filled_rect(btn_music, "darkblue")
   screen.draw.text("Toggle Music/Sound", center=btn_music.center, fontsize=40, color="white")

   screen.draw.filled_rect(btn_exit, "darkred")
   screen.draw.text("Exit", center=btn_exit.center, fontsize=40, color="white")

def update():
   global camera_x, game_state, score, checkpoints, lives

   if game_state == "playing":
      hero.update()
      for enemy in enemies:
         enemy.update()

      camera_x = max(0, hero.x - WIDTH // 2)
      score = max(0, int((hero.x - start_x) / 10))

      for cp in checkpoints[:]:
         if hero.x >= cp:
               enemies.append(Enemy(cp + 200, 320, 100))
               checkpoints.remove(cp)

      for enemy in enemies:
         if hero.rect.colliderect(enemy.rect):
               print("Ouch! Enemy hit!")
               if sounds_on:
                  sounds.enemy_hit.play()
               lives -= 1
               hero.x, hero.y = 100, 500
               if lives <= 0:
                  game_state = "gameover"
                  sounds.gameover.play()
               break
def on_mouse_down(pos):
   global game_state, music_on, sounds_on, lives, score, checkpoints, enemies

   if game_state == "menu":
      if btn_play.collidepoint(pos):
         game_state = "playing"
         play_music()
      elif btn_music.collidepoint(pos):
         music_on = not music_on
         sounds_on = not sounds_on
         if music_on:
               play_music()
         else:
               stop_music()
      elif btn_exit.collidepoint(pos):
         exit()

   elif game_state == "gameover":
      #restart game
      lives = 3
      hero.x, hero.y = 100, 500
      score = 0
      enemies.clear()
      enemies.extend([Enemy(400, 320, 100), Enemy(600, 320, 150)])
      checkpoints[:] = [800, 1200, 1600, 2000, 2500]
      game_state = "playing"

def draw():
   screen.clear()
   if game_state == "menu":
      draw_menu()

   elif game_state == "playing":
      screen.blit("sky", (0, 0))
      screen.draw.filled_rect(Rect(0, 380, 800, 200), (99, 99, 99))
      hero.draw()
      for enemy in enemies:
         enemy.draw()

      screen.draw.text(f"Score: {score}", (20, 20), fontsize=30, color="white")

      for i in range(lives):
         screen.blit("heart", (20 + i * 30, 60))

   elif game_state == "gameover":
      screen.fill("black")
      screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
      screen.draw.text("Click to reign", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

def on_mouse_down(pos):
   global game_state, music_on, sounds_on, lives, score, checkpoints, enemies

   if game_state == "menu":
      if btn_play.collidepoint(pos):
         game_state = "playing"
         play_music()
      elif btn_music.collidepoint(pos):
         music_on = not music_on
         sounds_on = not sounds_on
         if music_on:
               play_music()
         else:
               stop_music()
      elif btn_exit.collidepoint(pos):
         exit()

   elif game_state == "gameover":
      lives = 3
      hero.x, hero.y = 100, 500
      score = 0
      enemies.clear()
      enemies.extend([Enemy(400, 320, 100), Enemy(600, 320, 150)])
      checkpoints[:] = [800, 1200, 1600, 2000, 2500]
      game_state = "playing"
