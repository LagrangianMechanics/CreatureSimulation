import tkinter as tk
import math

s1 = math.sin(2 * math.pi / 3)
s2 = math.sin(4 * math.pi / 3)

c1 = math.cos(2 * math.pi / 3)
c2 = math.cos(4 * math.pi / 3)

A = 3 / (2 * math.pi)

X1 = lambda r, x: A * (c1 - 1) * x + r
X2 = lambda r, x: r * c1
X3 = lambda r, x: A * r * (1 - c2) * (x - 4 * math.pi / 3) + r * c2

Y1 = lambda r, y: A * r * s1 * y
Y2 = lambda r, y: A * r * (s2 - s1) * (y - 2 * math.pi / 3) + r * s1
Y3 = lambda r, y: -A * r * s2 * (y - 4 * math.pi / 3) + r * s2

def X(r, t):
	if 0 <= t <= 2 * math.pi / 3:
		return X1(r, t)
	elif 2 * math.pi / 3 < t <= 4 * math.pi / 3:
		return X2(r, t)
	else:
		return X3(r, t)

def Y(r, t):
	if 0 <= t <= 2 * math.pi / 3:
		return Y1(r, t)
	elif 2 * math.pi / 3 < t <= 4 * math.pi / 3:
		return Y2(r, t)
	else:
		return Y3(r, t)

def curve(t, x, y, r):
	#return (X(r, t) + x, Y(r, t) + y)
	return (r * math.cos(t) + x, r * math.sin(t) + y)

class Creature:
	def __init__(self, xy: (float, float), *radii: tuple[float]):
		self.radii = radii
		self.pos: [(float, float)] = [xy]

		self.maxT = 90 #math.pi / 2

		x, y = xy

		for r in self.radii:
			x += r
			y += r

			self.pos.append((x, y))
	def move(self, segment: int, dx: float, dy: float):
		X, Y = self.pos[segment]
		X, Y = X + dx, Y + dy
		self.pos[0] = (X, Y)

		for j, r in enumerate(self.radii):
			x, y = self.pos[j + 1]

			u, v = (x - X), (y - Y)

			U = math.atan(v / u)
			if U < 0:
				U += 2 * math.pi
			if U > 2 * math.pi:
				U -= 2 * math.pi

			T = U if u >= 0 else math.pi + U
			if T < 0:
				T += 2 * math.pi
			if T > 2 * math.pi:
				T -= 2 * math.pi

			#X, Y = r * math.cos(T) + X, r * math.sin(T) + Y
			X, Y = curve(T, X, Y, r)
			self.pos[j + 1] = (X, Y)
	def create(self, canvas):
		self.LineId = canvas.create_line(0, 0, 0, 0, smooth = True, fill = "cyan")
		self.canvas = canvas

		self.A = canvas.create_polygon(0, 0, 0, 0, fill = "grey", smooth = False)

		self.IdA = []
		self.IdB = []
		for j in range(len(self.radii)):
			I1 = self.canvas.create_oval(0, 0, 0, 0, outline = "", fill = "dark blue")
			I2 = self.canvas.create_oval(0, 0, 0, 0, outline = "", fill = "orange")
			self.IdA.append(I1)
			self.IdB.append(I2)

		#self.L1 = canvas.create_line(0, 0, 0, 0, smooth = False, fill = "dark grey", width = 10)
		#self.L2 = canvas.create_line(0, 0, 0, 0, smooth = False, fill = "black", width = 10)
	def draw(self):
		#self.canvas.coords(self.LineId, *self.pos)
		P = []
		B = []

		for j, r in enumerate(self.radii):
			x, y = self.pos[j]
			a = curve(math.pi / 2, x, y, r)
			b = curve(3 / 2 * math.pi, x, y, r)

			P.append(a)
			B.append(b)

		#self.canvas.coords(self.L1, *P)
		#self.canvas.coords(self.L2, *B)

		B.reverse()
		P.extend(B)

		self.canvas.coords(self.A, P)

		s = 5
		for j, r in enumerate(self.radii):
			I1 = self.IdA[j]
			I2 = self.IdB[j]
			x, y = self.pos[j]

			x1, y1 = curve(math.pi / 2, x, y, r)
			x2, y2 = curve(3 * math.pi / 2, x, y, r)

			self.canvas.coords(I1, x1 - s, y1 - s, x1 + s, y1 + s)
			self.canvas.coords(I2, x2 - s, y2 - s, x2 + s, y2 + s)

class Application:
	def __init__(self, master: tk.Tk = None):
		self.master = tk.Tk() if master == None else master
		self.master.title("Creature Game")

		self.canvas = tk.Canvas(self.master, highlightthickness = 0)
		self.canvas.pack(fill = "both", expand = True)

		#self.C = Creature((200, 200), 50, 40, 30)
		U = [30] * 60
		self.C = Creature((200, 200), *U)
		self.create()

		self.master.mainloop()
	def create(self):
		self.C.create(self.canvas)
		self.C.draw()

		#x, y = self.C.pos[0]
		r = 10

		for j, (x, y) in enumerate(self.C.pos):
			self.canvas.create_oval(x - r, y - r, x + r, y + r, tag = ("circle.dragable", f"C[{j}]"), fill = "red", outline = "")
			break
		self.canvas.tag_bind(f"circle.dragable", "<Button-1>", self.on_mouse_click)
		self.canvas.tag_bind(f"circle.dragable", "<B1-Motion>", self.on_mouse_drag)
	def on_mouse_click(self, event):
		self.x, self.y = event.x, event.y
	def on_mouse_drag(self, event):
		x, y = event.x, event.y

		dx, dy = (x - self.x), (y - self.y)

		#self.canvas.move("circle.dragable", dx, dy)

		self.x, self.y = x, y

		self.C.move(0, dx, dy)
		self.C.draw()

		r = 10
		for j, (x, y) in enumerate(self.C.pos):
			self.canvas.coords(f"C[{j}]", x - r, y - r, x + r, y + r)

def main():
	root = tk.Tk()
	app = Application(root)

if __name__ == "__main__":
	main()