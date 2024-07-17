import tkinter as tk
import math
import random


class Body:
	#self.__init__ :: tuple[float, float] -> list[float] -> None
	def __init__(self, pos, *radList, r = 20):
		self.radList = radList
		self.r = r

		#self.Ids :: list[int]
		self.Ids = []

		#self.pos :: list[tuple[float, float]]
		self.pos = [pos]

		theta = 0
		dt = 25 * math.pi / 180

		x, y = pos

		for r in self.radList:
			x = r * math.cos(theta) + x
			y = r * math.sin(theta) + y

			self.pos.append((x, y))
			theta += dt
	
	#self.move :: float -> float -> None
	def move(self, dx, dy):
		x, y = self.pos[0]
		x, y = x + dx, y + dy
		self.pos[0] = (x, y)

		for i, r in enumerate(self.radList):
			X, Y = self.pos[i + 1]
			
			R = math.sqrt((X - x) ** 2 + (Y - y) ** 2)
			n = r / R
			X, Y = n * (X - x) + x, n * (Y - y) + y
			
			x, y = X, Y
			self.pos[i + 1] = (x, y)

class Application:
	#self.__init__ :: Maybe[tk.Tk]
	def __init__(self, master = None):
		self.master = tk.Tk() if master == None else master
		self.master.title("Animation")

		#self.canvas :: tk.Canvas
		self.canvas = tk.Canvas(self.master, highlightthickness = 0)
		self.canvas.pack(fill = "both", expand = True)

		B1 = Body((200, 200), 70, 80, 70, 50, 25, 25, 25, 25)
		B2 = Body((500, 800), 60, 70, 80, 30, 30, 20, 15, 10, 5)
		B3 = Body((700, 2500), 40, 25, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
		B4 = Body((700, 2500), 35, 15, 10, 10, 10, 10, 20, 20, 30, 50)
		self.bodies = [B1, B2, B3, B4]
		self.v = [150, 270, 320, 500]

		self.draw_all()
		self.update_all()

		self.master.bind("<Left>", lambda event: self.move(-1, 0))
		self.master.bind("<Right>", lambda event: self.move(1, 0))
		self.master.bind("<Up>", lambda event: self.move(0, -1))
		self.master.bind("<Down>", lambda event: self.move(0, 1))

		self.A = True
		self.master.bind("<space>", lambda event: self.M(True))

		self.X = 0
		self.Y = 0
		self.canvas.bind("<Motion>", self.on_mouse_move)
		self.canvas.bind("<Button-1>", self.on_mouse_click)
		self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

	#self._draw :: Body -> None
	def _draw(self, body, fill):
		#body.F = []
		#body.Ids = [self.canvas.create_polygon(0, 0, 0, 0, fill = "cyan", outline = "black")]
		for r in body.radList:
			#break
			Id = self.canvas.create_oval(0, 0, 0, 0, fill = fill, outline = "")
			#K = self.canvas.create_oval(0, 0, 0, 0, fill = "red", outline = "")
			#L = self.canvas.create_oval(0, 0, 0, 0, fill = "cyan", outline = "")
			body.Ids.append(Id)
			#body.F.append((K, L))

	#self._update :: Body -> None
	def _update(self, body):
		a = 5
		#Id = body.Ids[0]
		p1 = []
		p2 = []
		for i, (x, y) in enumerate(body.pos[:-1]):
			r = body.radList[i]
			Id = body.Ids[i]
			#K, L = body.F[i]

			X = r * math.cos(math.pi / 2) + x
			Y = r * math.sin(math.pi / 2) + y
			Z = -r * math.sin(math.pi / 2) + y

			p1.append((X, Y))
			p2.append((X, Z))

			self.canvas.coords(Id, x - r, y - r, x + r, y + r)
			#self.canvas.coords(K, X - a, Y - a, X + a, Y + a)
			#self.canvas.coords(L, X - a, Z - a, X + a, Z + a)

		#p2.reverse()
		#p1.extend(p2)
		#self.canvas.coords(Id, *p1)

	def draw_all(self):
		for colour, body in zip(["cyan", "red", "orange", "green"], self.bodies):
			self._draw(body, colour)

	def update_all(self):
		for body in self.bodies:
			self._update(body)

	def move(self, dx, dy):
		dx *= 10
		dy *= 10
		for body in self.bodies:
			body.move(dx, dy)

		self.update_all()

	def on_mouse_move(self, event):
		self.x, self.y = event.x, event.y
	def on_mouse_click(self, event):
		for i in range(4):
			self.v[i] += 200
	def on_mouse_release(self, event):
		for i in range(4):
			self.v[i] -= 200

	def M(self, S = False):
		if S == True:
			self.A = not self.A
			if self.A == True:
				self.master.after_cancel(self.Q)
				return

		t = 1 / 24
		for i, body in enumerate(self.bodies):
			if False and i == 0:
				X, Y = self.bodies[3].pos[0]
			elif False and i == 1:
				X, Y = self.bodies[2].pos[0]
			else:
				X, Y = self.x, self.y

			v = self.v[i]
			d = v * t
			x, y = body.pos[0]

			dx = X - x
			dy = Y - y

			m = math.sqrt(dx ** 2 + dy ** 2)
			n = d / m
			body.move(n * dx, n * dy)

		self.update_all()

		self.Q = self.master.after(20, self.M)

def main():
	root = tk.Tk()
	app = Application(root)
	root.mainloop()

if __name__ == "__main__":
	main()