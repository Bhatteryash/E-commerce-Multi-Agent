from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
from src.tools.ecommerce_tools import ProductSearchTool, PriceComparisonTool

@CrewBase
class ECommerce():
    """E-commerce Multi-Agent Crew for product research, price analysis, and recommendations"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def product_researcher(self) -> Agent:
        """Product research specialist agent"""
        return Agent(
            config=self.agents_config['product_researcher'],
            tools=[ProductSearchTool()],
            verbose=True,
            memory=True
        )

    @agent
    def price_analyzer(self) -> Agent:
        """Price comparison and market analysis agent"""
        return Agent(
            config=self.agents_config['price_analyzer'],
            tools=[PriceComparisonTool()],
            verbose=True,
            memory=True
        )

    @agent
    def recommendation_specialist(self) -> Agent:
        """Personalized recommendation agent"""
        return Agent(
            config=self.agents_config['recommendation_specialist'],
            verbose=True,
            memory=True
        )

    @agent
    def customer_service_agent(self) -> Agent:
        """Customer service and support agent"""
        return Agent(
            config=self.agents_config['customer_service_agent'],
            verbose=True,
            memory=True
        )

    @task
    def product_search_task(self) -> Task:
        """Product search and research task"""
        return Task(
            config=self.tasks_config['product_search_task'],
            agent=self.product_researcher()
        )

    @task
    def price_analysis_task(self) -> Task:
        """Price analysis and comparison task"""
        return Task(
            config=self.tasks_config['price_analysis_task'],
            agent=self.price_analyzer()
        )

    @task
    def recommendation_task(self) -> Task:
        """Personalized recommendation task"""
        return Task(
            config=self.tasks_config['recommendation_task'],
            agent=self.recommendation_specialist(),
            output_file='recommendations.md'
        )

    @task
    def customer_support_task(self) -> Task:
        """Customer support task"""
        return Task(
            config=self.tasks_config['customer_support_task'],
            agent=self.customer_service_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the E-commerce Multi-Agent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    def run_product_search(self, query: str, budget: str = "flexible", category: str = "general", preferences: str = "") -> Dict[str, Any]:
        """Run the crew for product search and recommendations"""
        inputs = {
            'query': query,
            'budget': budget,
            'category': category,
            'preferences': preferences,
            'follow_up_query': ""
        }
        
        result = self.crew().kickoff(inputs=inputs)
        return {
            'success': True,
            'result': result,
            'recommendations': result
        }
    
    def handle_customer_query(self, follow_up_query: str, context: str = "") -> Dict[str, Any]:
        """Handle customer support queries"""
        inputs = {
            'query': context,
            'budget': "flexible",
            'category': "general",
            'preferences': "",
            'follow_up_query': follow_up_query
        }
        
        # Run only the customer support task
        support_task = self.customer_support_task()
        support_agent = self.customer_service_agent()
        
        result = Crew(
            agents=[support_agent],
            tasks=[support_task],
            process=Process.sequential,
            verbose=True
        ).kickoff(inputs=inputs)
        print("\n✅ Customer support query handled successfully!")
        print(f"Results: {result.raw}")
        return {
            'success': True,
            'response': result.raw
        }
