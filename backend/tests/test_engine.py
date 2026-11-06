from app.engine import category_for
def test_db(): assert category_for("ERROR database connection refused")[0]=="database"
def test_memory(): assert category_for("MemoryError out of memory")[0]=="memory"
def test_unknown(): assert category_for("normal request completed")[0]=="unknown"
