import pytest
from agent.agentic_workflow import GraphBuilder

def test_graph_initialization():
    builder = GraphBuilder(model_provider="groq")
    graph = builder.build_graph()
    assert graph is not None
    # Check if the graph has the 'agent' and 'tools' nodes
    assert "agent" in graph.nodes
    assert "tools" in graph.nodes

@pytest.mark.skip(reason="Requires valid API key and internet access for full invocation")
def test_graph_invocation():
    # This is more of an integration/E2E test
    builder = GraphBuilder(model_provider="groq")
    graph = builder.build_graph()
    messages = {"messages": [{"role": "user", "content": "Hello"}]}
    config = {"configurable": {"thread_id": "test_thread"}}
    response = graph.invoke(messages, config=config)
    assert "messages" in response
    assert len(response["messages"]) > 0
