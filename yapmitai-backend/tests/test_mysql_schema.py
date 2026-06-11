from sqlalchemy.dialects.mysql import dialect
from sqlalchemy.schema import CreateTable

from app.models import Base


def test_all_tables_compile_for_mysql() -> None:
    table_names = set()
    mysql_dialect = dialect()

    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=mysql_dialect))
        assert "CREATE TABLE" in ddl
        assert "JSONB" not in ddl
        table_names.add(table.name)

    assert table_names == {
        "agent_call_logs",
        "agent_knowledge_bases",
        "agents",
        "ai_tools",
        "conversations",
        "knowledge_bases",
        "knowledge_documents",
        "messages",
        "model_configs",
        "skill_run_records",
    }
