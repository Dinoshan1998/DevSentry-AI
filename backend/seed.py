from app.db import Base,engine,Session
from app.models import Knowledge
Base.metadata.create_all(bind=engine)
db=Session()
if db.query(Knowledge).count()==0:
 db.add_all([
  Knowledge(title="Database runbook",content="For connection refused: check database service health, hostname, port, firewall, connection pool saturation, credentials and recent deployments. Validate in staging."),
  Knowledge(title="Memory runbook",content="For out of memory: inspect container metrics, heap profile, traffic and recent deployments. Reproduce in test before changing memory limits.")
 ])
 db.commit()
db.close()
print("Seeded sample runbooks")
