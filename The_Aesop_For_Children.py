#  Copyright 2022-2023 Mashiur Rahman Mahid
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY
from Aesop_Fables_data import fables
import glob
font_list=glob.glob("data/font/*.ttf")
import pygame,sys
from pygame.locals import*
pygame.init()
clock=pygame.time.Clock()
pygame.display.set_caption("The Aesop for Children")
icon=pygame.image.load('data/The Aesop for Childern.png')
pygame.display.set_icon(icon)
available_display_resolution=pygame.display.list_modes()
set_display_resolution=[1200,650]

try:
	set_display_resolution=available_display_resolution[4]
except:
	pass

w=set_display_resolution[0]
h=set_display_resolution[1]
screen=pygame.display.set_mode((w,h),RESIZABLE)
current_text_placing_postion_y=0
currently_displaying_fable_number=0
total_fable_number=145
total_text_line_height=0
number_of_pixel_forward_on_scroll=0
font_list_index=0
font_size=20

class TextView():
	def __init__(self,screen,text='',text_position_x=0,text_position_y=0,text_width=200,text_height=400,text_color="#666666",font_size=20):
		self.screen=screen
		self.text_position_x=text_position_x
		self.text_position_y=text_position_y
		self.text_weight=text_width
		self.text_height=text_height
		self.text_color=text_color 
		self.text=text
		self.font_size=font_size
		self.text_font=pygame.font.Font(font_list[font_list_index], self.font_size)
		self.text_lines=[]
		self.splitted_lines=self.text.splitlines()
		for splitted_line in self.splitted_lines:
			if self.text_font.size(splitted_line)[0] > self.text_weight:
				words = splitted_line.split(' ')
				fitted_line=""
				for word in words:
					test_line = fitted_line + word + " "
					if self.text_font.size(test_line)[0] < self.text_weight:
						fitted_line = test_line
					else:
						self.text_lines.append(fitted_line)
						fitted_line = word + " "
				self.text_lines.append(fitted_line)
			else:
				self.text_lines.append(splitted_line)
				
		text_line_height=(self.text_font.size(self.text_lines[0])[1])
		global total_text_line_height
		total_text_line_height=text_line_height*(len(self.text_lines)-1)
		
		
		for line in self.text_lines:
			if line != "":
				text_surface = self.text_font.render(line, 1, self.text_color)
				self.screen.blit(text_surface, (self.text_position_x, self.text_position_y))
			self.text_position_y+=text_line_height


will_scroll=False

game_running=True
while game_running:
	screen.fill('#F0FFFF')
	clock.tick(60)
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
		if event.type==pygame.VIDEORESIZE:
			w,h=event.size

		if event.type==pygame.MOUSEBUTTONDOWN:
			if event.button==1:
				will_scroll=True

			if event.button==3:
				will_scroll=False
				number_of_pixel_forward_on_scroll=0

			if event.button==2:
				if font_list_index+1>=len(font_list):
					font_list_index=0
				else:
					font_list_index+=1
					
		if event.type==pygame.MOUSEWHEEL:	
			current_text_placing_postion_y=0
			current_text_placing_position_x=0

			if abs(event.y)+currently_displaying_fable_number<=total_fable_number:
				currently_displaying_fable_number+=event.y
			elif currently_displaying_fable_number==total_fable_number:
				currently_displaying_fable_number=0
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_f:
				if font_size+5<50:
					font_size=font_size+5
				else:
					font_size=20




	if will_scroll==True and number_of_pixel_forward_on_scroll<=total_text_line_height:
		if abs(current_text_placing_postion_y)<=total_text_line_height:
			number_of_pixel_forward_on_scroll+=.5
			current_text_placing_postion_y-=.5

	TextView(screen,text=fables[currently_displaying_fable_number],text_position_x=20,text_position_y=10+current_text_placing_postion_y,text_width=w-50,text_height=h,font_size=font_size)
	pygame.display.update()
