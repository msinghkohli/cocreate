from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
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
            verbose=True
        )

    @agent
    def training_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['training_content_creator'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def create_training_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_training_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:

        # Define the manager agent
        training_manager = Agent(
            role="Training Manager for online training",
            goal="Efficiently manage the crew and ensure high-quality creation of contents for an online course",
            backstory="You're an experienced project manager, \
                skilled in overseeing complex projects and guiding teams to success. \
                Your role is to coordinate the efforts of the crew members, ensuring that \
                each task is completed on time and to the highest standard. \
                For any given task to create training for an online course, \
                you first get a member research about the high level contents of the {topic} to identify multiple sub-topics. \
                Then for those sub-topics, you have a member create content.",
            allow_delegation=True,
            verbose=True
        )

        """Creates the Cocreate crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            manager_agent=training_manager,
            process=Process.hierarchical,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
