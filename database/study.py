from dataclasses import dataclass


@dataclass
class Task:
    level: int  # Difficulty
    who_solved: list[str]  # Persons who solved task


@dataclass
class Course:
    name: str  # Course name
    teachers: list[str]  # Teachers of the course
    students: list[str]  # Students of the course



@dataclass
class Person:
    training_courses: list[Course]  # Courses where he sudies
    my_courses: list[Course]  # Courses where he teaches