from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from logger.logging import get_logger
from exception.exceptiohandling import TravelPlannerException
import sys

logger = get_logger(__name__)

class GraphBuilder():
    def __init__(self,model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Main agent function"""
        try:
            logger.info("Agent started processing.")
            user_question = state["messages"]
            input_question = [self.system_prompt] + user_question
            response = self.llm_with_tools.invoke(input_question)
            logger.info("Agent successfully generated a response.")
            return {"messages": [response]}
        except Exception as e:
            logger.error(f"Error in agent_function: {str(e)}")
            raise TravelPlannerException(e, sys)

    def build_graph(self):
        try:
            logger.info("Building the graph with persistence.")
            graph_builder=StateGraph(MessagesState)
            graph_builder.add_node("agent", self.agent_function)
            graph_builder.add_node("tools", ToolNode(tools=self.tools))
            graph_builder.add_edge(START,"agent")
            graph_builder.add_conditional_edges("agent",tools_condition)
            graph_builder.add_edge("tools","agent")
            graph_builder.add_edge("agent",END)
            
            # Setup SQLite Persistence
            conn = sqlite3.connect("chat_history.sqlite", check_same_thread=False)
            memory = SqliteSaver(conn)
            
            self.graph = graph_builder.compile(checkpointer=memory)
            logger.info("Graph built and compiled successfully.")
            return self.graph
        except Exception as e:
            logger.error(f"Error building graph: {str(e)}")
            raise TravelPlannerException(e, sys)
        
    def __call__(self):
        return self.build_graph()