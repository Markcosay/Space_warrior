import time
import pygame
import random
import math

pygame.init()
status = True
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font(None,60)
#making cursofr invisible inside game window
pygame.mouse.set_visible(False)

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Warrior")

# Load images
background_img=pygame.image.load("icons\\background.jpg")
player_img = pygame.image.load("icons\\fighter-jet.png")
bullet_img = pygame.image.load("icons\\bullet.png")
missile_img = pygame.image.load("icons\missile.png")
enemy_img  = pygame.image.load("icons\enemy.png")
supply_img = pygame.image.load("icons\supplies.png")
health_img = pygame.image.load("icons\health.png")


#for non-stationary items
player_img = pygame.transform.scale(player_img, (40, 40))
bullet_img = pygame.transform.scale(bullet_img, (20, 10))
missile_img = pygame.transform.scale(missile_img, (30,20))
enemy_img = pygame.transform.scale(enemy_img,(40,40))
supply_img = pygame.transform.scale(supply_img,(40,40))
enemy_img= pygame.transform.flip(enemy_img, False, True)

#making logo for stationary items
background_img=pygame.transform.scale(background_img,(800,600))
missile_logo= pygame.transform.scale(missile_img,(20,20))
health_img= pygame.transform.scale(health_img,(20,20))

pygame.display.set_icon(player_img)
start_time = time.time()
timer = 0
timer1 = 0
timer2 = 0

# Set up global variables
global bullets
bullets = []

global missiles
missiles = []
global missiles_num
missiles_num = 5

global enemies
enemies = []

global enemies_Health
enemies_Health = []

enx = 0
global  k
k=0

global supplyx
global supplyy
global score
global player_health

player_health=5
score = 0

global supplyC
supplyC= []



#function to create player
def player(b):
    if(b>770):
        b=770
    screen.blit(player_img, (b, 550))

#function to create bullets
def bullet(b, c):
    bullets.append((b, 550-c))

#function to create missiles
def missile(b,c):
    global missiles_num
    if(missiles_num > 0):
        missiles.append((b-15,550-c))
        missiles.append((b+5,550-c))
        missiles_num -=1

#function to create enemy
def enemy(i):
    while(i>0 and len(enemies)<=i):
        enx = random.randint(0,770)
        enemies.append((enx,0))
        enemies_Health.append(3)
        i-=1

#function to check collison
def isColliding(ex,ey,cx,cy):
    distance = int(math.sqrt(math.pow((ex-cx),2) + math.pow((ey-cy),2)))
    if distance <= 30:
        return True
    else:
        return False

#gameover window
def game_over():
    screen.fill((0,0,0))
    gameover_text=font1.render("GAME OVER", True, (255,0,0), None)
    screen.blit(gameover_text,(300,250))
    
#opening animation
text = font1.render("SPACE WARRIOR", True, (255,255,255), None)
text_rect = text.get_rect()
text_rect.center = (400, 300)
kount = 0
k=1

for i in range(10):
        time.sleep(0.2)
        r = random.randint(0, 250)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        screen.fill((r,b,g))
        screen.blit(text, text_rect)
        pygame.display.update()


while status:
    
    kount+=1
    screen.blit(background_img,(0,0))
    screen.blit(missile_logo,(760,10))
    missile_count = font.render(str(missiles_num), True, (255, 255, 255))
    score_count = font.render("SCORE : "+str(score),True, (255,255,255))
    screen.blit(missile_count,(775,10))
    screen.blit(score_count,(25,10))

    #displaying health images according to remaining health
    for i in range (player_health):
        screen.blit(health_img,((25+(i*20)),40))

    #counting event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet(x, 0)
            if event.button == 3:
                missile(x,0)
        
    current_time = time.time()
    elapsed_time = current_time - start_time+1

    if elapsed_time > timer:
        timer += 15
        #generating random position for the supply
        supplyx = random.randint(10, 590)
        supplyy = 0
        supplyC.append((supplyx, supplyy))

    player(x)
    if elapsed_time>timer1:
        timer1+=30
        k+=1
        print(k)

    if elapsed_time > timer2:
        timer2 += 2
        enemy(k)

    for i,(bx,by) in enumerate(supplyC):
        pass
     
    for i, (bx, by) in enumerate(bullets):
        bullets[i] = (bx, by-5)
        screen.blit(bullet_img, (bx+10, by-5))
        if by <= 0:
            del bullets[i]

    for i, (bx, by) in enumerate(missiles):
        missiles[i] = (bx,by-5)
        screen.blit(missile_img,(bx+10, by-5))
        if by <=0:
            del missiles[i]

    for i,(bx,by) in enumerate(enemies):
        enemies[i] = (bx,by+2)
        screen.blit(enemy_img,(bx-10,by+5))
        if by>=600:
            del enemies[i]
            del enemies_Health[i]
       
    for ji,(ex,ey) in enumerate(enemies):
        for ii,(cx,cy) in enumerate(bullets): 
            if isColliding(ex,ey,cx,cy):
                del bullets[ii]
                enemies_Health[ji] = enemies_Health[ji] - 1
                if enemies_Health[ji] ==0:
                    del enemies[ji]
                    score+=1

    for ji,(ex,ey) in enumerate(enemies):
        for ii,(cx,cy) in enumerate(missiles): 
            if isColliding(ex,ey,cx,cy):
                del enemies[ji]
                del missiles[ii]
                del enemies_Health[ji]
                score+=1

    for i, (bx, by) in enumerate(supplyC):
        screen.blit(supply_img, (bx, by))
        if by >= 600:
            del supplyC[i]
        else:
            supplyC[i] = (bx, by+2)

    for ji,(ex,ey) in enumerate(supplyC): 
            if isColliding(ex,ey,x,550):
                supplyC.clear()
                missiles_num +=6

    for ji,(ex,ey) in enumerate(enemies): 
            if isColliding(ex,ey,x,550):
                del enemies[ji]
                player_health-=1
                break

    if(player_health<=0):
        game_over() 

    pygame.display.update()
    time.sleep(0.01)

pygame.quit()
