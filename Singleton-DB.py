import sqlite3
from abc import ABC, abstractmethod
import os
import random
import time
def setup_database():
    with sqlite3.connect('leaderboards.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard (circle INTEGER, square INTEGER, triangle INTEGER)")
        # Check if the table is empty before inserting default values
        cursor.execute("SELECT COUNT(*) FROM leaderboard")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO leaderboard (circle, square, triangle) VALUES (0, 0, 0)")
        conn.commit()
def update_score(shape):
    with sqlite3.connect('leaderboards.db') as conn:
        cursor = conn.cursor()
        if shape == "circle":
            cursor.execute("UPDATE leaderboard SET circle = circle + 1")
        elif shape == "square":
            cursor.execute("UPDATE leaderboard SET square = square + 1")
        elif shape == "triangle":
            cursor.execute("UPDATE leaderboard SET triangle = triangle + 1")
        conn.commit()
def retrieve_high_scores():
    with sqlite3.connect('leaderboards.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM leaderboard')
        scores = cursor.fetchall()
        for score in scores:
            print(f"\nCircle is {score[0]}")
            print(f"Square is {score[1]}")
            print(f"Triangle is {score[2]}\n")
    return scores
def delete_scores():
    with sqlite3.connect('leaderboards.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE leaderboard SET circle = 0, square = 0, triangle = 0")
        conn.commit()
class Singleton:
    instance = None
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
class Shape(ABC, Singleton):
    @abstractmethod
    def sides(self):
        pass
class Circle(Shape):
    def sides(self):
        return "0"
class Square(Shape):
    def sides(self):
        return "4"
class Triangle(Shape):
    def sides(self):
        return "3"
class Game:
    def __init__(self):
        self.sides = None
    def random_sides(self):
        self.sides = random.choice(["0", "3", "4"])
        return self.sides
    def __str__(self):
        return f"\nWhat shape has {self.random_sides()} sides?"
    def game(self):
        while True:
            print(self)
            print("\nSelect an Option:")
            print("1. Circle")
            print("2. Square")
            print("3. Triangle")
            print("4. Reset Terminal")
            print("5. Return to Main Menu")
            option = input("Select a menu option: ")
            if option == "1" and "0" == self.sides:
                choice = Circle()
                update_score("circle")
                print(f"A circle has {choice.sides()} sides: {id(choice)}")
            elif option == "2" and "4" == self.sides:
                choice = Square()
                update_score("square")
                print(f"A square has {choice.sides()} sides: {id(choice)}")
            elif option == "3" and "3" == self.sides:
                choice = Triangle()
                update_score("triangle")
                print(f"A triangle has {choice.sides()} sides: {id(choice)}")
            elif option == "4":
                self.cls()
            elif option == "5":
                print("Returning to main menu...")
                break
            else:
                print("Wrong guess! You lose.")
                break
    def cls(self):
        os.system('cls')
        time.sleep(0.1)
    def main_menu(self):
        while True:
            print("\nSelect a choice:")
            print("1. Play Game")
            print("2. Scoreboard")
            print("3. Clear Terminal")
            print("4. Reset Scores")
            print("5. End Game")
            option = input("Select a menu option: ")
            if option == "1":
                self.game()
            elif option == "2":
                retrieve_high_scores()
            elif option == "3":
                self.cls()
            elif option == "4":
                delete_scores()
                print("Scores have been reset.")
            elif option == "5":
                break
            else:
                print("Invalid input")
def main():
    setup_database()
    run = Game()
    run.main_menu()
main()
