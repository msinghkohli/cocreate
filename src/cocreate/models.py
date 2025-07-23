from typing import List
from pydantic import BaseModel

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str

class CourseSubtopic(BaseModel):
    title: str
    synopsis: str
    contents: str
    questions: List[QuizQuestion]

class Module(BaseModel):
    title: str
    synopsis: str
    subtopics: List[CourseSubtopic]

class CourseContents(BaseModel):
    modules: List[Module]