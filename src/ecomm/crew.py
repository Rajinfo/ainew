import os
import re
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import FileWriterTool
from crewai.tools import BaseTool
from typing import Any


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


# --- Custom Tool to Extract and Write Markdown Files ---
class MarkdownToFileTool(BaseTool):
    name: str = "Markdown File Extractor"
    description: str = "Extracts code blocks from a markdown file and writes them to the specified file paths."
    markdown_file_path: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, input: str) -> str:
        print(f"🛠️ MarkdownTool is processing: {self.markdown_file_path}")
        if not os.path.exists(self.markdown_file_path):
            return f"❌ Markdown file not found: {self.markdown_file_path}"

        with open(self.markdown_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        result_log = []

        # Pattern 1: ### File: `ecomm/backend/...`
        pattern1 = r"### File: `(.+?)`\n```(?:\w+)?\n(.*?)\n```"
        matches1 = re.findall(pattern1, content, re.DOTALL)

        for file_path, code in matches1:
            result_log.append(self._write_file(file_path.strip(), code))

        # Pattern 2: ### src/... (relative path to be prefixed with ecomm/backend/)
        pattern2 = r"### (src\/.+?)\n```(?:\w+)?\n(.*?)\n```"
        matches2 = re.findall(pattern2, content, re.DOTALL)

        for relative_path, code in matches2:
            file_path = os.path.join("ecomm/backend", relative_path)
            result_log.append(self._write_file(file_path.strip(), code))

        # Pattern 3:  ### : `ecomm/backend/...`
        pattern3 = r"### (ecomm\/.+?)\n```(?:\w+)?\n(.*?)\n```"
        matches3= re.findall(pattern3, content, re.DOTALL)

        for file_path, code in matches3:
            result_log.append(self._write_file(file_path.strip(), code))

        # Pattern 4: File path between ```anyword and ``` lines, starting with ecomm/
        pattern4 = r"```\w+\n(ecomm\/.+?)\n```"
        matches4 = re.findall(pattern4, content, re.DOTALL)

        for file_path, code in matches4:
            # For this pattern, we just extract the file path, no code to write
            result_log.append(self._write_file(file_path.strip(), code))

        if not (matches1 or matches2 or matches3 or matches4):
            return "⚠️ No valid code blocks with file paths found."

        return "\n".join(result_log)

    def _write_file(self, file_path: str, code: str) -> str:
        try:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"📄 Writing: {file_path}")
            file_writer = FileWriterTool()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code.strip())
            return f"✅ Wrote {file_path}"
        except Exception as e:
            return f"❌ Failed to write {file_path}: {e}"

# --- Setup tool, agent, task, and crew ---
markdown_tool = MarkdownToFileTool(markdown_file_path="ecomm/backend/Backend.md")
markdown_tool_fe = MarkdownToFileTool(markdown_file_path="ecomm/frontend/frontend.md")

# [Define your Agents, Tasks, Tools, etc.]

def log_task_output(task_output: Any):
    print("\n--- Task Callback Received ---")
    if task_output is not None:
        print(f"Object type: {type(task_output).__name__}")
        attributes = getattr(
            task_output, "__dict__", "N/A (object may lack __dict__)"
        )
        print(f"Instance attributes: {attributes}")
    else:
        print("Received None object.")

def log_step_output(step_output: Any):
    print("\n--- Step Callback Received ---")
    if step_output is not None:
        print(f"Object type: {type(step_output).__name__}")
        attributes = getattr(
            step_output, "__dict__", "N/A (object may lack __dict__)"
        )
        print(f"Instance attributes: {attributes}")
    else:
        print("Received None object.")
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
    def code_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['code_generator'],  # type: ignore[index]
            tools=[markdown_tool],
            verbose=True
        )
    @agent
    def code_generator_fe(self) -> Agent:
        return Agent(
            config=self.agents_config['code_generator_fe'],  # type: ignore[index]
            tools=[markdown_tool_fe],
            verbose=True
        )

    @agent
    def frontend_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_validator'],  # type: ignore[index]
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
    def generate_backend_structure_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_backend_structure'],  # type: ignore[index]
            agent=self.code_generator()
        )
    @task
    def generate_frontend_structure_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_frontend_structure'],  # type: ignore[index]
            agent=self.code_generator_fe()
        )

    @task
    def validate_frontend_startup_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_frontend_startup'],  # type: ignore[index]
            agent=self.frontend_validator()
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
            task_callback=log_task_output,
            step_callback=log_step_output,
            #process=Process.hierarchical, # In case you want to use hierarchical process
        )
