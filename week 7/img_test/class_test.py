import os
import sys

class Course:
	'''
	Course class
	properties: id,name,credits,lecturer
	methods: get_name,set_credits
	'''
	ID = 0 # 类变量 所有实例共享一份 类似静态变量

	def __init__(self,name,credits,lecturer):
		self.id = Course.ID
		Course.ID += 1
		self.name = name
		self.credits = credits
		self.lecturer = lecturer
		return None

	def print_course(self):
		print(f'{self.id}\t{self.name}\t{self.credits}\t{self.lecturer}')

class Student:
	def __init__(self,name):
		self.name = name
		self.courses = []

	def choose_course(self,c:Course):
		self.courses.append(c)

	def total_credits(self):
		total = 0
		for c in self.courses:
			total += c.credits
		return total


def main():
	cc = Course('c',2,'z')
	cp = Course('Python',2,'z')
	cc.print_course()
	cp.print_course()

	s = Student('l')
	s.choose_course(cc)
	s.choose_course(cp)
	print(s.total_credits())

	print(Course.ID)
	Course.print_course(cc) # 直接调用类的方法的时候 要传入类的实例

if __name__ == '__main__':
	main()