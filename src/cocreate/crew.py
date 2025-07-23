from cocreate.models import CourseContents
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Cocreate():
    """Cocreate crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    

    @agent
    def training_content_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['training_content_researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def training_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['training_content_creator'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def training_quiz_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['training_quiz_creator'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    # @task
    # def training_content_research(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['training_content_research'], # type: ignore[index]
    #     )
    
    # @task
    # def training_content_create(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['training_content_create'], # type: ignore[index]
    #     )
    
    @task
    def create_training_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_training_task'], # type: ignore[index]
            output_pydantic=CourseContents
        )

    @crew
    def crew(self) -> Crew:

        # Define the manager agent
        project_manager = Agent(
            role="Project Manager",
            goal="Efficiently manage the crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. \
                Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
            allow_delegation=True,
            verbose=True
        )

        """Creates the Cocreate crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            manager_agent=project_manager,
            process=Process.hierarchical,
            verbose=True,
            response_format=CourseContents
        )
