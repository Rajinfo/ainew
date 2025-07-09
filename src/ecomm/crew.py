from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ecomm:
    """Software Development Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def prd_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['prd_analyzer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config['designer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def developer(self) -> Agent:
        return Agent(
            config=self.agents_config['developer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def senior_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_developer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def devops(self) -> Agent:
        return Agent(
            config=self.agents_config['devops'],  # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_prd_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_prd'],  # type: ignore[index]
        )

    @task
    def design_ui_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_ui'],  # type: ignore[index]
        )

    @task
    def develop_code_fe_task(self) -> Task:
        return Task(
            config=self.tasks_config['develop_code_fe'],  # type: ignore[index]
        )
    @task
    def develop_code_be_task(self) -> Task:
        return Task(
            config=self.tasks_config['develop_code_be'],  # type: ignore[index]
        )
    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review'],  # type: ignore[index]
        )

    @task
    def testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['testing'],  # type: ignore[index]
        )

    @task
    def cicd_pipeline_fe_task(self) -> Task:
        return Task(
            config=self.tasks_config['cicd_pipeline_fe'],  # type: ignore[index]
        )
    @task
    def cicd_pipeline_be_task(self) -> Task:
        return Task(
            config=self.tasks_config['cicd_pipeline_be'],  # type: ignore[index]
        )
    @crew
    def crew(self) -> Crew:
        """Creates the Software Development Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you want to use hierarchical process
        )
